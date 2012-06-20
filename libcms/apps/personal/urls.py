# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('',
    (r'^', include('personal.frontend.urls', namespace='frontend')),
)

