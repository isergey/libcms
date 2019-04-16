# -*- coding: utf-8 -*-
from django.conf.urls import *
import views
urlpatterns = patterns(
    '',
    url(r'^$', views.index, name="index"),
    url(r'^redirect/$', views.redirect_from_idp, name="redirect_from_ip"),
    url(r'^ask/(?P<id>\d+)$', views.ask_for_exist_reader, name="ask_for_exist_reader"),
    url(r'^register/(?P<id>\d+)$', views.register_new_user, name="register_new_user"),
    # url(r'^grs$', views.grs_test, name="create_or_update_ruslan_user"),
    #url(r'^login/$', views.login, name="login"),
)

