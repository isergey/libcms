# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('',
    (r'^admin/', include('apps.gallery.administration.urls', namespace='administration')),
    (r'^', include('apps.gallery.frontend.urls', namespace='frontend')),

)

