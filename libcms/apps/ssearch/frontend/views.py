# -*- coding: utf-8 -*-
import datetime
from lxml import etree
import sunburnt
from django.shortcuts import render, HttpResponse, get_object_or_404, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import  QueryDict
from ssearch.models import Record

xslt_root = etree.parse('libcms/xsl/record_in_search.xsl')
xslt_transformer = etree.XSLT(xslt_root)

xslt_marc_dump = etree.parse('libcms/xsl/marc_dump.xsl')
xslt_marc_dump_transformer = etree.XSLT(xslt_marc_dump)

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
    'content-type': {
        'attr':'content-type_t'
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

def terms_constructor(attrs, values):
    terms = []
    for i, q in enumerate(values):
        attr = attr_map.get(attrs[i], None)
        if not attr:
            return HttpResponse(u'Wrong search attribute')
        else:
            attr = attr['attr']

        split_attr = attr.split('_')
        if len(split_attr) > 1 and split_attr[-1] in resolvers:
            try:
                value = resolvers[split_attr[-1]](q)
                if type(value) == tuple or type(value) == list:
                    q = value[0]
                else:
                    q = value
            except ValueError:
                continue

        terms.append({attr: q})
    return terms

def search(request):
    solr = sunburnt.SolrInterface('http://127.0.0.1:8983/solr/')

    qs = request.GET.getlist('q', [])
    attrs = request.GET.getlist('attr', [])

    fqs = request.GET.getlist('fq', [])
    fattrs = request.GET.getlist('fattr', [])

    in_founded = request.GET.get('in_founded', None)

    terms = []
    if in_founded:
        terms += terms_constructor(fattrs, fqs)

    terms += terms_constructor(attrs, qs)


    print terms
    query = None

    for term in terms:
        if not query:
            query = solr.Q(**term)
        else:
            query = query & solr.Q(**term)



    facets = ['author_sf', 'content-type_t','date-of-publication_dtf', 'subject-heading_sf' ]
    paginator = Paginator(solr.query(query).facet_by(field=facets, limit=20, mincount=1), 20) # Show 25 contacts per page

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


    doc_ids = []
    for doc in docs:
        doc_ids.append(doc['id'])

    records_dict = {}
    records =  list(Record.objects.using('records').filter(gen_id__in=doc_ids))
    from time import time as t
    s  = t()
    for record in records:
        records_dict[record.gen_id] = xml_doc_to_dict(record.content)
    print t() - s

    for doc in docs:
        doc['record'] = records_dict.get(doc['id'])

    search_breadcumbs = []
    query_dict = None
    for term in terms:



        key = term.keys()[0]
        value = term[key]
        if type(value) == datetime.datetime:
            value = unicode(value.year)

        new_key = key.split('_')[0]
        if not query_dict:
            query_dict = QueryDict('q=' + value + '&attr='+new_key).copy()
        else:
            query_dict.getlist('q').append(value)
            query_dict.getlist('attr').append(new_key)
#        print 'q', query_dict.getlist('q')
#        print 'attr', query_dict.getlist('attr')
#        print query_dict.urlencode()
        search_breadcumbs.append({
            'attr': new_key,
            'value': value,
            'href': query_dict.urlencode()
        })

    print search_breadcumbs
    return render(request, 'ssearch/frontend/index.html', {
        'docs': docs,
        'results_page': results_page,
        'facets': facets,
        'search_breadcumbs':search_breadcumbs
    })


def detail(request, gen_id):
    print request
    try:
        record = Record.objects.using('records').get(gen_id=gen_id)
    except Record.DoesNotExist:
        raise Http404()

    doc_tree = etree.XML(record.content)
    marct_tree = xslt_marc_dump_transformer(doc_tree)
    marc_dump =  etree.tostring(marct_tree, encoding='utf-8')
    doc_tree_t = xslt_transformer(doc_tree)
    doc = doc_tree_to_dict(doc_tree_t)

    holders = doc.get('holders', list())
    if holders:
        # оставляем уникальных держателей
        doc['holders'] = list(set(holders))

    return render(request, 'ssearch/frontend/detail.html', {
        'marc_dump': marc_dump,
        'doc': doc
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
        value = beautify(value)
        values = doc_dict.get(attrib, None)
        if not values:
            doc_dict[attrib] = [value]
        else:
            values.append(value)
    return doc_dict

def beautify(value):
    value = unicode(value).replace(u'..', u"%#dot#dot#")\
    .replace(u'.:', u"%#dot#colon#")\
    .replace(u'.;', u"%#dot#semicolon#")\
    .replace(u'.!', u"%#dot#screamer#")\
    .replace(u'.?', u"%#dot#question#")

    value = value.replace(u':', u": ")\
    .replace(u'.', u". ")\
    .replace(u',', u", ")\
    .replace(u';', u"; ")\
    .replace(u')', u") ")

    value = value.replace(u"%#dot#dot#",'. ' )\
    .replace(u"%#dot#colon#",u'.: ' )\
    .replace(u"%#dot#semicolon#", u'.; ')\
    .replace(u"%#dot#screamer#",u'.! ' )\
    .replace(u"%#dot#question#" , u'.? ')

    return value