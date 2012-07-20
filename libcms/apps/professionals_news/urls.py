# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('',
    (r'^admin/', include('professionals_news.administration.urls', namespace='administration')),
    (r'^', include('professionals_news.frontend.urls', namespace='frontend')),

)

