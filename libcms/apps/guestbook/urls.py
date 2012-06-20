# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('',
    (r'^admin/', include('guestbook.administration.urls', namespace='administration')),
    (r'^', include('guestbook.frontend.urls', namespace='frontend')),

)

