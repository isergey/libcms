# -*- coding: utf-8 -*-
from django.conf.urls import *


urlpatterns = patterns('core.views',
    # Индексная страница
    url(r'^$', 'index', name="index"),
    url(r'^select_language/$', 'select_language', name="select_language"),
    url(r'^set_language/', 'set_language', name='set_language'),


)
