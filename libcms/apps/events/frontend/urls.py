# -*- coding: utf-8 -*-
from django.conf.urls import *
import views
urlpatterns = patterns(
    '',
    url(r'^$', views.index , name="index"),
    url(r'^(?P<id>\d+)/$', views.show , name="show"),
    url(r'^date/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.index, name="events_by_date"),
)
