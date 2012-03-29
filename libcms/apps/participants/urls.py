# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

#from participants.api.views import auth_user

urlpatterns = patterns('',
    (r'^', include('participants.frontend.urls', namespace='frontend')),
    (r'^admin/', include('participants.administration.urls', namespace='administration')),
)


