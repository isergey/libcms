# -*- coding: utf-8 -*-
from django.conf.urls import *
from . import views

urlpatterns = patterns(
    '',
    url(r'^(?P<section>[a-z0-9]+)/$', views.index, name='index'),
    url(r'^items/(?P<id>\d+)/$', views.detail, name='detail'),
)
