# -*- coding: utf-8 -*-
from django.conf.urls import *
import views

urlpatterns = patterns(
    views,
    url(r'^$', views.index, name="index"),
    url(r'^(?P<id>\d+)/$', views.show, name="show"),
    url(r'^(?P<poll_id>\d+)/(?P<image_id>\d+)/vote/$', views.vote, name="vote"),
)
