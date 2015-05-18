# -*- coding: utf-8 -*-
from django.conf.urls import *

import views

urlpatterns = patterns('',
    url(r'^$', views.index , name="index"),
    url(r'^detail/(?P<id>\d+)/$', views.detail, name="detail"),
    url(r'^department/(?P<id>\d+)/$', views.department_detail, name="department_detail"),
    url(r'^department/create/(?P<library_id>\d+)/$', views.create_department, name="create_department"),
    url(r'^department/edit/(?P<id>\d+)/$', views.edit_department, name="edit_department"),
    url(r'^department/delete/(?P<id>\d+)/$', views.delete_department, name="delete_department"),
    url(r'^get_departments/$', views.get_departments, name="get_departments"),
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
    url(r'^managed_districts/$', views.managed_districts, name="managed_districts"),


    url(r'^lib_users/$', views.library_user_list, name="library_user_list"),
    url(r'^lib_users/(?P<library_id>\d+)/create/$', views.add_library_user, name="add_library_user"),
    url(r'^lib_users/edit/(?P<id>\d+)/$', views.edit_library_user, name="edit_library_user"),
    url(r'^lib_users/delete/(?P<id>\d+)/$', views.delete_library_user, name="delete_library_user"),
    url(r'^find_library_by_district/$', views.find_library_by_district, name="find_library_by_district"),
    url(r'^load_libs/$', views.load_libs, name="load_libs"),

)
