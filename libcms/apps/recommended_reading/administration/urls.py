# -*- coding: utf-8 -*-
from django.conf.urls import *
from . import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^items/$', views.items, name='items'),
    url(r'^items/(?P<id>\d+)/$', views.detail, name='detail'),
    url(r'^items/(?P<item_id>\d+)/attachments/upload/$', views.upload_attachment, name='upload_attachment'),
    url(r'^items/(?P<item_id>\d+)/attachments/delete/(?P<id>\d+)/$', views.delete_attachment, name='delete_attachment'),
    url(r'^items/create/$', views.create_item, name='create_item'),
    url(r'^items/change/(?P<id>\d+)/$', views.change_item, name="change_item"),
    url(r'^items/delete/(?P<id>\d+)/$', views.delete_item, name="delete_item"),
)