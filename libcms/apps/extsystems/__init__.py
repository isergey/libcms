# coding=utf-8
from django.apps import AppConfig

default_app_config = 'extsystems.AppConfig'


class AppConfig(AppConfig):
    name = 'extsystems'
    verbose_name = u'Внешние системы'
