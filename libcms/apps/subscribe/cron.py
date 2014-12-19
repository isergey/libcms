# coding=utf-8
from django.conf import settings
from django.utils import translation

from django_cron import CronJobBase, Schedule
from apps.subscribe import models


translation.activate(settings.LANGUAGE_CODE)



class SendLetters(CronJobBase):
    RUN_EVERY_MINS = 60
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'subscribe.send_letters'

    def do(self):
        models.send_letters()
        models.send_to_email()
