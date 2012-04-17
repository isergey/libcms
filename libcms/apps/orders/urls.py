# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('',
    (r'^', include('orders.frontend.urls', namespace='frontend')),
    #    (r'^admin/', include('urt.administration.urls', namespace='administration')),
)

