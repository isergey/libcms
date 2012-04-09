# -*- coding: utf-8 -*-
from django.conf.urls import *
import views
urlpatterns = patterns(views,
    url(r'^$', views.index , name="index"),
    url(r'^show/$', views.show , name="show"),
    url(r'^book/$', views.book , name="book"),
    url(r'^draw/$', views.draw , name="draw"),
)
