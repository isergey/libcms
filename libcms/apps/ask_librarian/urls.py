# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('',
    (r'^admin/', include('ask_librarian.administration.urls', namespace='administration')),
    (r'^', include('ask_librarian.frontend.urls', namespace='frontend')),

)

