# -*- encoding: utf-8 -*-
from django.conf.urls import *

import views

urlpatterns = patterns('',
    url(r'^$', views.index , name="index"),
    url(r'^albums/$', views.albums_list, name="albums_list"),
    url(r'^albums/images/(?P<id>\d+)/$', views.album_view, name="album_view"),
    url(r'^albums/upload/(?P<id>\d+)/$', views.album_upload, name="album_upload"),
    url(r'^albums/create/$', views.album_create, name="album_create"),
    url(r'^albums/edit/(?P<id>\d+)/$', views.album_edit, name="album_edit"),
    url(r'^albums/delete/(?P<id>\d+)/$', views.album_delete, name="album_delete"),

    url(r'^albums/images/edit/(?P<id>\d+)/$', views.image_edit, name="image_edit"),
    url(r'^albums/images/delete/(?P<id>\d+)/$', views.image_delete, name="image_delete"),

    url(r'^albums/images/up/(?P<id>\d+)/$', views.image_up, name="image_up"),
    url(r'^albums/images/down/(?P<id>\d+)/$', views.image_down, name="image_down"),

    url(r'^albums/images/image_to_begin/(?P<id>\d+)/$', views.image_to_begin, name="image_to_begin"),
    url(r'^albums/images/image_to_end/(?P<id>\d+)/$', views.image_to_end, name="image_to_end"),

)