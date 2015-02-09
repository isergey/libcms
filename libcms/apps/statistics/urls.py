# -*- coding: utf-8 -*-
from django.conf.urls import *
from .frontend import urls as furls
urlpatterns = patterns('',
    (r'^', include(furls, namespace='frontend')),
    #(r'^admin/', include('ssearch.administration.urls', namespace='administration')),
)

