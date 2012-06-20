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
#    page = get_object_or_404(Page, url_path=slug)
    page = Page.objects.get(url_path=slug)
    try:
        content = Content.objects.get(page=page, lang=cur_language[:2])
    except Content.DoesNotExist:
        content = None
    children = None

#    if not page.is_leaf_node():
#        children = list(Page.objects.filter(parent=page, public=True))
#        contents = Content.objects.filter(page__in=children, lang=cur_language[:2])
#        cd = {}
#        for child in children:
#            cd[child.id] = child
#
#        for contend_page in contents:
#            if contend_page.page_id in cd:
#                cd[contend_page.page_id].content = contend_page

    return render(request, 'pages/frontend/show.html', {
        'page': page,
        'content': content,
#        'children': children,
    })
