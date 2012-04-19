# -*- coding: utf-8 -*-
from django.conf.urls import *
import views
urlpatterns = patterns(views,
    url(r'^$', views.index , name="index"),
    url(r'^(?P<id>\d+)/$', views.lib_orders, name="lib_orders"),
    url(r'^zorder/(?P<library_id>\d+)/$', views.zorder, name="zorder"),
    url(r'^mbaorder/$', views.mba_orders, name="mba_orders"),
    url(r'^mbaorder/copy/$', views.mba_order_copy, name="mba_order_copy"),
    url(r'^mbaorder/delivery/$', views.mba_order_delivery, name="mba_order_delivery"),
)