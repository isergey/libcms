# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
import views
urlpatterns = patterns(views,
    url(r'^$', views.index , name="index"),
    url(r'^branches/(?P<code>[/_\-0-9A-Za-z]+)/$', views.branches , name="branches"),
    # в этом вызове id передается в GET
    url(r'^branches/$', views.branches , name="branches"),
    url(r'^detail/(?P<code>[/_\-0-9A-Za-z]+)/$', views.detail , name="detail"),
)
