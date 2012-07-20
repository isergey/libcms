# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('',
    (r'^', include('robots_txt.frontend.urls', namespace='frontend')),

)

