# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import translation
from django.utils.translation import to_locale, get_language

from ..models import Page, Content
from participants.models import Library

def index(request, library_id):
    library = get_object_or_404(Library, id=library_id)
    cur_language = translation.get_language()
    page = get_object_or_404(Page, slug='index')
    try:
        content = Content.objects.get(page=page, lang=cur_language[:2])
    except Content.DoesNotExist:
        content = None

    return render(request, 'participants_pages/frontend/show.html', {
        'page': page,
        'content': content,
        'library':library
    })

def show(request, library_id, slug):
    library = get_object_or_404(Library, id=library_id)
    cur_language = translation.get_language()
    page = get_object_or_404(Page, url_path=slug)
    try:
        content = Content.objects.get(page=page, lang=cur_language[:2])
    except Content.DoesNotExist:
        content = None

    return render(request, 'participants_pages/frontend/show.html', {
        'page': page,
        'content': content,
        'library':library
    })
