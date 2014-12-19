# -*- coding: utf-8 -*-
from django.conf.urls import *
import views

urlpatterns = patterns(views,
    url(r'^$', views.index, name="index"),
    url(r'^create$', views.create, name="create"),
    url(r'^edit/(?P<poll_id>\d+)/$', views.edit, name="edit"),
    url(r'^delete/(?P<poll_id>\d+)/$', views.delete, name="delete"),

    url(r'^view/(?P<poll_id>\d+)/$', views.view, name="view"),
    url(r'^create/choice/(?P<poll_id>\d+)/$', views.create_choice, name="create_choice"),
    url(r'^edit/choice/(?P<choice_id>\d+)/$', views.edit_choice, name="edit_choice"),
    url(r'^delete/choice/(?P<choice_id>\d+)/$', views.delete_choice, name="delete_choice"),

)