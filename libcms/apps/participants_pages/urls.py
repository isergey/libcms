# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('',
    (r'^admin/', include('participants_pages.administration.urls', namespace='administration')),
    (r'^', include('participants_pages.frontend.urls', namespace='frontend')),

)

