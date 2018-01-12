# coding=utf-8
import json
from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError


SEX_CHOICES = (
    ('m', u'М'),
    ('f', u'Ж')
)


class RuslanUser(models.Model):
    user_id = models.CharField(max_length=256, db_index=True, unique=True)
    first_name = models.CharField(max_length=256, blank=True)
    patronymic = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    email = models.EmailField(max_length=256, blank=True)
    birth_date = models.DateField(null=True, db_index=True)
    sex = models.CharField(max_length=1, db_index=True, choices=SEX_CHOICES)
    grs_json = models.TextField(max_length=1024 * 1024)
    active = models.BooleanField(default=True, db_index=True)
    sync_session = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class SyncStatus(models.Model):
    sync_started_at = models.DateTimeField(null=True)
    last_sync = models.DateTimeField(null=True)
    refresh_next_time = models.BooleanField(default=False)
    record_processed = models.IntegerField(default=0)
    sync_session = models.IntegerField(default=0)

    def clean(self):
        if SyncStatus.objects.all().count() > 1:
            raise ValidationError(u'Уже существует статус синхронизации')

    @staticmethod
    def get_or_create():
        status_list = SyncStatus.objects.all()
        if not len(status_list):
            sync_status = SyncStatus()
            sync_status.save()
            return sync_status
        return status_list[0]
