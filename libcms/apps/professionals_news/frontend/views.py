# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import translation
from django.utils.translation import get_language
from django.db.models import Q
from guardian.decorators import permission_required_or_403
from common.pagination import get_page
from ..models import News, NewsContent



@permission_required_or_403('professionals_news.can_views_prof_news')
def index(request):
    news_page = get_page(request, News.objects.filter(publicated=True).order_by('-create_date'))

    news_contents = list(NewsContent.objects.filter(news__in=list(news_page.object_list), lang=get_language()[:2]))

    t_dict = {}
    for news in news_page.object_list:
        t_dict[news.id] = {'news': news}

    for news_content in news_contents:
        t_dict[news_content.news_id]['news'].news_content = news_content

    return render(request, 'professionals_news/frontend/list.html', {
        'news_list': news_page.object_list,
        'news_page': news_page,
        })

@permission_required_or_403('professionals_news.can_views_prof_news')
def show(request, id):
    cur_language = translation.get_language()
    try:
        news = News.objects.get(id=id)
    except News.DoesNotExist:
        raise Http404()

    try:
        content = NewsContent.objects.get(news=news, lang=cur_language[:2])
    except Content.DoesNotExist:
        content = None

    return render(request, 'professionals_news/frontend/show.html', {
        'news': news,
        'content': content
    })
