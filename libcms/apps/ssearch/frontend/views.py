# -*- coding: utf-8 -*-
import sunburnt
from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    q = request.GET.get('q', None)

    if not q:
        return init_search(request)
    else:
        return search(request)



def init_search(request):
    return render(request, 'ssearch/frontend/index.html')




attr_map = {
    'author': {
        'attr':'author_t'
    },
    'title': {
        'attr':'title_t'
    },
    'subject-heading': {
        'attr':'subject-heading_t'
    },
    'date-of-publication': {
        'attr':'date-of-publication_dt'
    },
    'isbn': {
        'attr':'isbn_t'
    },
    'issn': {
        'attr':'issn_t'
    },
    'anywhere': {
        'attr':'anywhere_t'
    },
}

#reverse_attr_map = {}
#
#def do_reverse_attr_map():
#    for key in attr_map:
#        reverse_attr_map[attr_map[key]['attr']] = {'attr':key}
#
#do_reverse_attr_map()
#print reverse_attr_map

def replace_doc_attrs(doc):
    """
    Вырезает из названия атрибута указатель на тип. Список типов в переменной reserved_types
    """
    reserved_types = [
        't', # текст
        's', # фраза
        'dt', # дата время
#        'ts', # сортировка текста
#        'ss', # --//--
#        'dts', # --//--
        'tf', # фасет текста
        'sf', # --//--
        'dtf', # --//--
    ]
    new_doc = {}
    for key in doc.keys():
        split_key = key.split('_')
        if len(split_key) > 1 and split_key[-1] in reserved_types:
            new_doc[split_key[0]] = doc[key]
        else:
            new_doc[key] = doc[key]
    return new_doc

from ..common import resolve_date
# распознование типа
resolvers = {
    'dt': resolve_date,
    'dts': resolve_date,
    'dtf': resolve_date,
    }
# тип поля, которое может быть только одно в документе
origin_types = ['ts', 'ss', 'dts']

def search(request):
    solr = sunburnt.SolrInterface('http://127.0.0.1:8983/solr/')
    q = request.GET.get('q', None)
    attr = request.GET.get('attr', None)

    if not attr or attr not in attr_map:
        attr = 'anywhere'

    attr = attr_map[attr]['attr']

    split_attr = attr.split('_')
    if len(split_attr) > 1 and split_attr[-1] in resolvers:
        try:
            value = resolvers[split_attr[-1]](q)
            if type(value) == tuple or type(value) == list:
                q = value[0]
            else:
                q = value
        except ValueError:
            split_attr[0] = 'anywhere'



    kwarg = {
        attr_map[split_attr[0]]['attr']: q
    }

    facets = ['author_sf', 'content-type_t','date-of-publication_dtf' ]
    paginator = Paginator(solr.query(**kwarg).facet_by(field=facets, limit=20, mincount=1), 30) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        results_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        results_page = paginator.page(paginator.num_pages)


    docs = []

    facets = replace_doc_attrs(results_page.object_list.facet_counts.facet_fields)
    for row in results_page.object_list:
        docs.append(replace_doc_attrs(row))

    return render(request, 'ssearch/frontend/index.html', {
        'docs': docs,
        'results_page': results_page,
        'facets': facets
    })