# -*- coding: utf-8 -*-
from django.conf.urls import *

import views

urlpatterns = patterns('',
    url(r'^$', views.index , name="index"),
    url(r'^pages/$', views.pages_list, name="pages_list"),
    url(r'^pages/(?P<parent>\d+)/$', views.pages_list, name="pages_list"),
    url(r'^pages/create/$', views.create_page , name="create_page"),
    url(r'^pages/create/(?P<parent>\d+)/$', views.create_page , name="create_page"),
    url(r'^pages/edit/(?P<id>\d+)/$', views.edit_page, name="edit_page"),
    url(r'^pages/delete/(?P<id>\d+)/$', views.delete_page, name="delete_page"),
    url(r'^pages/content/create/(?P<page_id>\d+)/$', views.create_page_content, name="create_page_content"),
    url(r'^pages/content/edit/(?P<page_id>\d+)/(?P<lang>[a-z]{2})$', views.edit_page_content, name="edit_page_content"),
)