# -*- coding: utf-8 -*-
from django.conf.urls import *
from administration import urls as aurls

urlpatterns = patterns('',
    (r'^admin/', include(aurls, namespace='administration')),
)
