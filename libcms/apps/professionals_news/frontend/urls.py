# -*- coding: utf-8 -*-
from django.conf.urls import *
import views
#import feeds
urlpatterns = patterns(views,
    url(r'^$', views.index , name="index"),
    url(r'^(?P<id>\d+)/$', views.show , name="show"),
#    url(r'^rss/$', feeds.LatestEntriesFeed(), name='rss'),
)
