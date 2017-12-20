# -*- coding: utf-8 -*-
from django.conf.urls import *
from .administration import urls as aurls
from .frontend import urls as furls


urlpatterns = patterns('',
    (r'^admin/', include(aurls, namespace='administration')),
    (r'^', include(furls, namespace='frontend')),

)

