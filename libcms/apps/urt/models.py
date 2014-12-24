# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from participants.models import Library

class LibReader(models.Model):
    user = models.ForeignKey(User, verbose_name=u'Пользователь', unique=True)
    # library = models.ForeignKey(Library, verbose_name=u'Библиотека')
    reader_id = models.CharField(max_length=255, verbose_name=u'Идентификатор читательского билета', unique=True)
    # lib_password = models.CharField(max_length=255, verbose_name=u'Пароль, выданный библиотекой')
