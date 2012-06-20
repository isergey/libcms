# -*- coding: utf-8 -*-

from django.utils.translation import get_language
from news.models import News, NewsContent



from django.contrib.syndication.views import Feed


class LatestEntriesFeed(Feed):
    title = u"Новости"
    link = "/news/"
    description = u"Новостная лента"

    def items(self):
        return index()

    def item_title(self, item):
        return item.news_content.title

    def item_description(self, item):
        return item.news_content.teaser


def index():
    news_list =  News.objects.filter(publicated=True).exclude(type=2).order_by('-create_date')[:5]

    news_contents = list(NewsContent.objects.filter(news__in=list(news_list), lang=get_language()[:2]))

    t_dict = {}
    for news in news_list:
        t_dict[news.id] = {'news': news}

    for news_content in news_contents:
        t_dict[news_content.news_id]['news'].news_content = news_content

    return news_list

#def show(request, id):
#    cur_language = translation.get_language()
#    news = get_object_or_404(News, id=id)
#    try:
#        content = NewsContent.objects.get(news=news, lang=cur_language[:2])
#    except Content.DoesNotExist:
#        content = None
#
#    return render(request, 'news/frontend/show.html', {
#        'news': news,
#        'content': content
#    })
