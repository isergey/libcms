# -*- encoding: utf-8 -*-
from datetime import datetime

from django.shortcuts import urlresolvers
from django.conf import settings
from django.db import models
from participants.models import Library

class News(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    show_avatar = models.BooleanField(verbose_name=u"Показывать аватарку", default=False)
    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"Дата создания", db_index=True)
    order = models.IntegerField(default=0, verbose_name=u'Приоритет', db_index=True, help_text=u'Новости сортируются по приоритету, далее - по дате создания. 0 - по умолчанию.')
    publicated = models.BooleanField(verbose_name=u'Опубликовано?', default=True, db_index=True)
    avatar_img_name = models.CharField(max_length=512, blank=True)
    lang = models.CharField(
        verbose_name=u"Язык", db_index=True, max_length=2, choices=settings.LANGUAGES, default=settings.LANGUAGES[0],
        help_text=u'Новость на сайте появится при соответствующем языке'
    )
    title = models.CharField(verbose_name=u'Заглавие', max_length=512)
    teaser = models.CharField(verbose_name=u'Тизер', max_length=512, help_text=u'Краткое описание новости')
    content = models.TextField(verbose_name=u'Содержание новости')
    def get_absolute_url(self):
        return urlresolvers.reverse('participant_news:frontend:show', args=[self.library.code, self.id])

    class Meta:
        ordering = ['order', '-create_date']





from django.db.models.signals import post_delete
from attacher.frontend.views import delete_content_attaches
def remove_attachments(sender, **kwargs):
    delete_content_attaches('participant_news', str(kwargs['instance'].id))
    pass


post_delete.connect(remove_attachments, sender=News)