# -*- coding: utf-8 -*-
from django.conf.urls import *
from frontend import urls as furls
from administration import urls as aurls

urlpatterns = patterns('',
    (r'^admin/', include(aurls, namespace='administration')),
    (r'^', include(furls, namespace='frontend')),

)
