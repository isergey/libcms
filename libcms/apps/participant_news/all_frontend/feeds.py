# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.translation import get_language
from participants.models import Library
from ..models import News



from django.contrib.syndication.views import Feed


class LatestEntriesFeed(Feed):
    title = u"Новости"
    description = u"Новостная лента"

    def get_object(self, request, library_code):
        library = get_object_or_404(Library, code=library_code)
        return library

    def title(self, library):
        return u'Новости %s' % library.name

    def items(self, library):
        return index(library)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.teaser

    def link(self, obj):
        return reverse('participant_news:frontend:index', args=[obj.code])

def index(library):
    news_list =  News.objects.filter(publicated=True, lang=get_language()[:2], library=library).order_by('-order', '-create_date')[:5]
    return news_list

