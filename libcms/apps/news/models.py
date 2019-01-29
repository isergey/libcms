# -*- encoding: utf-8 -*-
from django.shortcuts import urlresolvers
from django.conf import settings
from django.db import models
from django.db.models import Count
from datetime import datetime

NEWS_TYPE_CHOICES = (
    (0, u'Публичные'),
    (1, u'Профессиональные'),
    (2, u'Общие'),
)


class News(models.Model):
    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"Дата создания", db_index=True)
    type = models.IntegerField(verbose_name=u'Вид новостей', default=(0, u'Публичные'), choices=NEWS_TYPE_CHOICES,
                               db_index=True)
    publicated = models.BooleanField(verbose_name=u'Опубликовано?', default=True, db_index=True)

    # avatar_img_name = models.CharField(max_length=100, blank=True)
    def get_absolute_url(self):
        return urlresolvers.reverse('news:frontend:show', args=[self.id])


class NewsContent(models.Model):
    news = models.ForeignKey(News)
    lang = models.CharField(verbose_name=u"Язык", db_index=True, max_length=2, choices=settings.LANGUAGES)
    title = models.CharField(verbose_name=u'Заглавие', max_length=512, blank=True)
    teaser = models.CharField(verbose_name=u'Тизер', max_length=512, help_text=u'Краткое описание новости', blank=True)
    content = models.TextField(verbose_name=u'Содержание новости', blank=True)

    def __init__(self, *args, **kwargs):

        super(NewsContent, self).__init__(*args, **kwargs)

        self.__default_lang_content = None

    class Meta:
        unique_together = (('news', 'lang'),)

    def get_title(self):
        if self.title.strip():
            return self.title

        default_lang_content = self.__get_default_lang_content()
        if default_lang_content:
            return default_lang_content.title

        return ''

    def get_teaser(self):
        if self.teaser.strip():
            return self.teaser

        default_lang_content = self.__get_default_lang_content()
        if default_lang_content:
            return default_lang_content.teaser

        return ''

    def get_content(self):
        if self.content.strip():
            return self.content

        default_lang_content = self.__get_default_lang_content()
        if default_lang_content:
            return default_lang_content.content

        return ''

    def __get_default_lang_content(self):
        if self.__default_lang_content is not None:
            return self.__default_lang_content
        try:
            self.__default_lang_content = NewsContent.objects.get(news_id=self.news_id, lang=settings.LANGUAGES[0][0])
        except NewsContent.DoesNotExist:
            return None

        return self.__default_lang_content
