# coding=utf-8
from django.conf import settings
from django.db import models
from participants.models import Library


BANNER_PLACES = (
    ('left', u'Слева'),
    ('bottom', u'Под профилем библиотеки')
)


class Banner(models.Model):
    libraries = models.ManyToManyField(
        Library,
        blank=True,
        verbose_name=u'Организации, на сайтах которых будет показан банер'
    )
    library_creator = models.ForeignKey(Library, related_name='library_creator')
    in_descendants = models.BooleanField(
        default=False,
        verbose_name=u'Банер отображается на сайтах дочерних организаций'
    )
    lang = models.CharField(
        verbose_name=u"Язык",
        db_index=True,
        max_length=2,
        choices=settings.LANGUAGES,
        help_text=u'Язык системы, при котором будет отображен банер'
    )
    place = models.CharField(
        max_length=64,
        choices=BANNER_PLACES,
        default=BANNER_PLACES[0][0],
        verbose_name=u'Место размещения'
    )
    image = models.ImageField(upload_to=u'participant_banners/%Y/%m/%d')
    title = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=u'Название'
    )
    description = models.TextField(
        max_length=1000,
        blank=True,
        verbose_name=u'Описание'
    )
    url = models.CharField(
        max_length=500,
        verbose_name=u'Ссылка для клика по банеру',
        blank=True
    )
    target_blank = models.BooleanField(
        default=False,
        verbose_name=u'Открывать ссылку в новой вкладке'
    )
    show_period = models.IntegerField(
        default=5,
        help_text=u'Период показа в секундах'
    )
    global_banner = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name=u'Глобальный банер',
        help_text=u'Будет отображен на всех сайтах без исключения'
    )
    active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name=u'Активный'
    )
    order = models.IntegerField(
        default=0,
        verbose_name=u'Порядок вывода',
        db_index=True
    )
    start_date = models.DateTimeField(verbose_name=u'Дата начала показа', db_index=True)
    end_date = models.DateTimeField(verbose_name=u'Дата окончания показа', db_index=True)

    class Meta:
        ordering = ['-order', '-id']
        verbose_name = u'Банер'
        verbose_name_plural = u'Банеры'
        permissions = (
            ('bind_to_descendants', u'Bind to descendants organisations'),
        )