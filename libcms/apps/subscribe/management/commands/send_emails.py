# encoding: utf-8
from django.conf import settings
from django.utils import translation
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError

from apps.subscribe import models

class Command(BaseCommand):
    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        now = datetime.now()
        models.send_to_email()
        models.clear_statuses()
        self.stdout.write(u"Emails was successfully sended at %s \n" % unicode(now))