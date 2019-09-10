# coding=utf-8
import datetime
import hashlib
import json

import httplib2
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import QueryDict
from django.shortcuts import render, HttpResponse, get_object_or_404, Http404, urlresolvers
from django.utils.translation import get_language
from lxml import etree
from participants.models import Library
from participants.settings import PARTICIPANTS_SHOW_ORG_TYPES
import sunburnt
from libcms.libs.common.xslt_transformers import xslt_transformer, xslt_marc_dump_transformer, xslt_bib_draw_transformer
from .. import rusmarc_template
from ..common import resolve_date
from ..models import Record, SavedRequest, DetailAccessLog, get_records
from ..administration.views import record_to_indexing_doc

# # на эти трансформаторы ссылаются из других модулей
# xslt_root = etree.parse('libcms/xsl/record_in_search.xsl')
# xslt_transformer = etree.XSLT(xslt_root)
#
# xslt_marc_dump = etree.parse('libcms/xsl/marc_dump.xsl')
# xslt_marc_dump_transformer = etree.XSLT(xslt_marc_dump)
#
# xslt_bib_draw = etree.parse('libcms/xsl/full_document.xsl')
# xslt_bib_draw_transformer = etree.XSLT(xslt_bib_draw)

class RecordObject(object):
    id = None
    title = u''

    def get_absolute_url(self):
        return urlresolvers.reverse('ssearch:frontend:detail', args=[self.id])


def rss():
    now = datetime.date.today()
    seven_days_ago = now - datetime.timedelta(4)
    records_dicts = []
    records = list(Record.objects.using('records').filter(add_date__gte=seven_days_ago, add_date__lte=now))
    for record in records:
        rd = xml_doc_to_dict(record.content)
        ro = RecordObject()
        ro.id = record.gen_id
        ro.title = rd['title'][0]
        records_dicts.append(ro)
    return records_dicts


attr_map = {
    'text_t': {
        'order': 1,
        'attr': u'text_t',
        'title': u'Везде',
        'display': True,
    },
    'title_t': {
        'order': 2,
        'attr': u'title_t',
        'title': u'Заглавие',
        'display': True,
    },
    'author_t': {
        'order': 3,
        'attr': u'author_t',
        'title': u'Автор',
        'display': True,
    },
    'subject-heading_t': {
        'order': 4,
        'attr': u'subject-heading_t',
        'title': u'Тематика',
        'display': True,
    },
    'date-of-publication_dt': {
        'order': 5,
        'attr': u'date-of-publication_s',
        'title': u'Год публикации',
        'display': True,
    },
    'code-language': {
        'order': 6,
        'attr': u'code-language_t',
        'title': u'Язык',
        'display': False,
    },
    'isbn_t': {
        'order': 7,
        'attr': u'isbn_t',
        'title': u'ISBN',
        'display': True,
    },
    'issn_t': {
        'order': 8,
        'attr': u'issn_t',
        'title': u'ISSN',
        'display': True,
    },
    'content-type': {
        'order': 9,
        'attr': u'content-type_t',
        'title': u'Тип содержания',
        'display': False,
    },
    'full-text': {
        'order': 10,
        'attr': u'full-text',
        'title': u'Содержимое',
        'display': False,
    },
    'fond_sf': {
        'order': 11,
        'attr': u'fond_t',
        'title': u'Фонд',
        'display': False,
    },
    'dublet': {
        'order': 12,
        'attr': u'dublet_sf',
        'title': u'Ключ дублетности',
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
        'attr': u'date-of-publication_ss',
        'order': 'desc',
    },
    u'record-create-date': {
        'attr': u'record-create-date_dts',
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
            'title': attr_map['full-text']['title'],
            'value': attr_map['full-text']['attr'],
            'order': attr_map['full-text']['order'],
        })

    search_attrs.sort(key=lambda x: x['order'])
    return search_attrs


def index(request, catalog=None):
    library_code = request.GET.get('library', None)

    try:
        library = Library.objects.get(code=library_code)
    except Library.DoesNotExist:
        library = None

    q = request.GET.get('q', None)
    fq = request.GET.get('fq', None)
    if not catalog:
        catalog = request.GET.get('catalog', None)
    if not q and not fq:
        return init_search(request, catalog, library=library)
    else:
        return search(request, catalog, library=library)


def init_search(request, catalog=None, library=None):
    search_attrs = _make_search_attrs(catalog)
    stats = None
    if catalog == u'ebooks':
        stats = statictics()
    collections = get_collections()
    if stats:
        for collection in collections:
            collection['stats'] = stats['collections'].get(collection['persistant-number'][0], '')
    return render(request, 'ssearch/frontend/index.html', {
        'search_attrs': search_attrs,
        'stats': stats,
        'catalog': catalog,
        'collections': collections,
        'library': library
    })


def replace_doc_attrs(doc):
    """
    Вырезает из названия атрибута указатель на тип. Список типов в переменной reserved_types
    """
    #     reserved_types = [
    #         't', # текст
    #         's', # фраза
    #         'dt', # дата время
    # #        'ts', # сортировка текста
    # #        'ss', # --//--
    # #        'dts', # --//--
    #         'tf', # фасет текста
    #         'sf', # --//--
    #         'dtf', # --//--
    #     ]
    #     new_doc = {}
    #     for key in doc.keys():
    #         split_key = key.split('_')
    #         if len(split_key) > 1 and split_key[-1] in reserved_types:
    #             new_doc[split_key[0]] = doc[key]
    #         else:
    #             new_doc[key] = doc[key]
    return doc


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
        attr = attrs[i]
        terms.append({attr: q})
    return terms


def search(request, catalog=None, library=None):
    holders = []
    if library:
        holders.append(library.code)
        leaf_libraries = library.get_leafnodes()
        for leaf_library in leaf_libraries:
            holders.append(getattr(leaf_library, 'code'))
    facet_fields = [
        'fond_sf',
        'content_type_s',
        'author_sf',
        'subject-heading_sf',
        'date-of-publication_s',
        'code-language_t',
    ]

    search_attrs = _make_search_attrs(catalog)
    search_deep_limit = 5  # ограничение вложенных поисков
    solr_connection = httplib2.Http(disable_ssl_certificate_validation=True)
    solr = sunburnt.SolrInterface(settings.SOLR['host'], http_connection=solr_connection)

    qs = request.GET.getlist('q', [])
    attrs = request.GET.getlist('attr', [])
    sort = request.GET.getlist('sort', [])

    sort_attrs = []

    for sort_attr in sort:
        mapped_sort_attr = sort_attr_map.get(sort_attr, None)
        if not mapped_sort_attr:
            continue

        sort_attrs.append({
            'attr': mapped_sort_attr['attr'],
            'order': mapped_sort_attr.get('order', 'asc')
        })

    fqs = request.GET.getlist('fq', [])
    fattrs = request.GET.getlist('fattr', [])
    if fqs and fattrs and fqs[0] == u'*' and fattrs[0] == u'*':
        fqs = fqs[1:]
        fattrs = fattrs[1:]
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
    if len(terms) == 1 and 'text_t' in terms[0] and terms[0]['text_t'].strip() == '*':
        terms = [{u'*': u'*'}]

    if len(terms) > 1 and u'*' in terms[0][terms[0].keys()[0]].strip() == u'*':
        terms = terms[1:]
    try:
        for term in terms[:search_deep_limit]:
            # если встретилось поле с текстом, то через OR ищем аналогичное с постфиксом _ru
            morph_query = None
            attr = term.keys()[0]
            if len(attr) > 2 and attr[-2:] == '_t' and term.values()[0] != u'*':
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
                    term[attr] = "%s" % term[attr]

                    query = query & solr.Q(**term)
    except ValueError:
        return HttpResponse(u'Неверные параметры')

    if qs and attrs:
        log_search_request({'attr': attrs[0], 'value': qs[0]}, catalog, getattr(library, 'code', u''))

    # if holders:
    #     holders_query = solr.Q(**{'holder-sigla_s': holders[0]})
    #     for holder in holders[1:]:
    #         holders_query |= solr.Q(**{'holder-sigla_s': holder})
    #     query = query & holders_query

    filter_q = solr.Q()
    if holders:
        holders_q = solr.Q()

        for holder in holders:
            holders_q |= solr.Q(**{'system-holder_s': holder})

        filter_q &= holders_q

    # if holders:
    #     holders_query = solr.Q(**{'system-holder_s': holders[0]})
    #     for holder in holders[1:]:
    #         holders_query |= solr.Q(**{'system-holder_s': holder})
    #     query = query & holders_query

    solr_searcher = solr.query(query)
    if PARTICIPANTS_SHOW_ORG_TYPES:
        participant_types_q = solr.Q()
        for PARTICIPANTS_SHOW_ORG_TYPE in PARTICIPANTS_SHOW_ORG_TYPES:
            participant_types_q |= solr.Q(**{'org_type_s': PARTICIPANTS_SHOW_ORG_TYPE})

        filter_q &= participant_types_q

    solr_searcher = solr_searcher.filter(filter_q)

    if 'full-text' in request.GET.getlist('attr'):
        solr_searcher = solr_searcher.highlight(fields=['full-text'])

    exclude_kwargs = {}

    if catalog == u'sc2':
        exclude_kwargs = {'system-catalog_s': u"2"}
    elif catalog == u'ebooks':
        exclude_kwargs = {'system-catalog_s': u"4"}
    else:
        pass

    solr_searcher = solr_searcher.exclude(**exclude_kwargs)
    # solr_searcher = solr_searcher.filter(**{'date-of-publication_s': '2001'})

    for sort_attr in sort_attrs:
        if sort_attr['order'] == 'desc':
            solr_searcher = solr_searcher.sort_by(u'-' + sort_attr['attr'])
        else:
            solr_searcher = solr_searcher.sort_by(sort_attr['attr'])
    # ключ хеша зависит от языка
    terms_facet_hash = hashlib.md5(
        unicode(terms) + u'_facets_' + get_language() + u'#'.join(exclude_kwargs.values())).hexdigest()

    facets = cache.get(terms_facet_hash, None)
    if not facets:
        solr_searcher = solr_searcher.facet_by(field=facet_fields, limit=15, mincount=1)

    solr_searcher = solr_searcher.field_limit("id")
    paginator = Paginator(solr_searcher, 20)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        results_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        results_page = paginator.page(paginator.num_pages)

    search_statisics = {
        'num_found': results_page.object_list.result.numFound,
        'search_time': "%.3f" % (int(results_page.object_list.QTime) / 1000.0)
    }

    docs = []
    doc_ids = []
    if not facets:
        facets = replace_doc_attrs(results_page.object_list.facet_counts.facet_fields)
        cache.set(terms_facet_hash, facets)

    for row in results_page.object_list:
        doc_id = replace_doc_attrs(row).get('id')
        if doc_id:
            doc_ids.append(doc_id)

    for record in get_records(doc_ids):
        docs.append({
            'id': record.gen_id,
            'record': xml_doc_to_dict(record.content)
        })
    search_breadcumbs = []
    query_dict = None

    star = False
    for term in terms[:search_deep_limit]:
        key = term.keys()[0]
        value = term[key]
        if isinstance(value, str):
            value = value.decode('utf-8')
        if value.strip() == '*':
            star = True

        if type(value) == datetime.datetime:
            value = unicode(value.year)

        new_key = key.split('_')[0]
        if not query_dict:
            query_dict = QueryDict((u'q=' + value + u'&attr=' + key).encode('utf-8')).copy()
        else:
            query_dict.getlist('q').append(value)
            query_dict.getlist('attr').append(key)

        search_breadcumbs.append({
            'attr': key,
            'value': value,
            'href': query_dict.urlencode()
        })

    if catalog == u'ebooks' and len(search_breadcumbs) > 1 and star:
        return HttpResponse(u'Нельзя использовать * при вложенных запросах в каталоге содержащий полный текст')

    json_search_breadcumbs = json.dumps(search_breadcumbs, ensure_ascii=False)

    ordered_facets = []

    for facet_field in facet_fields:
        if facet_field in facets:
            ordered_facets.append(
                {
                    'title': facet_field,
                    'values': facets[facet_field]
                }
            )
    return render(request, 'ssearch/frontend/index.html', {
        'docs': docs,
        'results_page': results_page,
        'facets': ordered_facets,
        'search_breadcumbs': search_breadcumbs,
        'sort': sort,
        'search_statisics': search_statisics,
        'search_request': json_search_breadcumbs,
        'search_attrs': search_attrs,
        'catalog': catalog,
        'library': library
    })


def facet_explore(request, catalog=None, library=None):
    holders = []
    library_code = request.GET.get('library')
    try:
        library = Library.objects.get(code=library_code)
    except Library.DoesNotExist:
        library = None

    if library:
        holders.append(library.code)
        leaf_libraries = library.get_leafnodes()
        for leaf_library in leaf_libraries:
            holders.append(getattr(leaf_library, 'code'))
    facet = request.GET.get('facet')
    offset = int(request.GET.get('offset', '0'))
    if offset < 0:
        offset = 0
    facet_fields = [facet]
    facet_limit = 15
    search_attrs = _make_search_attrs(catalog)
    search_deep_limit = 5  # ограничение вложенных поисков
    solr_connection = httplib2.Http(disable_ssl_certificate_validation=True)
    solr = sunburnt.SolrInterface(settings.SOLR['host'], http_connection=solr_connection)

    qs = request.GET.getlist('q', [])
    attrs = request.GET.getlist('attr', [])
    # sort = request.GET.getlist('sort', [])
    #
    # sort_attrs = []
    #
    # for sort_attr in sort:
    #     mapped_sort_attr = sort_attr_map.get(sort_attr, None)
    #     if not mapped_sort_attr:
    #         continue
    #
    #     sort_attrs.append({
    #         'attr': mapped_sort_attr['attr'],
    #         'order': mapped_sort_attr.get('order', 'asc')
    #     })

    fqs = request.GET.getlist('fq', [])
    fattrs = request.GET.getlist('fattr', [])
    if fqs and fattrs and fqs[0] == u'*' and fattrs[0] == u'*':
        fqs = fqs[1:]
        fattrs = fattrs[1:]
    in_founded = request.GET.get('in_founded', None)

    terms = []
    try:
        # if in_founded:
        terms += terms_constructor(fattrs, fqs)
        terms += terms_constructor(attrs, qs)
    except WrongSearchAttribute:
        return HttpResponse(u'Задан непрвильный атрибут поиска')
    except IndexError:
        return HttpResponse(u'Некорректный набор атрибутов')

    query = None
    if len(terms) == 1 and 'text_t' in terms[0] and terms[0]['text_t'].strip() == '*':
        terms = [{u'*': u'*'}]

    if len(terms) > 1 and u'*' in terms[0][terms[0].keys()[0]].strip() == u'*':
        terms = terms[1:]
    try:
        for term in terms[:search_deep_limit]:
            # если встретилось поле с текстом, то через OR ищем аналогичное с постфиксом _ru
            morph_query = None
            attr = term.keys()[0]
            if len(attr) > 2 and attr[-2:] == '_t' and term.values()[0] != u'*':
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
                    term[attr] = "%s" % term[attr]

                    query = query & solr.Q(**term)
    except ValueError:
        return HttpResponse(u'Неверные параметры')

    if holders:
        holders_query = solr.Q(**{'holder-sigla_s': holders[0]})
        for holder in holders[1:]:
            holders_query |= solr.Q(**{'holder-sigla_s': holder})
        query = query & holders_query

    filter_q = solr.Q()
    if holders:
        holders_q = solr.Q()

        for holder in holders:
            holders_q |= solr.Q(**{'system-holder_s': holder})

        filter_q &= holders_q

    if holders:
        holders_query = solr.Q(**{'system-holder_s': holders[0]})
        for holder in holders[1:]:
            holders_query |= solr.Q(**{'system-holder_s': holder})
        query = query & holders_query

    solr_searcher = solr.query(query)
    if PARTICIPANTS_SHOW_ORG_TYPES:
        participant_types_q = solr.Q()
        for PARTICIPANTS_SHOW_ORG_TYPE in PARTICIPANTS_SHOW_ORG_TYPES:
            participant_types_q |= solr.Q(**{'org_type_s': PARTICIPANTS_SHOW_ORG_TYPE})

        filter_q &= participant_types_q

    solr_searcher = solr_searcher.filter(filter_q)

    exclude_kwargs = {}

    if catalog == u'sc2':
        exclude_kwargs = {'system-catalog_s': u"2"}
    elif catalog == u'ebooks':
        exclude_kwargs = {'system-catalog_s': u"4"}
    else:
        pass

    solr_searcher = solr_searcher.exclude(**exclude_kwargs)


    # ключ хеша зависит от языка
    terms_facet_hash = hashlib.md5(
        unicode(terms) + u'_facets_' + get_language() + u'#'.join(exclude_kwargs.values())).hexdigest()

    facet_by_args = dict(
        field=facet_fields,
        limit=facet_limit,
        mincount=1
    )

    if offset > 0:
        facet_by_args['offset'] = offset

    solr_searcher = solr_searcher.facet_by(**facet_by_args)

    solr_searcher = solr_searcher.field_limit("id")
    paginator = Paginator(solr_searcher, 1)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        results_page = paginator.page(1)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        results_page = paginator.page(paginator.num_pages)

    facets = replace_doc_attrs(results_page.object_list.facet_counts.facet_fields)

    search_breadcumbs = []
    query_dict = None

    star = False
    for term in terms[:search_deep_limit]:
        key = term.keys()[0]
        value = term[key]
        if isinstance(value, str):
            value = value.decode('utf-8')
        if value.strip() == '*':
            star = True

        if type(value) == datetime.datetime:
            value = unicode(value.year)

        new_key = key.split('_')[0]
        if not query_dict:
            query_dict = QueryDict((u'q=' + value + u'&attr=' + key).encode('utf-8')).copy()
        else:
            query_dict.getlist('q').append(value)
            query_dict.getlist('attr').append(key)

        search_breadcumbs.append({
            'attr': key,
            'value': value,
            'href': query_dict.urlencode()
        })

    if catalog == u'ebooks' and len(search_breadcumbs) > 1 and star:
        return HttpResponse(u'Нельзя использовать * при вложенных запросах в каталоге содержащий полный текст')

    json_search_breadcumbs = json.dumps(search_breadcumbs, ensure_ascii=False)

    ordered_facets = []

    for facet_field in facet_fields:
        if facet_field in facets:
            ordered_facets.append(
                {
                    'title': facet_field,
                    'values': facets[facet_field]
                }
            )

    has_next = len(ordered_facets[0]['values']) >= facet_limit
    has_prev = offset > 0

    return render(request, 'ssearch/frontend/facets.html', {
        'facets': ordered_facets,
        'next': offset + facet_limit,
        'prev': offset - facet_limit,
        'has_next': has_next,
        'has_prev': has_prev,
    })


def participant_income(request):
    sigla = request.GET.get('sigla', None)
    solr_connection = httplib2.Http(disable_ssl_certificate_validation=True)
    solr = sunburnt.SolrInterface(settings.SOLR['local_records_host'], http_connection=solr_connection)

    if sigla:
        query = solr.Q(**{'holder-sigla_s': sigla})
    else:
        query = solr.Q(**{'*': '*'})

    solr_searcher = solr.query(query)
    solr_searcher = solr_searcher.field_limit("id")

    solr_searcher = solr_searcher.sort_by('-record-create-date_dts')

    paginator = Paginator(solr_searcher, 20)  # Show 25 contacts per page

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

    for row in results_page.object_list:
        docs.append(replace_doc_attrs(row))

    doc_ids = []
    for doc in docs:
        doc_ids.append(doc['id'])

    records_dict = {}
    records = list(Record.objects.using('local_records').filter(gen_id__in=doc_ids))
    for record in records:
        records_dict[record.gen_id] = etree.tostring(
            xslt_bib_draw_transformer(etree.XML(record.content), abstract='false()'), encoding='utf-8')

    for doc in docs:
        doc['record'] = records_dict.get(doc['id'])

    return render(request, 'ssearch/frontend/income.html', {
        'results_page': results_page,
        'docs': docs
    })


# def select_library(request):
#     # q = Q(parent=None)
#     # org_type = 'library'
#     # if request.user.is_authenticated():
#     #     if request.session.get('auth_source', TATEDU_AUTH_SOURCE) == TATEDU_AUTH_SOURCE:
#     #         org_type = 'school'
#
#     libraries = Library.objects.filter(parent=None, org_type='library').values('code', 'name', 'id')
#     return render(request, 'ssearch/frontend/select_library.html', {
#         'libraries': libraries,
#     })

def select_library(request):
    # q = Q(parent=None)
    # org_type = 'library'
    # if request.user.is_authenticated():
    #     if request.session.get('auth_source', TATEDU_AUTH_SOURCE) == TATEDU_AUTH_SOURCE:
    #         org_type = 'school'

    org_id = request.session.get('org_id')
    current_library = None
    if org_id:
        try:
            current_library = Library.objects.get(id=org_id)
        except Library.DoesNotExist:
            pass

    libraries = Library.objects.filter(hidden=False, org_type__in=PARTICIPANTS_SHOW_ORG_TYPES)
    return render(request, 'ssearch/frontend/select_library.html', {
        'libraries': libraries,
        'current_library': current_library
    })


from levenshtein import levenshtein


def compare(word1, word2):
    word1 = word1.strip().lower().replace(u' ', u'')
    word2 = word2.strip().lower().replace(u' ', u'')
    word1_len = len(word1)
    word2_len = len(word2)
    lev = levenshtein(word1, word2)
    if lev == 0:
        return 1.0
    else:
        if word1_len > word2_len:
            return (float(lev) / word1_len) * 1 / (float(lev) / word2_len)
        else:
            return (float(lev) / word2_len) * 1 / (float(lev) / word1_len)


def detail(request, gen_id):
    catalog = None
    try:
        record = Record.objects.using('records').get(gen_id=gen_id)
        catalog = 'records'
    except Record.DoesNotExist:
        raise Http404()

    # DetailAccessLog(catalog=catalog, gen_id=record.gen_id).save()
    DetailAccessLog.objects.create(catalog=catalog, gen_id=gen_id, date_time=datetime.datetime.now())

    doc_tree = etree.XML(record.content)
    leader8 = doc_tree.xpath('/record/leader/leader08')

    analitic_level = u'0'
    if len(leader8) == 1:
        analitic_level = leader8[0].text

    bib_tree = xslt_bib_draw_transformer(doc_tree)
    marct_tree = xslt_marc_dump_transformer(doc_tree)
    bib_dump = etree.tostring(bib_tree, encoding='utf-8')
    marc_dump = etree.tostring(marct_tree, encoding='utf-8')
    doc_tree_t = xslt_transformer(doc_tree)
    doc = doc_tree_to_dict(doc_tree_t)
    holders = doc.get('holders', list())
    if holders:
        # оставляем уникальных держателей
        doc['holders'] = list(set(holders))
    linked_docs = []
    if analitic_level == '1':
        doc['holders'] = []

        solr_connection = httplib2.Http(disable_ssl_certificate_validation=True)
        solr = sunburnt.SolrInterface(settings.SOLR['host'], http_connection=solr_connection)

        linked_query = solr.query(**{'linked-record-number_s': record.record_id.replace(u"\\", u'\\\\')})
        linked_query = linked_query.field_limit("id")
        linked_results = linked_query.execute()

        linked_doc_ids = []
        for linked_doc in linked_results:
            linked_doc_ids.append(linked_doc['id'])

        records = list(Record.objects.using('records').filter(gen_id__in=linked_doc_ids))

        for record in records:
            record_dict = {}
            record_dict['record'] = xml_doc_to_dict(record.content)
            record_dict['id'] = record.gen_id
            linked_docs.append(record_dict)

            #        for doc in mlt_docs:
            #            doc['record'] = records_dict.get(doc['id'])

    access_count = DetailAccessLog.objects.filter(catalog=catalog, gen_id=record.gen_id).count()
    indexing_doc = record_to_indexing_doc(doc_tree)
    return render(request, 'ssearch/frontend/detail.html', {
        'doc_dump': rusmarc_template.beautify(bib_dump.replace('<b/>', '')),
        'marc_dump': marc_dump,
        'indexing_doc': indexing_doc,
        'doc': doc,
        'gen_id': gen_id,
        'linked_docs': linked_docs,
        'access_count': access_count
    })

    def clean_holder_title(holder):
        return holder.get('org', {}).get('title', '') \
            .lower() \
            .replace(u'цбс', '') \
            .replace(u'го', '') \
            .replace(u'г.', '') \
            .strip()

    holders.sort(key=clean_holder_title)

    return holders


def to_print(request, gen_id):
    catalog = None
    try:
        record = Record.objects.using('records').get(gen_id=gen_id)
        catalog = 'records'
    except Record.DoesNotExist:
        raise Http404()

    # DetailAccessLog(catalog=catalog, gen_id=record.gen_id).save()
    # DetailAccessLog.objects.create(catalog=catalog, gen_id=gen_id, date_time=datetime.datetime.now())

    doc_tree = etree.XML(record.content)
    # leader8 = doc_tree.xpath('/record/leader/leader08')
    #
    # analitic_level = u'0'
    # if len(leader8) == 1:
    #     analitic_level = leader8[0].text

    bib_tree = xslt_bib_draw_transformer(doc_tree)
    marct_tree = xslt_marc_dump_transformer(doc_tree)
    bib_dump = etree.tostring(bib_tree, encoding='utf-8')
    # marc_dump =  etree.tostring(marct_tree, encoding='utf-8')
    doc_tree_t = xslt_transformer(doc_tree)
    doc = doc_tree_to_dict(doc_tree_t)
    # holders = doc.get('holders', list())
    # if holders:
    #     # оставляем уникальных держателей
    #     doc['holders'] = list(set(holders))
    # linked_docs = []
    # if analitic_level == '1':
    #     doc['holders'] = []
    #
    #     solr = sunburnt.SolrInterface(settings.SOLR['host'])
    #     linked_query = solr.query(**{'linked-record-number_s':record.record_id.replace(u"\\",u'\\\\')})
    #     linked_query = linked_query.field_limit("id")
    #     linked_results = linked_query.execute()
    #
    #     linked_doc_ids = []
    #     for linked_doc in linked_results:
    #         linked_doc_ids.append(linked_doc['id'])
    #
    #     records =  list(Ebook.objects.using('records').filter(gen_id__in=linked_doc_ids))
    #     records +=  list(Record.objects.using('records').filter(gen_id__in=linked_doc_ids))
    #
    #     for record in records:
    #         record_dict = {}
    #         record_dict['record'] = xml_doc_to_dict(record.content)
    #         record_dict['id'] = record.gen_id
    #         linked_docs.append(record_dict)

    #        for doc in mlt_docs:
    #            doc['record'] = records_dict.get(doc['id'])

    # access_count = DetailAccessLog.objects.filter(catalog=catalog, gen_id=record.gen_id).count()

    return render(request, 'ssearch/frontend/print.html', {
        'doc_dump': bib_dump.replace('<b/>', ''),
        # 'marc_dump': marc_dump,
        'doc': doc,
        'gen_id': gen_id,
        # 'linked_docs': linked_docs,
        # 'access_count': access_count
    })


from docx import Document
from docx.shared import Inches
from django.utils.html import strip_tags, strip_spaces_between_tags
import re
def print_to_pdf(request):
    # print 1,2
    doc_ids = request.POST.getlist('selected')

    document = Document()

    # document.add_heading('Document Title', 0)

    records = get_records(doc_ids)
    for i, record in enumerate(records):
        doc_tree = etree.XML(record.content)
        bib_tree = xslt_bib_draw_transformer(doc_tree)
        bib_dump = etree.tostring(bib_tree, encoding='utf-8')

        libcard = strip_tags(rusmarc_template.beautify(bib_dump.replace('<b/>', '')).decode('utf-8'))
        while True:
            res = re.search('\.\w', libcard, flags=re.IGNORECASE|re.MULTILINE|re.UNICODE)
            if res is None:
                break
            span = res.span()
            libcard = libcard[0: span[0] + 1] + ' ' + libcard[span[1] - 1: ]
        # libcard = u'. '.join(re.split('\.\w', libcard, flags=re.IGNORECASE | re.UNICODE))
        document.add_paragraph(unicode(i + 1) + u'. ' + libcard)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=print.docx'
    document.save(response)
    return response


@login_required
def saved_search_requests(request):
    saved_requests = SavedRequest.objects.filter(user=request.user).order_by('-add_time')
    srequests = []
    for saved_request in saved_requests:
        try:
            srequests.append({
                'saved_request': saved_request,
                'breads': json.loads(saved_request.search_request),
                'catalog': saved_request.catalog
            })
        except json.JSONDecoder:
            srequests.append({
                'saved_request': saved_request,
                'breads': None,
                'catalog': saved_request.catalog
            })

    return render(request, 'ssearch/frontend/saved_request.html', {
        'srequests': srequests,
    })


def save_search_request(request):
    catalog = request.GET.get('catalog', None)
    if not request.user.is_authenticated():
        return HttpResponse(u'Вы должны быть войти на портал', status=401)

    search_request = request.GET.get('srequest', None)
    if SavedRequest.objects.filter(user=request.user).count() > 500:
        return HttpResponse(u'{"status": "error", "error": "Вы достигли максимально разрешенного количества запросов"}')

    SavedRequest(user=request.user, search_request=search_request, catalog=catalog).save()
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


def content_to_xml(xmlstring_doc):
    doc_tree = etree.XML(xmlstring_doc)
    doc_tree_t = xslt_transformer(doc_tree)


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


def beautify(value):
    value = unicode(value).replace(u'..', u"%#dot#dot#") \
        .replace(u'.:', u"%#dot#colon#") \
        .replace(u'.;', u"%#dot#semicolon#") \
        .replace(u'.!', u"%#dot#screamer#") \
        .replace(u'.?', u"%#dot#question#")

    value = value.replace(u':', u": ") \
        .replace(u'.', u". ") \
        .replace(u',', u", ") \
        .replace(u';', u"; ") \
        .replace(u')', u") ")

    value = value.replace(u"%#dot#dot#", '. ') \
        .replace(u"%#dot#colon#", u'.: ') \
        .replace(u"%#dot#semicolon#", u'.; ') \
        .replace(u"%#dot#screamer#", u'.! ') \
        .replace(u"%#dot#question#", u'.? ')

    return value


# import pymorphy
import uuid
from ..models import SearchRequestLog


# morph = pymorphy.get_morph(settings.PYMORPHY_CDB_DICTS, 'cdb')
def log_search_request(last_search_value, catalog, library_code=u''):
    def clean_term(term):
        """
        Возвращает кортеж из ненормализованног и нормализованного терма
        """
        terms = term.strip().lower().split()
        nn_term = u' '.join(terms)

        n_terms = []
        # нормализация
        for t in terms:
            n_term = t  # morph.normalize(t.upper())
            if isinstance(n_term, set):
                n_terms.append(n_term.pop().lower())
            elif isinstance(n_term, unicode):
                n_terms.append(n_term.lower())

        n_term = u' '.join(n_terms)
        return (nn_term, n_term)

    search_request_id = uuid.uuid4().hex
    term_groups = []

    term = last_search_value.get('value', None)
    if term:
        forms = clean_term(term)
        term_groups.append({
            'nn': forms[0],
            'use': last_search_value.get('attr', u'not defined'),

        })
    logs = []
    for group in term_groups:
        logs.append(SearchRequestLog(
            catalog=catalog,
            search_id=search_request_id,
            use=group['use'],
            not_normalize=group['nn'],
            library_code=library_code
        ))
    SearchRequestLog.objects.bulk_create(logs)


def statictics():
    solr_connection = httplib2.Http(disable_ssl_certificate_validation=True)
    solr = sunburnt.SolrInterface(settings.SOLR['host'], http_connection=solr_connection)

    facet_fields = ['fond_sf']
    qkwargs = {'*': '*'}
    solr_searcher = solr.query(**qkwargs).paginate(start=0, rows=0)
    exclude_kwargs = {'system-catalog_s': u"1"}
    solr_searcher = solr_searcher.exclude(**exclude_kwargs)
    solr_searcher = solr_searcher.facet_by(field=facet_fields, limit=30, mincount=1)
    solr_searcher = solr_searcher.field_limit("id")
    response = solr_searcher.execute()
    collections = {}
    for key in response.facet_counts.facet_fields.keys():
        for val in response.facet_counts.facet_fields[key]:
            collections[val[0]] = val[1]

    stats = {
        'collections': collections,
        'count_all': 0,
        'count_last_month': 0,
    }
    now = datetime.datetime.now()
    before_30_now = now - datetime.timedelta(30)
    count_all = Record.objects.using('records').filter(source_id='2').exclude(deleted=True).count()
    count_last_month = Record.objects.using('records').filter(add_date__year=now.year, add_date__month=now.month,
                                                              source_id='2').exclude(deleted=True).count()
    count_last_30 = Record.objects.using('records').filter(add_date__gte=before_30_now, add_date__lte=now,
                                                           source_id='2').exclude(deleted=True).count()
    stats['count_all'] = count_all
    stats['count_last_month'] = count_last_month
    stats['count_last_30'] = count_last_30
    return stats


def get_collections():
    collections = Record.objects.using('records').filter(source_id='1')
    colls = []
    for collection in collections:
        collections_dict = xml_doc_to_dict(collection.content)
        colls.append(collections_dict)

    return colls
