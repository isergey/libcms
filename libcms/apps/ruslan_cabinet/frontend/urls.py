# -*- coding: utf-8 -*-
from django.conf.urls import *
import views

urlpatterns = (
    url(r'^$', views.on_hand, name="on_hand"),
    url(r'^current/$', views.current_orders, name="current_orders"),
    url(r'^holding_info/$', views.holding_info, name="holding_info"),
    url(r'^make_order/$', views.make_order, name="make_order"),
    # url(r'^make_order/$', views.make_order, name="make_order"),
)
