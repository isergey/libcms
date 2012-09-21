# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.utils import translation
from django.utils.translation import get_language
from django.db.models import Q
from common.pagination import get_page
from ..models import Item, ItemContent



def index(request):
    items_page = get_page(request, Item.objects.filter(publicated=True).order_by('-create_date'), per_page=10)

#    item_contents = list(ItemContent.objects.filter(item__in=list(items_page.object_list), lang=get_language()[:2]))
    item_contents = list(ItemContent.objects.filter(item__in=list(items_page.object_list), lang='ru'))

    t_dict = {}
    for item in items_page.object_list:
        t_dict[item.id] = {
            'item': item
        }

    for item_content in item_contents:
        t_dict[item_content.item_id]['item'].item_content = item_content

    return render(request, 'newinlib/frontend/list.html', {
        'items_list': items_page.object_list,
        'items_page': items_page,
        })

def show(request, id):
    cur_language = translation.get_language()
    try:
        item = Item.objects.get(id=id)
    except Item.DoesNotExist:
        raise Http404()

    try:
#        content = ItemContent.objects.get(item=item, lang=cur_language[:2])
        content = ItemContent.objects.get(item=item, lang='ru')

    except ItemContent.DoesNotExist:
        content = None

    return render(request, 'newinlib/frontend/show.html', {
        'item': item,
        'content': content
    })

