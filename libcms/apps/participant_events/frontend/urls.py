# -*- coding: utf-8 -*-
from django.conf.urls import *
import views
urlpatterns = patterns(views,
    url(r'^$', views.index , name="index"),
    url(r'^subscribe/$', views.subscribe , name="subscribe"),
    url(r'^subscribe/complate/$', views.subscribe_complate , name="subscribe_complate"),

    url(r'^(?P<id>\d+)/$', views.show , name="show"),
    url(r'^(?P<id>\d+)/notification/$', views.create_notification , name="create_notification"),
    url(r'^(?P<id>\d+)/notification/created/$', views.create_notification_complate , name="create_notification_complete"),

    url(r'^(?P<id>\d+)/ical$', views.make_icalendar , name="make_icalendar"),
    url(r'^date/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.filer_by_date, name="events_by_date"),
    url(r'^favorits/$', views.favorit_events , name="favorit_events"),
    url(r'^favorits/(?P<id>\d+)/$', views.favorite_show , name="favorite_show"),
    url(r'^(?P<id>\d+)/add_to_favorite/$', views.add_to_favorits , name="add_to_favorits"),
)
