# -*- coding: utf-8 -*-
from django.conf.urls import *

import views

urlpatterns = patterns('',
    url(r'^$', views.index , name="index"),
    url(r'^events/$', views.events_list, name="events_list"),
    url(r'^events/create/$', views.create_event , name="create_event"),
    url(r'^events/edit/(?P<id>\d+)/$', views.edit_event, name="edit_event"),
    url(r'^events/delete/(?P<id>\d+)/$', views.delete_event, name="delete_event"),
)