# -*- coding: utf-8 -*-
from django.conf.urls import *
import views
urlpatterns = patterns(views,
    url(r'^$', views.index , name="index"),
    url(r'^ask$', views.ask , name="ask"),
    url(r'^detail/(?P<id>\d+)/', views.detail , name="detail"),
    url(r'^detail/print/(?P<id>\d+)/', views.printed_detail , name="printed_detail"),
    url(r'^my/', views.my_questions , name="my_questions"),
#    url(r'^(?P<slug>[/_\-0-9A-Za-z]+)/$', views.show , name="show"),
)

