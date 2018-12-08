# -*- coding: utf-8 -*-
from django import template
from django.conf import settings

from ssearch.models import get_records
from ..models import ItemContent
from .. import utils
register = template.Library()


@register.inclusion_tag('newinlib/tags/items_feed.html')
def last_items_feed(count=5):
    lang = 'ru'
    items_list = list(ItemContent.objects.prefetch_related('item').filter(item__publicated=True, lang=lang).order_by(
        '-item__create_date')[:count])
    nd = {}

    for item in items_list:
        nd[item.item.id_in_catalog] = item

    records_ids = []
    for items_lis in items_list:
        records_ids.append(items_lis.item.id_in_catalog)

    records = get_records(records_ids)
    for record in records:
        doc = utils.xml_doc_to_dict(record.content)
        item = nd.get(record.gen_id)
        if item is not None:
            item.cover = doc.get('cover', [''])[0]
    # saved_documents = mydocs_models.SavedDocument.objects.values('gen_id').filter(gen_id__in=records_ids)
    #
    # for saved_document in saved_documents:
    #     item_content = nd.get(saved_document.get('gen_id'))
    #     if item_content:
    #         item_content.in_favorite = True
    #
    # for record in get_records(records_ids):
    #     item_content = nd.get(record.gen_id)
    #     if item_content:
    #         nd[record.gen_id].attrs = xml_doc_to_dict(record.content)

    return ({
        'items_list': items_list,
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL
    })



