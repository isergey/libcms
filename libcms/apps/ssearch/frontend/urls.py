# coding: utf-8
from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^detail/(?P<gen_id>[A-Za-z]+)/$', views.detail, name='detail'),
)