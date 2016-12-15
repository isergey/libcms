# -*- coding: utf-8 -*-
from django.conf.urls import *
import views
urlpatterns = patterns(views,
    url(r'^$', views.index , name="index"),
    url(r'^on_hand$', views.books_on_hand , name="on_hand"),
    url(r'^reservations$', views.reservations , name="reservations"),
    url(r'^on_hand/(?P<id>\d+)/', views.books_on_hand_in_lib , name="on_hand_in_lib"),
    url(r'^(?P<id>\d+)/$', views.lib_orders, name="lib_orders"),
    url(r'^zorder/(?P<library_id>\d+)/$', views.zorder, name="zorder"),
    url(r'^morder/(?P<library_id>\d+)/(?P<gen_id>[a-z0-9]+)/$', views.mail_order, name="mail_order"),
    url(r'^mbaorder/$', views.mba_orders, name="mba_orders"),
    url(r'^mbaorder/copy/$', views.mba_order_copy, name="mba_order_copy"),
    url(r'^mbaorder/delivery/$', views.mba_order_delivery, name="mba_order_delivery"),
    url(r'^mbaorder/delete/(?P<order_id>[a-z0-9]+)/$', views.delete_order, name="mba_delete_order"),
)