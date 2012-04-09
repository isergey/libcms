# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('',
    (r'^admin/', include('events.administration.urls', namespace='administration')),
    (r'^', include('events.frontend.urls', namespace='frontend')),

)

