# -*- coding: utf-8 -*-
from lxml import etree
from django.conf import settings
from django import template
from django.utils.translation import get_language
from ..models import Item, ItemContent
from ssearch.models import get_records
from mydocs import models as mydocs_models
from libcms.libs.common.xslt_transformers import xslt_transformer, xslt_marc_dump_transformer, xslt_bib_draw_transformer

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

    saved_documents = mydocs_models.SavedDocument.objects.values('gen_id').filter(gen_id__in=records_ids)

    for saved_document in saved_documents:
        item_content = nd.get(saved_document.get('gen_id'))
        if item_content:
            item_content.in_favorite = True

    for record in get_records(records_ids):
        item_content = nd.get(record.gen_id)
        if item_content:
            nd[record.gen_id].attrs = xml_doc_to_dict(record.content)

    return ({
        'items_list': items_list,
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL
    })


def xml_doc_to_dict(xmlstring_doc):
    doc_tree = etree.XML(xmlstring_doc)
    doc_tree_t = xslt_transformer(doc_tree)
    return doc_tree_to_dict(doc_tree_t)


def doc_tree_to_dict(doc_tree):
    doc_dict = {}
    for element in doc_tree.getroot().getchildren():
        attrib = element.attrib['name']
        value = element.text
        # если поле пустое, пропускаем
        if not value: continue
        #        value = beautify(value)
        values = doc_dict.get(attrib, None)
        if not values:
            doc_dict[attrib] = [value]
        else:
            values.append(value)
    return doc_dict
