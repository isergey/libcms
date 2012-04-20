# -*- coding: utf-8 -*-
import datetime
import hashlib
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as __
from django.db import models
from django.core.exceptions import ValidationError

from mptt.models import MPTTModel, TreeForeignKey
from django.core.cache import cache

class AnswerManager(models.Model):
    """
    Профиль пользователя, уполномоченного отвечать на вопросы
    Принадлежность пользователя к организации можно узнать из модуля управления аккаунтами
    где присутвует связь между пользователями и организациями
    """
    user = models.ForeignKey(User,verbose_name=_(u'User, who can give the answer'), unique=True)
#    name = models.CharField(max_length=32, verbose_name=_(u'Name'))
#    surname = models.CharField(max_length=32, verbose_name=_(u'Surname'))
    phone = models.CharField(max_length=16, verbose_name=_(u'Phone number'))

    def __unicode__(self):
        return u'%s %s' % (self.user.last_name, self.user.first_name)

    @classmethod
    def get_non_active_managers(cls):
        """
        Возвращает QuerySet с неактивными менеджерами
        """
        not_active_periods = ManagerNonActivePeriod.get_not_active_periods()
        not_active_managers_id = []
        for not_active_period in not_active_periods:
            not_active_managers_id.append(not_active_period.manager_id)
        return cls.objects.filter(id__in=not_active_managers_id)

    @classmethod
    def get_active_managers(cls):
        """
        Возвращает QuerySet с активными менеджерами
        """
        not_active_periods = ManagerNonActivePeriod.get_not_active_periods()
        not_active_managers_id = []
        for not_active_period in not_active_periods:
            not_active_managers_id.append(not_active_period.manager_id)
        return cls.objects.all().exclude(id__in=not_active_managers_id)



class ManagerNonActivePeriod(models.Model):
    """
    Период, когда менеджер ответов недоступен
    """
    manager = models.ForeignKey(AnswerManager)
    start = models.DateTimeField(verbose_name=_(u'Start date of non active period'))
    end = models.DateTimeField(verbose_name=_(u'End date of non active period'))
    reason = models.CharField(max_length=256, blank=True, verbose_name=_(u'Reason, why not active'))

    @classmethod
    def get_not_active_periods(cls):
        """
        Возварщает QuerySet с неактивные периоды
        """
        now = datetime.datetime.now()
        return cls.objects.filter(start__lte=now, end__gte=now)


    def clean(self):
        """
        Проверка корректности периода:
            - дата конца периода должна быть больше даты начала периода
        """

        if self.end <= self.start:
            raise ValidationError(__(u'End date and time must be more then start'))

        return super(ManagerNonActivePeriod, self).clean()
    def __unicode__(self):
        return unicode(self.manager)






class Category(MPTTModel):
    """
    Категория вопроса
    Статус изменяется в сигналах set_question_status_processed, set_question_status_new
    """
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    name = models.CharField(max_length=50,verbose_name=_(u'Question category name'), db_index=True)
    def __unicode__(self):
        return self.name
    def get_count(self):
        #self.name + unicode(self.parent_id)
        key = hashlib.md5(self.name.encode('utf-8') + str(self.parent_id)).hexdigest()
        questions_count = cache.get(key, default=None)
        if questions_count == None:
            filter_categories = self.get_descendants(include_self=True)
            questions_count = Question.objects.filter(category__in=filter_categories).count()
            cache.set(key,questions_count)
        return  questions_count

    class MPTTMeta:
        order_insertion_by = ['name']

class AnswerLanguage(models.Model):
    """
    Язык, на котором можно давать ответ
    """
    name = models.CharField(max_length=16, verbose_name=_(u'Language name'))
    def __unicode__(self):
        return self.name

QUESTION_STATUSES = (
    (0, _(u'New')),
    (1, _(u'Processed')),
    (2, _(u'Rejected')),
)

class Question(models.Model):
    """
    Впрос, который поступает от пользователя
    """
    user = models.ForeignKey(User, null=True, blank=True)
    text = models.TextField(max_length=1024, verbose_name=_(u'Text of question'))
    answer_language = models.ManyToManyField(
        AnswerLanguage,
        verbose_name=_(u'The answer may contain links and materials on the languages of chosen'),
        db_index=True
    )
    category = models.ForeignKey(Category, verbose_name=_(u'Question category'), db_index=True)
    create_date = models.DateTimeField(auto_now=True, auto_now_add=True, db_index=True)
    status = models.IntegerField(verbose_name=_(u'Question status'), choices=QUESTION_STATUSES, default=0, db_index=True)

    @models.permalink
    def get_absolute_url(self):
        return ('ask_librarian:question_detail', [str(self.id)])

    def __unicode__(self):
        return self.text

    def get_category_path(self):
        ancestors = self.category.get_ancestors(include_self=True)
        return ancestors

    class Meta:
        permissions = (
            ("view_question", __("Can see question")),
        )


class AssignManager(models.Model):
    """
    Менеджер, которому назначен вопрос
    """
    answer_manager = models.ForeignKey(AnswerManager)
    question = models.ForeignKey(Question, unique=True)
    create_date = models.DateTimeField(auto_now=True, auto_now_add=True, db_index=True)




class Answer(models.Model):
    """
    Ответ на вопрос. Дается пользователем, который принадлежит AnswerManager
    """
    question = models.ForeignKey(Question, db_index=True)
    manager = models.ForeignKey(AnswerManager,verbose_name=_(u'Answer manager'), db_index=True)
    text = models.TextField(max_length=2048, verbose_name=_(u'Text of answer'))
    create_date = models.DateTimeField(auto_now=True, auto_now_add=True, db_index=True)
    @models.permalink
    def get_absolute_url(self):
        return ('ask_librarian:question_detail', [str(self.question_id)])



@receiver(post_save, sender=Answer)
def set_question_status_processed(sender, instance, **kwargs):
    """
    Установка статуса вопроса в "Processed" при создании ответа
    """
    question = instance.question
    question.status = 1 # Processed
    question.save()


@receiver(post_delete, sender=Answer)
def set_question_status_new(sender, instance, **kwargs):
    """
    Установка статуса вопроса в "New" если больше нет ответов
    """
    question = instance.question
    if Answer.objects.filter(question=question).count() == 0:
        question.status = 0 # New
        question.save()