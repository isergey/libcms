# -*- coding: utf-8 -*-
from django.shortcuts import render, Http404
from django.utils import translation

from common.pagination import get_page
from ssearch.models import get_records
from .. import utils
from ..models import Item, ItemContent


def index(request):
    cur_language = translation.get_language()

    items_page = get_page(
        request,
        ItemContent.objects.prefetch_related('item')
            .filter(item__publicated=True, lang=cur_language)
            .order_by('-item__create_date')
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
