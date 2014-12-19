# encoding: utf-8
from django.conf import settings
from django.utils import translation
from django.core.management.base import BaseCommand

from apps.subscribe import models

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        models.send_letters()