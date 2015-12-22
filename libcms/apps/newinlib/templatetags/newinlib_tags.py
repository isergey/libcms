# -*- coding: utf-8 -*-
from lxml import etree
from django.conf import settings
from django import template
from django.utils.translation import get_language
from ..models import Item, ItemContent
from ssearch.models import get_records
from common.xslt_transformers import xslt_transformer, xslt_marc_dump_transformer, xslt_bib_draw_transformer

register = template.Library()


@register.inclusion_tag('newinlib/tags/items_feed.html')
def last_items_feed(count=5):
    lang = 'ru'
    items_list = list(ItemContent.objects.prefetch_related('item').filter(item__publicated=True, lang=lang).order_by('-item__create_date')[:count])
    nd = {}
    for item in items_list:
        nd[item.item.id_in_catalog] = item

    # for item_content in items_contents:
    #     nd[item_content.item_id].item_content = item_content

    # if not items_contents:
    #     items_list = []
    #
    records_ids = []
    for items_lis in items_list:
        records_ids.append(items_lis.item.id_in_catalog)

    # records = []
    # print 'records_ids', records_ids
    for record in get_records(records_ids):
        item_content = nd.get(record.gen_id)
        print 'item_content', item_content
        if item_content:
            nd[record.gen_id].attrs = xml_doc_to_dict(record.content)
            print nd[record.gen_id].attrs
        # records.append({
        #     'id': record.gen_id,
        #     'content': xml_doc_to_dict(record.content),
        #     'title': getattr(nd.get(record.gen_id), 'title', '')
        # })

    # for record in records:
    #     print 'record', record.get('content').keys()
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
    # print records
    return ({
        'items_list': items_list,
        #        'main_item': main_item,
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
        #если поле пустое, пропускаем
        if not value: continue
        #        value = beautify(value)
        values = doc_dict.get(attrib, None)
        if not values:
            doc_dict[attrib] = [value]
        else:
            values.append(value)
    return doc_dict