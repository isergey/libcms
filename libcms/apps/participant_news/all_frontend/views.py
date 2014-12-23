# -*- coding: utf-8 -*-
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, Http404
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required
import forms
from common.pagination import get_page
from ..models import News, NewsImage


def index(request):
    filter_form = forms.NewsFilter(request.GET)
    lang=get_language()[:2]
    q = Q(publicated=True, lang=lang)
    if filter_form.is_valid():
        library = filter_form.cleaned_data['library']
        if library:
            libs = [library.id]
            for item in list(library.get_children().values('id')):
                libs.append(item['id'])
            q = q & Q(library__in=libs)
    news_page = get_page(request, News.objects.select_related('library').filter(q).order_by('-create_date'))
    return render(request, 'participant_news/all_frontend/list.html', {
        'news_list': news_page.object_list,
        'news_page': news_page,
        'filter_form': filter_form
    })


def show(request, id):
    lang=get_language()[:2]
    try:
        news = News.objects.get(id=id, lang=lang)
    except News.DoesNotExist:
        raise Http404()

    news_images = NewsImage.objects.filter(news=news)
    return render(request, 'participant_news/frontend/show.html', {
        'news': news,
        'news_images': news_images,
        'library': news.library
    })

