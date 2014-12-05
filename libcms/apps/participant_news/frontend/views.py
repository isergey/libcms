# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, Http404
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required

from common.pagination import get_page
from participants.models import Library
from ..models import News


def index(request, library_code):
    library = get_object_or_404(Library, code=library_code)
    lang=get_language()[:2]
    news_page = get_page(request, News.objects.filter(library=library, publicated=True, lang=lang).order_by('-order', '-create_date'))


    return render(request, 'participant_news/frontend/list.html', {
        'library': library,
        'news_list': news_page.object_list,
        'news_page': news_page,
    })

def show(request, library_code, id):
    lang=get_language()[:2]
    try:
        news = News.objects.get(id=id, lang=lang)
    except News.DoesNotExist:
        raise Http404()
    return render(request, 'participant_news/frontend/show.html', {
        'news': news,
        'library': news.library
    })

