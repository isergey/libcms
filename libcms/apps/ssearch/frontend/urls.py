# coding: utf-8
from django.conf.urls import *
import views
import feeds
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^income/$', views.participant_income, name='participant_income'),
    url(r'^rss/$', feeds.LatestEntriesFeed(), name='rss'),
    url(r'^ecatalog/$', views.index, name='ecatalog', kwargs={'catalog':'sc2'}),
    url(r'^ecollection/$', views.index, name='ecollection', kwargs={'catalog':'ebooks'}),
    url(r'^detail/(?P<gen_id>[A-Za-z]+)/$', views.detail, name='detail'),
    url(r'^select/library/$', views.select_library, name='select_library'),
    url(r'^statictics/$', views.statictics, name='statictics'),
    url(r'^requests/$', views.saved_search_requests, name='saved_search_requests'),
    url(r'^requests/save/$', views.save_search_request, name='save_search_request'),
    url(r'^requests/delete/(?P<id>\d+)/$', views.delete_search_request, name='delete_search_request'),
    url(r'^print/(?P<gen_id>[A-Za-z]+)/$', views.to_print, name='to_print'),
    # url(r'^collections/$', views.get_collections, name='collections'),
)