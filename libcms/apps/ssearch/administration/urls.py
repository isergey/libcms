# coding: utf-8
from django.conf.urls import *
import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^statistics/$', views.statistics, name="statistics"),
    url(r'^upload/$', views.upload, name="upload"),
    url(r'^process/$', views.pocess, name="process"),
    url(r'^indexing/$', views.indexing, name="indexing"),
    url(r'^lr_indexing/$', views.local_records_indexing, name="local_records_indexing"),
    url(r'^fte/$', views.full_text_extract, name="fte"),
)