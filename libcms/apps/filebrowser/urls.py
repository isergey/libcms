# -*- coding: utf-8 -*-
from django.conf.urls import *


urlpatterns = patterns('',
    (r'^admin/', include('filebrowser.administration.urls', namespace='administration')),
)

