# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^', include('ssearch.frontend.urls', namespace='frontend')),
    (r'^admin/', include('ssearch.administration.urls', namespace='administration')),
)

