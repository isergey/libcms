# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from participants.models import Library

class MenuItem(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=_(u'Родительский элемент'))
    show = models.BooleanField(verbose_name=u"Отображать пункт", default=True, db_index=True)
    open_in_new = models.BooleanField(verbose_name=u'Открывать в новой вкладке браузера', default=False)

    def get_t_ancestors(self):
        """
        return translated ancestors
        """
        ancestors = list(self.get_ancestors())
        lang=get_language()[:2]
        items = MenuItemTitle.objects.filter(item__in=ancestors, lang=lang)
        return items

    def title(self):
        lang=get_language()[:2]
        # print 'lang', lang
        #print 'ed',  MenuItemTitle.objects.get(lang=lang, item=self)
        return ''

    def __unicode__(self):
        return self.title()

    def up(self):
        previous = self.get_previous_sibling()
        if previous:
            self.move_to(previous, position='left')

    def down(self):
        next = self.get_next_sibling()
        if next:
            self.move_to(next, position='right')

class MenuItemTitle(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    lang = models.CharField(verbose_name=u"Язык", db_index=True, max_length=2, choices=settings.LANGUAGES)
    title = models.CharField(verbose_name=u'Заглавие', max_length=512)
    url = models.CharField(verbose_name=u'URL для этого языка', max_length=1024, default='#')

    def __unicode__(self):
        return self.title
    class Meta:
        unique_together = (('item', 'lang'),)

class Menu(models.Model):
    slug = models.SlugField(verbose_name=u'Slug', max_length=64)
    root_item = models.OneToOneField(MenuItem)
    library = models.ForeignKey(Library, verbose_name=u'Орагниция, которой принадлежит меню', on_delete=models.CASCADE)
    def title(self):
        lang=get_language()[:2]
        return MenuTitle.objects.get(lang=lang, menu=self).title

    class Meta:
        unique_together = ('slug', 'library')

class MenuTitle(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    lang = models.CharField(verbose_name=u"Язык", db_index=True, max_length=2, choices=settings.LANGUAGES)
    title = models.CharField(verbose_name=u'Заглавие', max_length=512)
    class Meta:
        unique_together = (('menu', 'lang'),)

