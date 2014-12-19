# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('',
    (r'^admin/', include('apps.polls.administration.urls', namespace='administration')),
    (r'^', include('apps.polls.frontend.urls', namespace='frontend')),

)

