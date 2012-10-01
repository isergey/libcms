# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'personal/frontend/index.html')