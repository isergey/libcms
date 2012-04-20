# -*- coding: utf-8 -*-
from django.conf.urls import *


urlpatterns = patterns('ask_librarian.views',
    url(r'^$', 'index', name="index"),
    url(r'^ask_question/$', 'ask_question', name="ask_question"),
    url(r'^question/(?P<id>\d+)/$', 'question_detail', name="question_detail"),
    url(r'^by_category/(?P<id>\d+)/$', 'by_category', name="by_category"),
    url(r'^available_managers/$', 'available_managers', name="available_managers"),
)


urlpatterns += patterns('ask_librarian.administration_views',
    url(r'^administration/$', 'index', name="admin_index"),
    url(r'^administration/questions/$', 'questions', name="admin_questions"),
    url(r'^administration/questions/list/$', 'questions_list', name="admin_questions_list"),
    url(r'^administration/questions/(?P<id>\d+)/$', 'questions_detail', name="admin_questions_detail"),
    url(r'^administration/managers/$', 'managers', name="admin_managers"),
)

