# -*- coding: utf-8 -*-
from django.conf.urls import *
import views
urlpatterns = patterns(views,
    url(r'^$', views.index , name="index"),
    url(r'^(?P<id>\d+)/$', views.show , name="show"),
    url(r'^date/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.filer_by_date, name="events_by_date"),
    url(r'^favorits/$', views.favorit_events , name="favorit_events"),
    url(r'^favorits/(?P<id>\d+)/$', views.favorite_show , name="favorite_show"),
    url(r'^(?P<id>\d+)/add_to_favorite/$', views.add_to_favorits , name="add_to_favorits"),
)
