# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import translation
from django.utils.translation import to_locale, get_language

from pages.models import Page, Content


def index(request):
    cur_language = translation.get_language()
    page = get_object_or_404(Page, slug='index')
    try:
        content = Content.objects.get(page=page, lang=cur_language[:2])
    except Content.DoesNotExist:
        content = None

    return render(request, 'pages/frontend/show.html', {
        'page': page,
        'content': content
    })

def show(request, slug):
    cur_language = translation.get_language()
    page = get_object_or_404(Page, url_path=slug)
    try:
        content = Content.objects.get(page=page, lang=cur_language[:2])
    except Content.DoesNotExist:
        content = None

    return render(request, 'pages/frontend/show.html', {
        'page': page,
        'content': content
    })
