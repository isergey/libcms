# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('',
    (r'^', include('accounts.frontend.urls', namespace='frontend')),
    (r'^api/', include('accounts.api.urls', namespace='api')),
    (r'^admin/', include('accounts.administration.urls', namespace='administration')),
)

