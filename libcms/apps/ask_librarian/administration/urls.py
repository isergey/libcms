# -*- coding: utf-8 -*-
from django.conf.urls import *

import views

urlpatterns = patterns('',
    url(r'^$', views.index , name="index"),
    url(r'^categories/$', views.categories_list, name="categories_list"),
    url(r'^categories/create/$', views.category_create, name="category_create"),
    url(r'^categories/(?P<parent>\d+)/create/$', views.category_create, name="category_create"),
    url(r'^categories/edit/(?P<id>\d+)/$', views.category_edit, name="category_edit"),
    url(r'^categories/delete/(?P<id>\d+)/$', views.category_delete, name="category_delete"),
    url(r'^categories/up/(?P<id>\d+)/$', views.category_up, name="category_up"),
    url(r'^categories/down/(?P<id>\d+)/$', views.category_down, name="category_down"),

    url(r'^questions/$', views.questions_list, name="questions_list"),
    url(r'^processes/assign_to_manager/(?P<question_id>\d+)/$', views.assign_to_manager, name="assign_to_manager"),
    url(r'^processes/my/$', views.questions_list, name="questions_processes", kwargs={'my':True}),
    url(r'^questions/question_answer/(?P<id>\d+)/$', views.question_answer, name="question_answer"),
    url(r'^questions/to_process/(?P<id>\d+)/$', views.questions_to_process, name="questions_to_process"),
    url(r'^questions/detail/(?P<id>\d+)/$', views.question_detail, name="question_detail"),
    url(r'^questions/edit/(?P<id>\d+)/$', views.question_edit, name="question_edit"),
    url(r'^questions/delete/(?P<id>\d+)/$', views.question_delete, name="question_delete"),

#    url(r'^categories/up/(?P<id>\d+)/$', views.category_up, name="category_up"),
#    url(r'^categories/down/(?P<id>\d+)/$', views.category_down, name="category_down"),
#    url(r'^pages/(?P<parent>\d+)/$', views.pages_list, name="pages_list"),
#    url(r'^pages/create/$', views.create_page , name="create_page"),
#    url(r'^pages/create/(?P<parent>\d+)/$', views.create_page , name="create_page"),
#    url(r'^pages/edit/(?P<id>\d+)/$', views.edit_page, name="edit_page"),
#    url(r'^pages/delete/(?P<id>\d+)/$', views.delete_page, name="delete_page"),
#    url(r'^pages/content/create/(?P<page_id>\d+)/$', views.create_page_content, name="create_page_content"),
#    url(r'^pages/content/edit/(?P<page_id>\d+)/(?P<lang>[a-z]{2})$', views.edit_page_content, name="edit_page_content"),
)