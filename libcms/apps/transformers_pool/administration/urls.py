# -*- coding: utf-8 -*-
from django.conf.urls import *
import views

urlpatterns = (
    url(r'^$', views.index, name="index"),
    url(r'^xslt/$', views.xslt, name="xslt"),
)
