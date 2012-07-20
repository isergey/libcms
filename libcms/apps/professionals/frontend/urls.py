# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('professionals.frontend.views',
    url(r'^$', 'index', name="index"),
)