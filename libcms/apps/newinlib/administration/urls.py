# -*- coding: utf-8 -*-
from django.conf.urls import *

import views

urlpatterns = patterns('',
    url(r'^$', views.index , name="index"),
    url(r'^items/$', views.items_list, name="items_list"),
    url(r'^items/create/$', views.create_item , name="create_item"),
    url(r'^items/edit/(?P<id>\d+)/$', views.edit_item, name="edit_item"),
    url(r'^items/delete/(?P<id>\d+)/$', views.delete_item, name="delete_item"),
)