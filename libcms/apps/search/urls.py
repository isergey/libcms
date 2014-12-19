# -*- coding: utf-8 -*-
from django.conf.urls import *


urlpatterns = patterns('',
    (r'^admin/', include('apps.search.administration.urls', namespace='administration')),
    (r'^', include('apps.search.frontend.urls', namespace='frontend')),

)

