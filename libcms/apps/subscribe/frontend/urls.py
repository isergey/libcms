# -*- coding: utf-8 -*-
from django.conf.urls import *

import views


urlpatterns = patterns(
    '',
    url(r'^$', views.index, name="index"),
    url(r'^(?P<id>[0-9]+)/$', views.subscription_detail, name="subscription_detail"),
    url(r'^(?P<id>[0-9]+)/subscribe/$', views.subscribe, name="subscribe"),
    url(r'^(?P<id>[0-9]+)/unsubscribe/$', views.unsubscribe, name="unsubscribe"),
    url(r'^slr/$', views.send_letters_req, name="send_letters_req"),
    url(r'^ser/$', views.send_emails_req, name="send_emails_req"),
)
