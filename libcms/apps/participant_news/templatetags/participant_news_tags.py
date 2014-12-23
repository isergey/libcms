# -*- coding: utf-8 -*-
from django.conf import settings
from django import template
from django.utils.translation import get_language
from django.core.cache import cache
from ..models import News

register = template.Library()
@register.inclusion_tag('participant_news/tags/news_feed.html')
def participant_news_feed(library_id, count=10):
    lang = get_language()[:2]
    cache_key = 'participant_news_feed' + 'p1' + lang + str(library_id) + str(count)
    news_list = cache.get(cache_key, [])
    if not news_list:
        news_list = list(News.objects.select_related('library').filter(publicated=True, lang=lang, library_id=library_id).order_by('-order', '-create_date')[:count])
        cache.set(cache_key, news_list)
    return ({
        'news_list': news_list,
        'MEDIA_URL': settings.MEDIA_URL,
    })


@register.inclusion_tag('participant_news/tags/all_news_feed.html')
def participant_all_news_feed(count=10):
    lang = get_language()[:2]
    cache_key = 'participant_news_feed' + 'p1' + lang + str(count)
    news_list = cache.get(cache_key, [])
    if not news_list:
        news_list = list(News.objects.select_related('library').filter(publicated=True, lang=lang).order_by('-create_date')[:count])
        cache.set(cache_key, news_list)
    return ({
        'news_list': news_list,
        'MEDIA_URL': settings.MEDIA_URL,
    })

