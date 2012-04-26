# -*- coding: utf-8 -*-

from django.utils.translation import get_language
from views import rss



from django.contrib.syndication.views import Feed


class LatestEntriesFeed(Feed):
    title = u"Поступления в сводный каталог и электронную коллекцию"
    link = "/ssearch/"
    description = u"Поступления в сводный каталог и электронную коллекцию"

    def items(self):
        return rss()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.title


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
