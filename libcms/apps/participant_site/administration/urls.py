# -*- coding: utf-8 -*-
from django.conf.urls import *
import views
urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    url(r'^info$', views.edit_info, name="edit_info"),
)