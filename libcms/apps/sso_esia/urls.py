# -*- coding: utf-8 -*-
from django.conf.urls import *
import views
urlpatterns = patterns(
    '',
    url(r'^$', views.index, name="index"),
    url(r'^redirect$', views.redirect_from_idp, name="redirect_from_ip"),
    url(r'^grs$', views.create_or_update_ruslan_user, name="create_or_update_ruslan_user"),
    #url(r'^login/$', views.login, name="login"),
)

