# -*- coding: utf-8 -*-
from django.conf.urls import *
from .administration import urls as aurls

urlpatterns = (
    url(r'^admin/', include(aurls, namespace='administration')),

)

