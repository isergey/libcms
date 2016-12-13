# -*- coding: utf-8 -*-
from django.conf.urls import *
from .frontend import urls as furls
from .api import urls as api_urls

urlpatterns = (
    url(r'^api/', include(api_urls, namespace='api')),
    url(r'^', include(furls, namespace='frontend')),
)

