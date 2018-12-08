# -*- coding: utf-8 -*-
from django.shortcuts import render, Http404
from django.utils import translation

from common.pagination import get_page
from ssearch.models import get_records
from .. import utils
from ..models import Item, ItemContent


def index(request):
    cur_language = translation.get_language()
    # items_page = get_page(request, Item.objects.filter(publicated=True).order_by('-create_date'), per_page=10)
    # item_contents = list(ItemContent.objects.select_related('item').filter(item__in=list(items_page.object_list), lang=cur_language))
    #
    # t_dict = {}
    # for item in items_page.object_list:
    #     t_dict[item.id] = {
    #         'item': item
    #     }
    #
    # for item_content in item_contents:
    #     t_dict[item_content.item_id]['item'].item_content = item_content
    #
    # nd = {}
    #
    # for item in item_contents:
    #     nd[item.item.id_in_catalog] = item
    #
    # records_ids = []
    #
    # for items_lis in item_contents:
    #     records_ids.append(items_lis.item.id_in_catalog)
    #
    # records = get_records(records_ids)
    # for record in records:
    #     doc = utils.xml_doc_to_dict(record.content)
    #     item = nd.get(record.gen_id)
    #     print(item)
    #     if item is not None:
    #         item.item.cover = doc.get('cover', [''])[0]

    items_page = get_page(
        request,
        ItemContent.objects.prefetch_related('item')
            .filter(item__publicated=True, lang=cur_language).order_by('-item__create_date')
    )

    nd = {}

    for item in items_page.object_list:
        nd[item.item.id_in_catalog] = item

    records_ids = []
    for items_lis in items_page.object_list:
        records_ids.append(items_lis.item.id_in_catalog)

    records = get_records(records_ids)
    for record in records:
        doc = utils.xml_doc_to_dict(record.content)
        item = nd.get(record.gen_id)
        if item is not None:
            item.cover = doc.get('cover', [''])[0]

    return render(request, 'newinlib/frontend/list.html', {
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
