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
    url(r'^pages/permissions/(?P<id>\d+)/$', views.page_permissions, name="page_permissions"),
    url(r'^pages/assign_page_permissions/(?P<id>\d+)/$', views.assign_page_permissions, name="assign_page_permissions"),
    url(r'^pages/up/(?P<id>\d+)/$', views.page_up , name="page_up"),
    url(r'^pages/down/(?P<id>\d+)/$', views.page_down , name="page_down"),
)