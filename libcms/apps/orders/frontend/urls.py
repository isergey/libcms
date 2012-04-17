# -*- coding: utf-8 -*-
from django.conf.urls import *
import views
urlpatterns = patterns(views,
    url(r'^$', views.index , name="index"),
    url(r'^(?P<id>\d+)/$', views.lib_orders, name="lib_orders"),
    url(r'^zorder/(?P<library_id>\d+)/$', views.zorder, name="zorder"),
)