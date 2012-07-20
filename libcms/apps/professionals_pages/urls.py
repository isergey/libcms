# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('',
    (r'^admin/', include('professionals_pages.administration.urls', namespace='administration')),
    (r'^', include('professionals_pages.frontend.urls', namespace='frontend')),

)

