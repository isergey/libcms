# -*- coding: utf-8 -*-
from django.conf.urls import *
import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^advanced/$', views.advanced_search, name="advanced_search"),
    url(r'^help/$', views.help, name="help"),
    # url(r'^$', views.index, name='advanced_search'),
     url(r'^ftr/$', views.full_text_redirect, name="full_text_redirect"),
    url(r'^income/$', views.income, name="income"),
    url(r'^facets/$', views.facets, name='facets'),
    url(r'^facets/more/$', views.more_facets, name='more_facets'),
    url(r'^facets/more/explore/$', views.facet_explore, name='facet_explore'),
    url(r'^detail/$', views.detail, name='detail'),
    url(r'^raw/$', views.load_raw_record, name='load_raw_record'),
    url(r'^requests/$', views.saved_search_requests, name='saved_search_requests'),
    url(r'^requests/save/$', views.save_search_request, name='save_search_request'),
    url(r'^requests/delete/(?P<id>\d+)/$', views.delete_search_request, name='delete_search_request'),
)

