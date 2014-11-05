# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('index.administration.views',
    url(r'^$', 'index', name="index"),
)