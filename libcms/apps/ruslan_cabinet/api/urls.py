# -*- coding: utf-8 -*-
from django.conf.urls import *
import views

urlpatterns = (
    url(r'^$', views.index, name="index"),
    url(r'^config/$', views.get_config, name="get_config"),
    url(r'^holdings/$', views.holdings, name="holdings"),
    url(r'^make_reservation/$', views.make_reservation, name="make_reservation"),
    # url(r'^search/$', views.search, name="search"),
    #url(r'^get_records/$', views.get_records, name="get_records"),
)
