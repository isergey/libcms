# -*- coding: utf-8 -*-
from django.conf.urls import *
import views
urlpatterns = patterns(views,
    url(r'^$', views.index , name="index"),
    url(r'^(?P<slug>[/_\-0-9A-Za-z]+)/$', views.show , name="show"),
)
