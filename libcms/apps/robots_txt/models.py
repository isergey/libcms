# -*- encoding: utf-8 -*-
from django.db import models


class Content(models.Model):
    text = models.TextField(max_length=2048, verbose_name=u'Содержимое robots.txt')
    def __unicode__(self):
        return self.text

