# -*- coding: utf-8 -*-
from django.conf.urls import *
#from django.contrib.auth.views import  login, logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
import views
urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    url(r'^link/$', views.link, name="link"),
)
