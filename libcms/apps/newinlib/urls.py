# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('',
    (r'^admin/', include('newinlib.administration.urls', namespace='administration')),
    (r'^', include('newinlib.frontend.urls', namespace='frontend')),

)

