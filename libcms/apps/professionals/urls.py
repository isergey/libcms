# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('',
    (r'^', include('professionals.frontend.urls', namespace='frontend')),
)

