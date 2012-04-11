# -*- coding: utf-8 -*-
import hashlib
import datetime
from lxml import etree
import sunburnt
from django.conf import settings
from django.utils.translation import get_language
from django.core.cache import cache
from django.shortcuts import render, HttpResponse, get_object_or_404, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import  QueryDict
from ssearch.models import Record, Ebook

xslt_root = etree.parse('libcms/xsl/record_in_search.xsl')
xslt_transformer = etree.XSLT(xslt_root)

xslt_marc_dump = etree.parse('libcms/xsl/marc_dump.xsl')
xslt_marc_dump_transformer = etree.XSLT(xslt_marc_dump)

xslt_bib_draw = etree.parse('libcms/xsl/full_document.xsl')
xslt_bib_draw_transformer = etree.XSLT(xslt_bib_draw)

def index(request):
    q = request.GET.get('q', None)
    fq = request.GET.get('fq', None)
    if not q and not fq:
        return init_search(request)
    else:
        return search(request)



def init_search(request):
    return render(request, 'ssearch/frontend/index.html')




attr_map = {
    u'author': {
        'attr': u'author_t'
    },
    u'title': {
        'attr': u'title_t'
    },
    u'subject-heading': {
        'attr': u'subject-heading_t'
    },
    u'date-of-publication': {
        'attr': u'date-of-publication_dt'
    },
    u'code-language':{
        'attr': u'code-language_t'
    },
    u'isbn': {
        'attr': u'isbn_t'
    },
    u'issn': {
        'attr': u'issn_t'
    },
    u'text': {
        'attr': u'text_t'
    },
    u'content-type': {
        'attr': u'content-type_t'
    },
    u'fond': {
        'attr': u'fond_t'
    },
}


sort_attr_map = {
    u'author': {
        'attr': u'author_ts',
        'order': 'asc',
    },
    u'title': {
        'attr': u'title_ts',
        'order': 'asc',
    },
    u'date-of-publication': {
        'attr': u'date-of-publication_dts',
        'order': 'desc',
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

class WrongSearchAttribute(Exception): pass

def terms_constructor(attrs, values):
    terms = []
    for i, q in enumerate(values):
        attr = attr_map.get(attrs[i], None)
        if not attr:
            raise WrongSearchAttribute()
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
    search_deep_limit = 5 # ограничение вложенных поисков
    solr = sunburnt.SolrInterface(settings.SOLR['host'])

    qs = request.GET.getlist('q', [])
    attrs = request.GET.getlist('attr', [])
    sort = request.GET.getlist('sort', [])

    sort_attrs = []


    for sort_attr in sort:
        sort_attr = sort_attr_map.get(sort_attr, None)
        if not sort_attr:
            continue

        sort_attrs.append({
            'attr':sort_attr['attr'],
            'order':sort_attr.get('order', 'asc')
        })


    fqs = request.GET.getlist('fq', [])
    fattrs = request.GET.getlist('fattr', [])

    in_founded = request.GET.get('in_founded', None)


    terms = []
    try:
        if in_founded or sort:
            terms += terms_constructor(fattrs, fqs)
        terms += terms_constructor(attrs, qs)
    except WrongSearchAttribute:
        return HttpResponse(u'Задан непрвильный атрибут поиска')


    query = None

    for term in terms[:search_deep_limit]:
        # если встретилось поле с текстом, то через OR ищем аналогичное с постфиксом _ru
        morph_query = None
        attr = term.keys()[0]
        if len(attr) > 2 and attr[-2:] == '_t':
            morph_query = solr.Q(**{attr + '_ru': term.values()[0]})

        if not query:
            if morph_query:
                query = solr.Q(solr.Q(**term) | morph_query)
            else:
                query = solr.Q(**term)
        else:
            if morph_query:
                query = query & solr.Q(solr.Q(**term) | morph_query)
            else:
                query = query & solr.Q(**term)




    facet_fields = ['author_sf', 'content-type_t','date-of-publication_dtf', 'subject-heading_sf', 'code-language_t', 'fond_sf' ]
    solr_searcher = solr.query(query)
    for sort_attr in sort_attrs:
        if sort_attr['order'] == 'desc':
            solr_searcher = solr_searcher.sort_by(u'-' + sort_attr['attr'])
        else:
            solr_searcher = solr_searcher.sort_by( sort_attr['attr'])

    # ключ хеша зависит от языка
    terms_facet_hash = hashlib.md5(unicode(terms) + u'_facets_' + get_language()).hexdigest()


    facets = cache.get(terms_facet_hash, None)
    if not facets:
        solr_searcher = solr_searcher.facet_by(field=facet_fields, limit=20, mincount=1)

    solr_searcher = solr_searcher.field_limit("id")
    paginator = Paginator(solr_searcher, 20) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        results_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        results_page = paginator.page(paginator.num_pages)

#    print dir(results_page.object_list)
    search_statisics = {
        'num_found': results_page.object_list.result.numFound,
        'search_time': "%.3f" % (int(results_page.object_list.QTime) / 1000.0)
    }

    docs = []

    if not facets:
        facets = replace_doc_attrs(results_page.object_list.facet_counts.facet_fields)
        cache.set(terms_facet_hash,facets)


    for row in results_page.object_list:
        docs.append(replace_doc_attrs(row))


    doc_ids = []
    for doc in docs:
        doc_ids.append(doc['id'])

    records_dict = {}
    records =  list(Ebook.objects.using('records').filter(gen_id__in=doc_ids))
    records +=  list(Record.objects.using('records').filter(gen_id__in=doc_ids))
    for record in records:
        records_dict[record.gen_id] = xml_doc_to_dict(record.content)

    for doc in docs:
        doc['record'] = records_dict.get(doc['id'])

    search_breadcumbs = []
    query_dict = None

    for term in terms[:search_deep_limit]:
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
        search_breadcumbs.append({
            'attr': new_key,
            'value': value,
            'href': query_dict.urlencode()
        })


    return render(request, 'ssearch/frontend/index.html', {
        'docs': docs,
        'results_page': results_page,
        'facets': facets,
        'search_breadcumbs':search_breadcumbs,
        'sort':sort,
        'search_statisics':search_statisics
    })


def detail(request, gen_id):
#    shards=['http://localhost:8983/solr','http://localhost:8982/solr']
#    mlt_docs = []
#    for shard in shards:
#        solr = sunburnt.SolrInterface(shard)
#        mlt_query = solr.query(id=gen_id).mlt(['author_t','subject-heading_t','title_t'],mindf='1', mintf='1')
##        mlt_query = solr.query(id=gen_id).mlt(["text_t"],mindf='1', mintf='1')
#        mlt_results = mlt_query.execute().more_like_these
#        if gen_id in mlt_results:
#            for doc in  mlt_results[gen_id].docs:
#                mlt_docs.append(doc)
#
#    doc_ids = []
#    for doc in mlt_docs:
#        doc_ids.append(doc['id'])
#
#    records_dict = {}
#    records =  list(Ebook.objects.using('records').filter(gen_id__in=doc_ids))
#    records +=  list(Record.objects.using('records').filter(gen_id__in=doc_ids))
#    for record in records:
#        records_dict[record.gen_id] = xml_doc_to_dict(record.content)
#
#    for doc in mlt_docs:
#        doc['record'] = records_dict.get(doc['id'])

    try:
        record = Record.objects.using('records').get(gen_id=gen_id)
    except Record.DoesNotExist:
        try:
            record = Ebook.objects.using('records').get(gen_id=gen_id)
        except Record.DoesNotExist:
            raise Http404()




    doc_tree = etree.XML(record.content)

    bib_tree = xslt_bib_draw_transformer(doc_tree)
    marct_tree = xslt_marc_dump_transformer(doc_tree)
    bib_dump =  etree.tostring(bib_tree, encoding='utf-8')
    marc_dump =  etree.tostring(marct_tree, encoding='utf-8')
    doc_tree_t = xslt_transformer(doc_tree)
    doc = doc_tree_to_dict(doc_tree_t)
    holders = doc.get('holders', list())
    if holders:
        # оставляем уникальных держателей
        doc['holders'] = list(set(holders))

    return render(request, 'ssearch/frontend/detail.html', {
        'doc_dump': bib_dump.replace('<b/>',''),
        'marc_dump': marc_dump,
        'doc': doc,
#        'mlt_docs': mlt_docs,
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