# -*- coding: utf-8 -*-
from django.conf.urls import *

import views

urlpatterns = patterns('',
    url(r'^$', views.index , name="index"),
    url(r'^detail/(?P<id>\d+)/$', views.detail, name="detail"),
    url(r'^add_user/(?P<id>\d+)/$', views.add_user, name="add_user"),
    url(r'^list/$', views.list, name="list"),
    url(r'^list/(?P<parent>\d+)/$', views.list, name="list"),
    url(r'^create/$', views.create , name="create"),
    url(r'^create/(?P<parent>\d+)/$', views.create , name="create"),
    url(r'^edit/(?P<id>\d+)/$', views.edit, name="edit"),
    url(r'^delete/(?P<id>\d+)/$', views.delete, name="delete"),
    url(r'^library_types/list/$', views.library_types_list, name="library_types_list"),
    url(r'^library_types/create/$', views.library_type_create, name="library_type_create"),
    url(r'^library_types/edit/(?P<id>\d+)/$', views.library_type_edit, name="library_type_edit"),
    url(r'^library_types/delete/(?P<id>\d+)/$', views.library_type_delete, name="library_type_delete"),

    url(r'^district/list/$', views.district_list, name="district_list"),
    url(r'^district/create/$', views.district_create, name="district_create"),
    url(r'^district/edit/(?P<id>\d+)/$', views.district_edit, name="district_edit"),
    url(r'^district/delete/(?P<id>\d+)/$', views.district_delete, name="district_delete"),
)
