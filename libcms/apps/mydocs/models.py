# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class List(models.Model):
    name = models.CharField(
        verbose_name='Название списка',
        max_length=255
    )

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class SavedDocument(models.Model):
    user = models.ForeignKey(User)
    gen_id = models.CharField(max_length=32, db_index=True)
    list = models.ForeignKey(
        List, null=True, blank=True, on_delete=models.SET_NULL,
        verbose_name='Список документов',
        help_text='Добавить спискок можно в Моих документах'
    )
    comments = models.CharField(max_length=2048, blank=True, verbose_name=u"Комментарии к документу")
    add_date = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=u"Дата добваления документа")
