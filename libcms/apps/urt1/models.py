# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from participants.models import Library


class LibReader(models.Model):
    user = models.OneToOneField(User, verbose_name=u'Пользователь')
    library = models.ForeignKey(Library, verbose_name=u'Библиотека')
    lib_login = models.CharField(max_length=255, verbose_name=u'Идентификатор читательского билета', unique=True)
    lib_password = models.CharField(max_length=255, verbose_name=u'Пароль, выданный библиотекой')
