# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('',
    (r'^', include('attacher.frontend.urls', namespace='frontend')),

)

