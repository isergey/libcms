# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponse
from ..models import Content



def index(request):
    robots_txt = Content.objects.all()[:1]
    return HttpResponse(robots_txt, content_type='text/plain')

