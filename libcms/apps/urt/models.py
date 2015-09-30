# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from participants.models import Library


class LibReader(models.Model):
    user = models.ForeignKey(User, verbose_name=u'Пользователь')
    library = models.ForeignKey(Library, verbose_name=u'Библиотека')
    lib_login = models.CharField(max_length=32, verbose_name=u'Идентификатор присвоенный библиотекой')
    lib_password = models.CharField(max_length=255, verbose_name=u'Пароль, выданный библиотекой')

    class Meta:
        unique_together = ['user', 'library']
