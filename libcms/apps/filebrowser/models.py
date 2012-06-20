# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
    name = models.CharField(max_length=128)


