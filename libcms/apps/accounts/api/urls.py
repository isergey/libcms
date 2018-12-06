# -*- coding: utf-8 -*-
from django.conf.urls import *
import views

urlpatterns = patterns(views,
    url(r'^user/$', views.user, name="user"),
    url(r'^get_user/$', views.get_user, name="get_user"),
    url(r'^check_password/$', views.check_password, name="check_password"),
)
