# -*- coding: utf-8 -*-
from django.conf.urls import *
import views

urlpatterns = patterns(
    views,
    url(r'^$', views.index, name="index"),
    url(r'^geosearch/$', views.geosearch, name="geosearch"),
    url(r'^geosearch/nearest/$', views.geo_nearest, name="geo_nearest"),
    url(r'^branches/(?P<code>[/_\-0-9A-Za-z]+)/$', views.branches, name="branches"),
    url(r'^get_district_letters/$', views.get_district_letters, name="get_district_letters"),
    url(r'^filter_by_districts/$', views.filter_by_districts, name="filter_by_districts"),
    # в этом вызове id передается в GET
    url(r'^branches/$', views.branches, name="branches"),
    url(r'^detail/(?P<code>[/_\-0-9A-Za-z]+)/$', views.detail, name="detail"),
)
