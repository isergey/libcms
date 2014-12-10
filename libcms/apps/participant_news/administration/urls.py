# -*- coding: utf-8 -*-
from django.conf.urls import *

import views


urlpatterns = patterns('',
    url(r'^$', views.index , name="index"),
    url(r'^news/$', views.news_list, name="news_list"),
    url(r'^news/create/$', views.create_news , name="create_news"),
    url(r'^news/edit/(?P<id>\d+)/$', views.edit_news, name="edit_news"),
    url(r'^news/delete/(?P<id>\d+)/$', views.delete_news, name="delete_news"),

    url(r'^news/(?P<id>\d+)/images/$', views.news_images, name="news_images"),
    url(r'^news/(?P<id>\d+)/images/create/$', views.create_news_image, name="create_news_image"),
    url(r'^news/(?P<id>\d+)/images/edit/(?P<image_id>\d+)/$', views.edit_news_image, name="edit_news_image"),
    url(r'^news/(?P<id>\d+)/images/delete/(?P<image_id>\d+)/$', views.delete_news_image, name="delete_news_image"),
)