# coding=utf-8
import uuid
from django.db import models

def generate_uuid():
   return uuid.uuid4()

class Party(models.Model):
    contactemail = models.EmailField(
        verbose_name=u'Контатный email',
        max_length=255,
        blank=True,
        null=True
    )
    contactperson = models.CharField(
        verbose_name=u'Контактное лицо',
        max_length=255, blank=True, null=True
    )
    endpoint = models.CharField(
        verbose_name=u'Точка доступа',
        max_length=255, blank=True, null=True
    )
    hours = models.IntegerField(
        verbose_name=u'Часы',
        blank=True, null=True
    )
    minutes = models.IntegerField(
        verbose_name=u'Минуты',
        blank=True, null=True
    )
    name = models.CharField(
        verbose_name=u'Название',
        max_length=255, blank=True, null=True
    )
    notify = models.NullBooleanField()
    status = models.NullBooleanField()
    token = models.CharField(max_length=255, blank=True, null=True, default=generate_uuid)

    class Meta:
        managed = False
        verbose_name = u'Система'
        verbose_name_plural = u'Системы'

    def __unicode__(self):
        return self.name or u"без названия"