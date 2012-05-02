# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import to_locale, get_language
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from participants.models import Library
class Permissions(User):
    """
    Класс для создания прав достпа
    """
    class Meta:
        proxy = True
        permissions = (
            ("view_page", "Can view page"),
            ("public_page", "Can public page"),
        )




class Page(MPTTModel):
    def set_title(self, title):
        self.title = title
    def get_title(self, title):
        return self.title


    library = models.ForeignKey(
        Library,
        verbose_name=u'ЦБС, которой принадлежит страница'
    )

    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        verbose_name=u'Родительская страница'
    )

    slug = models.SlugField(
        verbose_name=u'Slug',
        max_length=255,
        db_index=True,
        unique=True,
        help_text=u'Внимание! Последующее редактирование поля slug невозможно!'
    )

    url_path = models.CharField(
        max_length=2048,
        db_index=True
    )

    public = models.BooleanField(
        verbose_name=u'Опубликована?',
        default=False,
        db_index=True,
        help_text=u'Публиковать страницу могут только пользователи с правами публикации страниц'
    )

    create_date = models.DateTimeField(
        verbose_name=u"Дата создания",
        auto_now_add=True,
        db_index=True
    )
    def get_cur_lang_content(self):
        cur_language = get_language()
        try:
            content = Content.objects.get(page=self, lang=cur_language[:2])
        except Content.DoesNotExist:
            content = None
        return content

    def get_ancestors_titles(self):
        """
        return translated ancestors
        """
        ancestors = list(self.get_ancestors())
        lang=get_language()[:2]
        ad = {}
        for ancestor in ancestors:
            ad[ancestor.id] = ancestor
        contents = Content.objects.filter(page__in=ancestors, lang=lang).values('page_id', 'title')
        for content in contents:
            ad[content['page_id']].title = content['title']
        return ancestors

    class Meta:
        ordering = ['-create_date']

    def __unicode__(self):
        return  self.slug

    def save(self, *args, **kwargs):
        old = None
        if self.id:
            old = Page.objects.get(id=self.id)

        if old and self.slug != old.slug:
            self.slug = old.slug
        else:
            url_pathes = []
            if self.parent:
                for node in  self.parent.get_ancestors():
                    url_pathes.append(node.slug)
                url_pathes.append(self.parent.slug)
                url_pathes.append(self.slug)
            else:
                url_pathes.append(self.slug)

            self.url_path =  u'/'.join(url_pathes)

        return super(Page, self).save(*args, **kwargs)


class Content(models.Model):
    page = models.ForeignKey(
        Page,
        verbose_name=u'Родительская страница'
    )

    lang = models.CharField(
        verbose_name=u"Язык",
        db_index=True,
        max_length=2,
        choices=settings.LANGUAGES
    )

    title = models.CharField(
        verbose_name=u'Заглавие',
        max_length=512
    )

    meta = models.CharField(
        verbose_name=u"SEO meta",
        max_length=512,
        blank=True,
        help_text=u'Укажите ключевые слова для страницы, желательно на языке контента'
    )
    content = models.TextField(verbose_name=u'Контент')

    class Meta:
        unique_together = (('page', 'lang'),)

    def __unicode__(self):
        return self.title


    def return_in_lang(self):
        pass