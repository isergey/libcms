# -*- coding: utf-8 -*-
from django.conf.urls import *
import views

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    url(r'^upload/$', views.upload, name="upload"),
    url(r'^create_directory/$', views.create_directory, name="create_directory"),
    url(r'^delete/$', views.delete, name="delete"),
)