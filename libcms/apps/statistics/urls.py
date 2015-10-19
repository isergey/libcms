# -*- coding: utf-8 -*-
from django.conf.urls import *
from .frontend import urls as furls
from .api import urls as aurls

urlpatterns = patterns('',
                       (r'^', include(furls, namespace='frontend')),
                       (r'^api/', include(aurls, namespace='api')),
                       # (r'^admin/', include('ssearch.administration.urls', namespace='administration')),
                       )
