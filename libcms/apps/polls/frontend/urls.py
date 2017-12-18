# -*- coding: utf-8 -*-
from django.conf.urls import *
import views
urlpatterns = patterns(views,
    url(r'^$', views.index , name="index"),
    url(r'^(?P<poll_id>\d+)/$', views.vote , name="vote"),
    url(r'^(?P<poll_id>\d+)/results/$', views.results , name="results"),
#    url(r'^rss/$', feeds.LatestEntriesFeed(), name='rss'),
)
