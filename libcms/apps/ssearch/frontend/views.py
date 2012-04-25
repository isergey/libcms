# -*- coding: utf-8 -*-
import hashlib
import datetime
from lxml import etree
import sunburnt
import simplejson
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.core.cache import cache
from django.shortcuts import render, HttpResponse, get_object_or_404, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import  QueryDict
from ..models import Record, Ebook, SavedRequest

from common.xslt_transformers import xslt_transformer, xslt_marc_dump_transformer, xslt_bib_draw_transformer
## на эти трансформаторы ссылаются из других модулей
#xslt_root = etree.parse('libcms/xsl/record_in_search.xsl')
#xslt_transformer = etree.XSLT(xslt_root)
#
#xslt_marc_dump = etree.parse('libcms/xsl/marc_dump.xsl')
#xslt_marc_dump_transformer = etree.XSLT(xslt_marc_dump)
#
#xslt_bib_draw = etree.parse('libcms/xsl/full_document.xsl')
#xslt_bib_draw_transformer = etree.XSLT(xslt_bib_draw)






attr_map = {
    'text': {
        'order': 1,
        'attr': u'text_t',
        'title':u'Везде',
        'display': True,
        },
    'title': {
        'order': 2,
        'attr': u'title_t',
        'title':u'Заглавие',
        'display': True,
        },
    'author': {
        'order': 3,
        'attr': u'author_t',
        'title':u'Автор',
        'display': True,
        },
    'subject-heading': {
        'order': 4,
        'attr': u'subject-heading_t',
        'title':u'Тематика',
        'display': True,
        },
    'date-of-publication': {
        'order': 5,
        'attr': u'date-of-publication_dt',
        'title':u'Год публикации',
        'display': True,
        },
    'code-language':{
        'order': 6,
        'attr': u'code-language_t',
        'title':u'Язык',
        'display': False,
        },
    'isbn': {
        'order': 7,
        'attr': u'isbn_t',
        'title':u'ISBN',
        'display': True,
        },
    'issn': {
        'order': 8,
        'attr': u'issn_t',
        'title':u'ISSN',
        'display': True,
        },
    'content-type': {
        'order': 9,
        'attr': u'content-type_t',
        'title':u'Тип содержания',
        'display': False,
        },
    'full-text': {
        'order': 10,
        'attr': u'full-text',
        'title':u'Полный текст',
        'display': False,
        },
    'fond': {
        'order': 11,
        'attr': u'fond_t',
        'title':u'Фонд',
        'display': False,
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
    u'tom': {
        'attr': u'tom_f',
        'order': 'asc',
        },
    }

def _make_search_attrs(catalog):
    search_attrs = []
    for attr in attr_map:

        if not attr_map[attr].get('display', False):
            continue
        search_attrs.append({
            'title': attr_map[attr].get('title', attr),
            'value': attr,
            'order': attr_map[attr].get('order', 1000),
            })

    if catalog == u'ebooks':
        search_attrs.append({
            'title':attr_map['full-text']['title'],
            'value':attr_map['full-text']['attr'],
            'order':attr_map['full-text']['order'],
            })
    print catalog
    search_attrs.sort(key=lambda x: x['order'])
    return search_attrs


def index(request, catalog=None):
    q = request.GET.get('q', None)
    fq = request.GET.get('fq', None)
    if not q and not fq:
        return init_search(request, catalog)
    else:
        return search(request, catalog)



def init_search(request, catalog=None):
    search_attrs = _make_search_attrs(catalog)
    return render(request, 'ssearch/frontend/index.html', {
        'search_attrs': search_attrs
    })



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
origin_types = ['ts', 'ss', 'dts', 'f']

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


def search(request, catalog=None):

    search_attrs = _make_search_attrs(catalog)

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
    except IndexError:
        return HttpResponse(u'Некорректный набор атрибутов')


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
    solr_searcher = solr_searcher.highlight(fields=['full-text'])

    exclude_kwargs = {}

    if catalog == u'sc2':
        exclude_kwargs = {'system-catalog_s':u"ebooks"}
        solr_searcher = solr_searcher.exclude(**exclude_kwargs)
    elif catalog == u'ebooks':
        exclude_kwargs = {'system-catalog_s':u"sc2"}
        solr_searcher = solr_searcher.exclude(**exclude_kwargs)
    else:
        pass

#    print search_attrs

    for sort_attr in sort_attrs:
        if sort_attr['order'] == 'desc':
            solr_searcher = solr_searcher.sort_by(u'-' + sort_attr['attr'])
        else:
            solr_searcher = solr_searcher.sort_by( sort_attr['attr'])

    # ключ хеша зависит от языка
    terms_facet_hash = hashlib.md5(unicode(terms) + u'_facets_' + get_language() + u'#'.join(exclude_kwargs.values())).hexdigest()


    facets = cache.get(terms_facet_hash, None)
    if not facets:
        solr_searcher = solr_searcher.facet_by(field=facet_fields, limit=30, mincount=1)

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

    star = False
    for term in terms[:search_deep_limit]:
        key = term.keys()[0]
        value = term[key]
        if value.strip() == '*':
            star = True

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
    log_search_request({'attr': new_key, 'value': value},catalog)
    if catalog == u'ebooks' and len(search_breadcumbs) > 1 and star:
        return HttpResponse(u'Нельзя использовать * при вложенных запросах в каталоге содержащий полный текст')
    json_search_breadcumbs = simplejson.dumps(search_breadcumbs, ensure_ascii=False)
#    print docs
    return render(request, 'ssearch/frontend/index.html', {
        'docs': docs,
        'results_page': results_page,
        'facets': facets,
        'search_breadcumbs':search_breadcumbs,
        'sort':sort,
        'search_statisics':search_statisics,
        'search_request': json_search_breadcumbs,
        'search_attrs': search_attrs
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
        'gen_id': gen_id,
    })

@login_required
def saved_search_requests(request):

    saved_requests = SavedRequest.objects.filter(user=request.user)
    srequests = []
    for saved_request in saved_requests:
        try:
            srequests.append({
                'saved_request':saved_request,
                'breads':simplejson.loads(saved_request.search_request),
            })
        except simplejson.JSONDecodeError:
            srequests.append({
                'saved_request':saved_request,
                'breads': None
                })

    return render(request, 'ssearch/frontend/saved_request.html', {
        'srequests': srequests,
    })


def save_search_request(request):
    if not request.user.is_authenticated():
        return HttpResponse(u'Вы должны быть войти на портал', status=401)
    search_request =  request.GET.get('srequest', None)
    if SavedRequest.objects.filter(user=request.user).count() > 500:
        return HttpResponse(u'{"status": "error", "error": "Вы достигли максимально разрешенного количества запросов"}')

    SavedRequest(user=request.user, search_request=search_request).save()
    return HttpResponse(u'{"status": "ok"}')

def delete_search_request(request, id):
    if not request.user.is_authenticated():
        return HttpResponse(u'Вы должны быть войти на портал', status=401)
    sr = get_object_or_404(SavedRequest, user=request.user, id=id)
    sr.delete()
    return HttpResponse(u'{"status": "ok"}')




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







#import pymorphy
import uuid
from ..models import SearchRequestLog
#morph = pymorphy.get_morph(settings.PYMORPHY_CDB_DICTS, 'cdb')
def log_search_request(request, catalog):

    def clean_term(term):
        """
        Возвращает кортеж из ненормализованног и нормализованного терма
        """
        terms = term.strip().lower().split()
        nn_term = u' '.join(terms)

        n_terms = []
        #нормализация
        for t in terms:
            n_term = t #morph.normalize(t.upper())
            if isinstance(n_term, set):
                n_terms.append(n_term.pop().lower())
            elif isinstance(n_term, unicode):
                n_terms.append(n_term.lower())

        n_term = u' '.join(n_terms)
        return (nn_term, n_term)


    search_request_id =  uuid.uuid4().hex
    term_groups = []


    term = request.get('value', None)
    if term:
        forms = clean_term(term)
        term_groups.append({
            'nn': forms[0],
            'n':  forms[1],
            'use': request.get('attr',u'not defined'),

            })


    for group in term_groups:
        SearchRequestLog(
            catalog=catalog,
            search_id=search_request_id,
            use=group['use'],
            normalize=group['n'],
            not_normalize=group['nn'],
        ).save()