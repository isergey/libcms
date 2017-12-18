# -*- coding: utf-8 -*-
from django.utils import timezone
from django.db import models
import datetime

POLL_TYPE_CHOICES = (
    ('radio', u"Радио"),
    ('checkboxes', u"Галочки"),
)


class Poll(models.Model):
    question = models.CharField(
        verbose_name=u"Вопрос",
        max_length=255, null=False, blank=False
    )

    multi_vote = models.BooleanField(
        verbose_name=u"Возможность голосовать несколько раз",
        null=False, blank=False, default=False, choices=(
            (False, u"Нет"), (True, u"Да"))
    )

    poll_type = models.CharField(
        verbose_name=u"Тип голосования",
        help_text=u'Радио - можно голосовать за один вариант. Галочки - за несколько.',
        max_length=16, choices=POLL_TYPE_CHOICES, default='radio'
    )

    show_results_on_vote = models.BooleanField(
        verbose_name=u"Показывать результаты после ответа",
        null=False, blank=False, default=False
    )

    published = models.BooleanField(
        verbose_name=u"Опубликовано",
        null=False, blank=False, db_index=True
    )

    start_poll_date = models.DateTimeField(
        verbose_name=u"Дата начала голосования",
        null=False, blank=False, db_index=True
    )

    end_poll_date = models.DateTimeField(
        verbose_name=u"Дата окончания голосования",
        null=False, blank=False, db_index=True
    )

    show_results_after_end_poll = models.BooleanField(
        verbose_name=u"Показывать результаты после даты окончания голосования",
        null=False, blank=False, default=False
    )

    def is_active(self):
        now = timezone.now()
        return now >= self.start_poll_date and now < self.end_poll_date

    def __unicode__(self):
        return self.question

    class Meta:
        verbose_name = u"голосование"
        verbose_name_plural = u"голосования"
        permissions = (
            ('can_vote', u'Может голосовать'),
            ('can_view_results', u'Может просматривать результаты'),
        )


class Choice(models.Model):
    poll = models.ForeignKey(Poll, verbose_name=u"Голосование")
    avatar = models.ImageField(
        verbose_name=u'Изображение',
        help_text=u'Используйте изображения только в формата JPG или PNG',
        upload_to='polls/%Y/%m',
        max_length=255,
        # blank=True
    )
    choice = models.TextField(
        verbose_name=u"Вариант ответа",
        max_length=255, null=False, blank=False
    )

    record_id = models.CharField(
        verbose_name=u'Идентификатор записи', max_length=256, blank=True
    )

    votes = models.IntegerField(verbose_name=u"Количество голосов", default=0)
    sort = models.IntegerField(verbose_name=u'Сортировка', default=0)

    def __unicode__(self):
        return self.choice

    class Meta:
        verbose_name = u"вариант ответа"
        verbose_name_plural = u"варианты ответов"


class PolledUser(models.Model):
    poller_id = models.CharField(
        max_length=32,
        verbose_name=u"Идентификатор сессии (md5) или имя пользователя",
        db_index=True
    )

    poll = models.ForeignKey(Poll)
