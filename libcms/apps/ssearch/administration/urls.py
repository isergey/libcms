# coding: utf-8
from django.conf.urls import *
import views

urlpatterns = patterns('',
    url(r'^$', views.initial, name='initial'),
    url(r'^upload/$', views.upload, name="upload"),
    url(r'^process/$', views.pocess, name="process"),
    url(r'^indexing/(?P<slug>[a-z]+)/$', views.indexing, name="indexing"),
)