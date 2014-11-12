# coding: utf-8
from django.shortcuts import render

def index(request):
    return render(request, 'index/frontend/index.html')

def site(request):
    return render(request, 'index/frontend/org_site.html')

def site_page(request):
    return render(request, 'index/frontend/org_page.html')

def site_news_list(request):
    return render(request, 'index/frontend/org_news_list.html')

def site_news_detail(request, id):
    return render(request, 'index/frontend/org_news_detail.html')