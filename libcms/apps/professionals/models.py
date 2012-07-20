# -*- encoding: utf-8 -*-
from django.shortcuts import urlresolvers
from django.conf import settings
from django.db import models


class Professionals(models.Model):
    class Meta:
        permissions = (
            ("can_access_prof_page", "Can access professional page"),
        )
