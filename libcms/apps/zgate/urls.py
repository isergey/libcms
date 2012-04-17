# -*- coding: utf-8 -*-
from django.conf.urls import *
import views

urlpatterns = patterns('zgate.views',
    url(r'^(?P<catalog_id>\d+)/$', views.index, name="zgate_index"),
    url(r'^(?P<catalog_id>\d+)/order/$', views.draw_order, name="draw_order"),
    url(r'^(?P<catalog_id>\d+)/help/$', views.help, name="zgate_help"),

    url(r'^s/(?P<slug>[-_\w]+)/$', views.index, name="zgate_slug_index"),
    url(r'^s/(?P<slug>[-_\w]+)/order/$', views.draw_order, name="draw_order"),
    url(r'^s/(?P<slug>[-_\w]+)/help/$', views.help, name="zgate_slug_help"),

    url(r'^requests/$', views.saved_requests_list, name="zgate_saved_requests"),
    url(r'^requests/go/(?P<request_id>\d+)/$', views.make_saved_request, name="zgate_make_saved_request"),
    url(r'^requests/delete/(?P<request_id>\d+)/$', views.delete_saved_request, name="zgate_delete_saved_request"),

    url(r'^documents/$', views.saved_document_list, name="zgate_saved_document_list"),
    #url(r'^documents/search/(?P<document_id>\d+)/$', 'search_document', name="zgate_search_saved_document"),
    url(r'^documents/save/$', views.save_document, name="zgate_save_document"),
    url(r'^documents/load/$', views.load_documents, name="zgate_load_saved_documents"),
    url(r'^documents/delete/(?P<document_id>\d+)/$', views.delete_saved_document, name="zgate_delete_saved_document"),
)

