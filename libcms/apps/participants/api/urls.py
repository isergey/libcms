# -*- coding: utf-8 -*-
from django.conf.urls import *

import views

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    url(r'^auth_user/$', views.auth_user, name="auth_user"),
    url(r'^get_user_orgs/$', views.get_user_orgs, name="get_user_orgs"),
    url(r'^get_org/$', views.get_org, name="get_org"),
    url(r'^find_orgs/$', views.find_orgs, name="find_orgs"),
    url(r'^get_user/$', views.get_user, name="get_user"),
)
