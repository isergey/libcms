# -*- encoding: utf-8 -*-
from django.conf.urls import *

import views

urlpatterns = patterns('',
    url(r'^$', views.index , name="index"),
    url(r'^show/(?P<id>\d+)/$', views.album_view, name="album_view")
    )
