# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponse

def index(request):
    return HttpResponse(u'Profile')