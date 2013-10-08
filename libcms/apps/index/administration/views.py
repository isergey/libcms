# coding: utf-8
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
@login_required
def index(request):
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'backend_base.html')
    else:
        return  HttpResponseForbidden(u'403 Access forbidden')