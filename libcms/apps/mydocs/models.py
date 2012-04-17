# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
class SavedDocument(models.Model):
    user = models.ForeignKey(User)
    gen_id = models.CharField(max_length=32, db_index=True)
    comments = models.CharField(max_length=2048, blank=True, verbose_name=u"Комментарии к документу")
    add_date = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=u"Дата добваления документа")
