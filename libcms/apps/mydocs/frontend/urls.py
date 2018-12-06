# -*- coding: utf-8 -*-


from django.conf.urls import *
import views
urlpatterns = patterns(views,
    url(r'^$', views.index , name="index"),
    url(r'^save/$', views.save , name="save"),
    url(r'^delete/(?P<id>\d+)/$', views.delete , name="delete"),
    url(r'^lists/create/$', views.create_list , name="create_list"),
    url(r'^lists/(?P<id>\d+)/change/$', views.change_list , name="change_list"),
    url(r'^lists/(?P<id>\d+)/delete/$', views.delete_list , name="delete_list"),
)
