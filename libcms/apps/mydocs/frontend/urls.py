# -*- coding: utf-8 -*-


from django.conf.urls import *
import views
urlpatterns = patterns(views,
    url(r'^$', views.index , name="index"),
    url(r'^save/$', views.save , name="save"),
    url(r'^delete/(?P<id>\d+)/$', views.delete , name="delete"),
)
