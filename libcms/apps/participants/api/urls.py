# -*- coding: utf-8 -*-
from django.conf.urls import *

import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name="index"),
    url(r'^auth_user/$', views.auth_user, name="auth_user"),
    url(r'^get_user_orgs/$', views.get_user_orgs, name="get_user_orgs"),
    url(r'^get_org/$', views.get_org, name="get_org"),
    url(r'^find_orgs/$', views.find_orgs, name="find_orgs"),
    url(r'^get_user/$', views.get_user, name="get_user"),
    url(r'^export_orgs/$', views.export_orgs, name="export_orgs"),
    url(r'^export_ora_conns/$', views.export_ora_conns, name="export_ora_conns"),

    url(r'^user_organizations/$', views.user_organizations, name="user_organizations"),
    url(r'^personal_cabinet_links/$', views.personal_cabinet_links, name="personal_cabinet_links"),

)
