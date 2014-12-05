# -*- coding: utf-8 -*-
from django.conf.urls import *
from administration import urls
urlpatterns = patterns('',
    (r'^admin/', include(urls, namespace='administration')),
    #(r'^', include('participant_menu.frontend.urls', namespace='frontend')),

)

