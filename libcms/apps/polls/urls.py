# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('',
    (r'^admin/', include('polls.administration.urls', namespace='administration')),
    (r'^', include('polls.frontend.urls', namespace='frontend')),

)

