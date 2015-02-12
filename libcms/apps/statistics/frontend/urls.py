# coding: utf-8
from django.conf.urls import *
import views
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^org/$', views.org_stats, name='org_stats'),
    url(r'^search/$', views.search_stats, name='search_stats'),
    url(r'^watch/$', views.watch, name='watch'),
)