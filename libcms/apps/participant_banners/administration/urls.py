# -*- coding: utf-8 -*-
from django.conf.urls import *

import views

urlpatterns = patterns('',
    url(r'^create/$', views.create, name="create"),
    url(r'^edit/(?P<id>[0-9]+)/$', views.edit, name="edit"),
    url(r'^toggle_active/(?P<id>[0-9]+)/$', views.toggle_active, name="toggle_active"),
    url(r'^bind_to_children_orgs/(?P<id>[0-9]+)/$', views.bind_to_children_orgs, name="bind_to_children_orgs"),
    url(r'^unbind_to_children_orgs/(?P<id>[0-9]+)/$', views.unbind_to_children_orgs, name="unbind_to_children_orgs"),
    url(r'^delete/(?P<id>[0-9]+)/$', views.delete, name="delete"),

    url(r'^$', views.index, name="index"),
    url(r'^(?P<lang>[a-z]+)/$', views.index, name="index"),
)