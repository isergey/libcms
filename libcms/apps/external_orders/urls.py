# -*- coding: utf-8 -*-
from django.conf.urls import *
from .frontend import urls

urlpatterns = patterns(
    '',
    (r'^', include(urls, namespace='frontend')),

)

