# -*- coding: utf-8 -*-
from django.conf.urls import *
import views
urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    url(r'^link/$', views.link, name="link"),
    url(r'^auth/(?P<id>\d+)/$', views.auth, name="auth"),
    url(r'^link/edit/(?P<id>\d+)/$', views.edit_link, name="edit_link"),
)
