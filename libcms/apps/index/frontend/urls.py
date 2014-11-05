# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('index.frontend.views',
    url(r'^$', 'index', name="index"),
)