# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from urt.models import LibReader

@login_required
def index(request):
    try:
        lib_reader = LibReader.objects.get(user=request.user)
    except LibReader.DoesNotExist:
        lib_reader = None
    return render(request, 'personal/frontend/index.html', {
        'lib_reader': lib_reader
    })