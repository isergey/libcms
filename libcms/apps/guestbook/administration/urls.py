# -*- coding: utf-8 -*-
from django.conf.urls import *

import views

urlpatterns = patterns('',
    url(r'^$', views.index , name="index"),
    url(r'^feedbacks/list/$', views.feedbacks_list , name="feedbacks_list"),
    url(r'^feedbacks/edit/(?P<id>\d+)/$', views.edit_feedback , name="edit_feedback"),
    url(r'^feedbacks/delete/(?P<id>\d+)/$', views.delete_feedback , name="delete_feedback"),
#    url(r'^news/$', views.news_list, name="news_list"),
#    url(r'^news/create/$', views.create_news , name="create_news"),
#    url(r'^news/edit/(?P<id>\d+)/$', views.edit_news, name="edit_news"),
#    url(r'^news/delete/(?P<id>\d+)/$', views.delete_news, name="delete_news"),
)