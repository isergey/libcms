# -*- coding: utf-8 -*-
from django.conf.urls import *
import views
urlpatterns = patterns(
    '',
    url(r'^$', views.index, name="index"),
    url(r'^redirect$', views.redirect, name="redirect"),
    #url(r'^login/$', views.login, name="login"),
)

