# -*- coding: utf-8 -*-
from django.conf.urls import *

import views

urlpatterns = patterns('',
    url(r'^$', views.index , name="index"),
    url(r'^polls/$', views.polls_list, name="polls_list"),
    url(r'^polls/create/$', views.create_poll , name="create_poll"),
    url(r'^polls/(?P<id>\d+)/detail/$', views.poll_detail, name="poll_detail"),
    url(r'^polls/(?P<id>\d+)/edit/$', views.edit_poll, name="edit_poll"),
    url(r'^polls/(?P<id>\d+)/delete/$', views.delete_poll, name="delete_poll"),

    url(r'^polls/(?P<id>\d+)/images/create/$', views.create_poll_image, name="create_poll_image"),
    url(r'^polls/(?P<id>\d+)/images/(?P<image_id>\d+)/edit/$', views.edit_poll_image, name="edit_poll_image"),
    url(r'^polls/(?P<id>\d+)/images/(?P<image_id>\d+)/delete/$', views.delete_poll_image, name="delete_poll_image"),
)