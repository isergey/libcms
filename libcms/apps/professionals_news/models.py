# -*- encoding: utf-8 -*-
from django.shortcuts import urlresolvers
from django.conf import settings
from django.db import models


class News(models.Model):
    create_date = models.DateTimeField(auto_now=True, verbose_name=u"Дата создания", db_index=True)
    publicated = models.BooleanField(verbose_name=u'Опубликовано?', default=True, db_index=True)
    class Meta:
        permissions = (
            ("can_views_prof_news", "Can view professional news"),
        )
    def get_absolute_url(self):
        return urlresolvers.reverse('news:frontend:show', args=[self.id])

class NewsContent(models.Model):
    news = models.ForeignKey(News)
    lang = models.CharField(verbose_name=u"Язык", db_index=True, max_length=2, choices=settings.LANGUAGES)
    title = models.CharField(verbose_name=u'Заглавие', max_length=512)
    teaser = models.CharField(verbose_name=u'Тизер', max_length=512)
    content = models.TextField(verbose_name=u'Содержание новости')
    class Meta:
        unique_together = (('news', 'lang'),)

