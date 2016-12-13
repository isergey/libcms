# -*- coding: utf-8 -*-
from django.conf.urls import *
import views

urlpatterns = patterns(
    '',
    url(r'^/$', views.index, name='index'),
    url(r'^order/(?P<org_code>[/_\-0-9A-Za-z]+)/(?P<record_gen_id>[A-Za-z]+)$', views.order, name='order'),
)

