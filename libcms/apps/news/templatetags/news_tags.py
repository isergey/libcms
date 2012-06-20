# -*- coding: utf-8 -*-
from django import template
from django.utils.translation import get_language
from news.models import News, NewsContent

register = template.Library()
@register.inclusion_tag('news/tags/news_feed.html')
def news_feed(count=5):
    news_list = list(News.objects.filter(publicated=True).exclude(type=1).order_by('-create_date')[:count])
    lang=get_language()[:2]
    news_contents = NewsContent.objects.filter(news__in=news_list, lang=lang)
    nd = {}
    for news in news_list:
        nd[news.id] = news

    for news_content in news_contents:
        nd[news_content.news_id].news_content = news_content

    if not news_contents:
        news_list = []
    return ({
        'news_list': news_list,
    })

