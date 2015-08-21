# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from ... import models

class Command(BaseCommand):
    help = u'Синхронизация паролей с LDAP сервером'

    def handle(self, *args, **options):
        models.sync_all_passwords()