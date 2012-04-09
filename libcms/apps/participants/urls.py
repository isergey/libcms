# -*- coding: utf-8 -*-
from django.conf.urls import *


urlpatterns = patterns('',
    (r'^api/', include('participants.api.urls', namespace='api')),
    (r'^admin/', include('participants.administration.urls', namespace='administration')),
    (r'^', include('participants.frontend.urls', namespace='frontend')),
)


