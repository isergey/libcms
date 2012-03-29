# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
import views
urlpatterns = patterns(views,
    url(r'^$', views.index , name="index"),
    url(r'^branches/(?P<id>\d+)/$', views.branches , name="branches"),
    url(r'^detail/(?P<id>\d+)/$', views.detail , name="detail"),
)
