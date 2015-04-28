# -*- coding: utf-8 -*-
from django.conf.urls import *
import views

urlpatterns = patterns(views,
    url(r'^user/$', views.user, name="user"),
)
