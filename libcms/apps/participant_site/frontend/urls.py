# -*- coding: utf-8 -*-
from django.conf.urls import *
import views
urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    # url(r'^site/$', views.site, name="site"),
    # url(r'^site/news/$', views.site_news_list, name="site_news_list"),
    # url(r'^site/news/(?P<id>\d+)/$', views.site_news_detail, name="site_news_detail"),
    # url(r'^site/about/$', views.site_page, name="site_page"),
)