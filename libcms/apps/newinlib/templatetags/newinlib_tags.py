# -*- coding: utf-8 -*-
from django.conf import settings
from django import template
from django.utils.translation import get_language
from ..models import Item, ItemContent

register = template.Library()
@register.inclusion_tag('newinlib/tags/items_feed.html')
def last_items_feed(count=5):
    items_list = list(Item.objects.filter(publicated=True).order_by('-create_date')[:count])
#    lang=get_language()[:2]
    lang='ru'
    items_contents = ItemContent.objects.filter(item__in=items_list, lang=lang)
    nd = {}
    for item in items_list:
        nd[item.id] = item

    for item_content in items_contents:
        nd[item_content.item_id].item_content = item_content

    if not items_contents:
        items_list = []

    # Находим анонс помеченный как главный. Если такового нет, то делаем главным последний анонс
#    main_item = None
#    main_items = list(Item.objects.filter(main=True).order_by('-create_date')[0:1])
#    if main_items:
#        main_item = main_items[0]
#        main_item_contents = list(ItemContent.objects.filter(item=main_item, lang=lang)[0:1])
#        if main_item_contents:
#            main_item.item_content = main_item_contents[0]
#    else:
#        if items_list:
#            main_item = items_list[0]
#            items_list = items_list[1:]
    return ({
        'items_list': items_list,
#        'main_item': main_item,
        'MEDIA_URL': settings.MEDIA_URL
    })

