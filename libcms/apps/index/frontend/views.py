# coding: utf-8
from django.shortcuts import render, HttpResponse

def index(request):
    return render(request, 'index/frontend/index.html')

