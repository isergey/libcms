# encoding: utf-8
import json
from lxml import etree
from collections import OrderedDict
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render, urlresolvers, Http404, HttpResponse, get_object_or_404, redirect
from django.utils.http import urlunquote_plus
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .. import models
from .. import solr
from .. import titles
from .. import junimarc
from .. import rusmarc_template
import forms

SEARCH_ATTRS = getattr(settings, 'SEARCH', {}).get('attrs', [])
FULL_TEXT_PREFIX = getattr(settings, 'FULL_TEXT_PREFIX', '')
COVER_PREFIX = getattr(settings, 'COVER_PREFIX', '')

transformers = {}


def transformers_init():
    xsl_transformers = settings.SEARCH['transformers']
    for key in xsl_transformers.keys():
        xsl_transformer = xsl_transformers[key]
        transformers[key] = etree.XSLT(etree.parse(xsl_transformer))


transformers_init()


class BreadcrumbItem(object):
    def __init__(self, attr, value):
        self.attr = attr
        self.value = value
        self.title = titles.get_attr_title(attr)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((frozenset(self.attr), frozenset(self.value)))

    def __unicode__(self):
        return u'%s:%s' % (self.attr, self.value)

    def __str__(self):
        return (u'%s:%s' % (self.attr, self.value)).encode('utf-8')


def index(request):
    page = request.GET.get('page', '1')
    page = int(page)
    per_page = request.GET.get('per_page', 15)
    try:
        per_page = int(per_page)
    except Exception:
        per_page = 15

    if per_page > 100:
        per_page = 100
    if per_page < 1:
        per_page = 15


    SORT_ATTRS = ['score', 'author_ss', 'title_ss', 'date_time_of_income_dts']

    sort_titles = []

    for sort_item in SORT_ATTRS:
        sort_titles.append({
            'attr': sort_item,
            'title': titles.get_attr_title(sort_item)
        })

    sort = request.GET.get('sort', None)
    order = request.GET.get('order', 'asc')
    sorting = []
    if sort and order:
        sorting = ['%s %s' % (sort, order)]


    in_results = request.GET.get('in_results', '0')
    br_attr = request.GET.getlist('br_attr', [])
    br_value = request.GET.getlist('br_value', [])
    priority = request.GET.get('priority', {})
    if priority:
        priority = json.loads(priority)

    titled_attrs = []
    for attr in SEARCH_ATTRS:
        titled_attrs.append({
            'attr': attr,
            'title': titles.get_attr_title(attr)
        })
    if not titled_attrs:
        titled_attrs.append({
            'attr': 'all_t',
            'title': u'Везде'
        })
    breadcrumbs = []

    br_kvs = []
    if in_results == '1':
        br_kvs = build_kv_dicts(br_attr, br_value)
        for item in br_kvs:
            bc = BreadcrumbItem(attr=item['attr'], value=item['value'])
            if bc not in breadcrumbs:
                breadcrumbs.append(bc)

    attrs = request.GET.getlist('attr', [])

    def values_map(value):
        if not value:
            return u'*'
        return value

    values = map(values_map, request.GET.getlist('value', []))

    kv_dicts = br_kvs + build_kv_dicts(attrs, values)

    for item in kv_dicts:
        bc = BreadcrumbItem(attr=item['attr'], value=item['value'])
        if bc not in breadcrumbs:
            breadcrumbs.append(bc)

    search_breadcumbs = make_search_breadcumbs(breadcrumbs)

    search_conditions = build_search_conditions(kv_dicts)

    models.log_search_request(kv_dicts)

    query = build_query(search_conditions, priority)
    offset = (page - 1) * per_page
    if not search_breadcumbs and query == '*:*' and not sorting:
        sorting = ['date_time_of_income_dts desc']
        # query = 'date_time_added_to_db_ss:*'

    highlighting = []
    if query.find('full_text_tru') > -1:
        highlighting = ['full_text_tru']

    result = solr.search(query, limit=per_page, offset=offset, facets=[], sort=sorting,
                         highlighting=highlighting)

    paginator = Paginator(result, per_page)

    try:
        result_page = paginator.page(page)
    except PageNotAnInteger:
        result_page = paginator.page(1)
    except EmptyPage:
        result_page = paginator.page(paginator.num_pages)

    total = result.get('total', 0)
    ids = []

    for doc in result.get('docs', []):
        ids.append(doc['id'])

    records_content = models.get_records(ids)
    jrecords = []

    for i, record_content in enumerate(records_content):
        record_obj = junimarc.json_schema.record_from_json(record_content.content)
        title = rusmarc_template.get_title(record_obj)
        record_tree = junimarc.ruslan_xml.record_to_xml(record_obj)
        libcard = rusmarc_template.beautify(etree.tostring(transformers['libcard'](record_tree), encoding="utf-8"))
        record_dict = make_record_dict(transformers['record_dict'](record_tree, abstract='1'))
        result_row = {
            'attrs': {
                'income_date': rusmarc_template.get_income_date(record_obj)
            },
            'item_info': _get_item_info(record_obj),
            'title': title,
            'row_number': offset + 1 + i,
            'model': record_content,
            'libcard': libcard,
            'dict': record_dict,
            'urls': rusmarc_template.get_full_text_url(record_obj),
            'highlighting': result.get('highlighting', {}).get(record_content.record_id, {})

        }

        jrecords.append(result_row)

    if request.is_ajax():
        return render(request, 'search/frontend/ajax_results.html', {
            'records': jrecords,
            'result_page': result_page
        })

    show_priority = False

    if len(breadcrumbs) == 1 and breadcrumbs[0].attr == 'all_t':
        show_priority = True

    json_search_breadcumbs = json.dumps(search_breadcumbs, ensure_ascii=False)

    return render(request, 'search/frontend/index.html', {
        'sort_titles': sort_titles,
        'FULL_TEXT_PREFIX': FULL_TEXT_PREFIX,
        'titled_attrs': titled_attrs,
        'search_result': result,
        'records': jrecords,
        'total': total,
        'breadcrumbs': search_breadcumbs,
        'show_priority': show_priority,
        'prev_attrs': breadcrumbs,
        'result_page': result_page,
        'search_request': json_search_breadcumbs,
        'COVER_PREFIX': COVER_PREFIX,
    })


def advanced_search(request):
    ADVANCED_ATTRS = [
        'title_t', 'author_t', 'publisher_t', 'subject_keywords_t',
        'all_tru', 'date_of_publication_s', 'date_time_of_income_s', ]

    SORT_ATTRS = ['score', 'author_ss', 'title_ss', 'date_time_of_income_dts']

    sort_titles = []

    for sort_item in SORT_ATTRS:
        sort_titles.append({
            'attr': sort_item,
            'title': titles.get_attr_title(sort_item)
        })

    sort = request.GET.get('sort', None)
    order = request.GET.get('order', 'asc')
    sorting = []
    if sort and order:
        sorting = ['%s %s' % (sort, order)]


    page = request.GET.get('page', '1')
    page = int(page)
    per_page = request.GET.get('per_page', 15)
    try:
        per_page = int(per_page)
    except Exception:
        per_page = 15

    if per_page > 100:
        per_page = 100
    if per_page < 1:
        per_page = 15

    kv_attrs = []
    for k, v in request.GET.items():
        if k in ADVANCED_ATTRS:
            kv_attrs.append({
                'attr': k,
                'value': v,
                'attr_title': titles.get_attr_title(k),
                'value_title': titles.get_attr_value_title(k, v)
            })

    sc = solr.SearchCriteria(u"AND")

    for item in build_search_conditions(kv_attrs):
        sc.add_attr(item['attr'], item['value'])

    offset = (page - 1) * per_page
    result = solr.search(sc.to_lucene_query(), limit=per_page, offset=offset, facets=[], sort=sorting)

    paginator = Paginator(result, per_page)

    try:
        result_page = paginator.page(page)
    except PageNotAnInteger:
        result_page = paginator.page(1)
    except EmptyPage:
        result_page = paginator.page(paginator.num_pages)

    total = result.get('total', 0)
    ids = []

    for doc in result.get('docs', []):
        ids.append(doc['id'])

    records_content = models.get_records(ids)
    jrecords = []

    for i, record_content in enumerate(records_content):
        record_obj = junimarc.json_schema.record_from_json(record_content.content)
        title = rusmarc_template.get_title(record_obj)
        record_tree = junimarc.ruslan_xml.record_to_xml(record_obj)
        libcard = rusmarc_template.beautify(etree.tostring(transformers['libcard'](record_tree), encoding="utf-8"))
        record_dict = make_record_dict(transformers['record_dict'](record_tree, abstract='1'))
        result_row = {
            # 'item_info': _get_item_info(record_obj),
            'attrs': {
                'income_date': rusmarc_template.get_income_date(record_obj)
            },
            'title': title,
            'row_number': offset + 1 + i,
            'model': record_content,
            'libcard': libcard,
            'dict': record_dict,
            'urls': rusmarc_template.get_full_text_url(record_obj),
            'highlighting': result.get('highlighting', {}).get(record_content.record_id, {})

        }
        jrecords.append(result_row)

    return render(request, 'search/frontend/advanced_search.html', {
        'FULL_TEXT_PREFIX': FULL_TEXT_PREFIX,
        'search_result': result,
        'records': jrecords,
        'total': total,
        'result_page': result_page,
        'COVER_PREFIX': COVER_PREFIX,
        'sort_titles': sort_titles
    })


def help(request):
    result = solr.luke()

    fields = []

    for field in result.get('fields', []):
        name = field.get('name', '')
        fields.append({
            'name': name,
            'title': titles.get_attr_title(name),
            'type': field.get('type', 'неизвестно')
        })
    fields = sorted(fields, key=lambda item: item['title'])
    return render(request, 'search/frontend/help.html', {
        'fields': fields,
        'result': result
    })


def detail(request):
    tpl = 'search/frontend/detail.html'
    prnt = request.GET.get('print', None)
    id = request.GET.get('id', '')

    if prnt:
        tpl = tpl = 'search/frontend/print.html'

    records = models.get_records([id])
    if not records:
        raise Http404('Record not found')
    record = records[0]
    record_obj = junimarc.json_schema.record_from_json(record.content)
    record_tree = junimarc.ruslan_xml.record_to_xml(record_obj)
    record_dict = rusmarc_template.doc_tree_to_dict(transformers['record_dict'](record_tree, abstract='0'))
    libcard = rusmarc_template.beautify(
        etree.tostring(transformers['libcard'](record_tree),
                       encoding="utf-8")
    )
    urls = rusmarc_template.get_full_text_url(record_obj)
    result_record = {
        'attrs': {
            'income_date': rusmarc_template.get_income_date(record_obj)
        },
        'title': rusmarc_template.get_title(record_obj),
        'model': record,
        'object': record_obj,
        'dict': record_dict,
        'libcard': libcard,
        'urls': urls,
        'item_info': _get_item_info(record_obj),
    }

    local_number = record_dict.get('local_number', [])
    linked_records = []
    if local_number:
        linked_records = _load_linked_records(local_number[0], request)

    user = None
    if request.user.is_authenticated():
        user = request.user

    models.DetailAccessLog(record_id=id, user=user, action='detail').save()
    access_count = models.DetailAccessLog.objects.filter(record_id=id, action='detail').count()
    full_text_count = models.DetailAccessLog.objects.filter(record_id=id, action='full_text').count()

    return render(request, tpl, {
        'COVER_PREFIX': COVER_PREFIX,
        'record': result_record,
        'linked_records': linked_records,
        'access_count': access_count,
        'full_text_count': full_text_count
    })


def load_raw_record(request):
    id = request.GET.get('id', '')
    records = models.get_records([id])
    if records:
        return HttpResponse(content=records[0].content, content_type='application/json')
    else:
        raise Http404(u'Запись не найдена')


def _get_item_info(record_obj):
    f899 = record_obj.get_fields(tag='899')
    if not f899:
        return {}
    items_count = None
    author_code = u""
    sf_h = f899[0].get_subfields(code='h')
    if sf_h:
        author_code = sf_h[0].get_data()

    bd_code = u''
    sf_i = f899[0].get_subfields(code='i')
    if sf_i:
        bd_code = sf_i[0].get_data()

    items = 0
    for field899 in f899:
        items += len(field899.get_subfields(code='p'))

    if items:
        items_count = items
    return {
        'items_count': items_count,
        'author_code': author_code,
        'bd_code': bd_code
    }


def _load_linked_records(local_number, request):
    per_page = 10
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    offset = (page - 1) * per_page
    result = solr.search(
        'linked_record_number_s:"%s"' % solr.escape(local_number),
        offset=offset,
        limit=per_page,
        sort=['date_time_of_income_dts desc']
    )

    paginator = Paginator(result, 10)

    try:
        result_page = paginator.page(page)
    except PageNotAnInteger:
        result_page = paginator.page(1)
    except EmptyPage:
        result_page = paginator.page(paginator.num_pages)

    ids = []

    for doc in result.get('docs', []):
        ids.append(doc['id'])

    records = models.get_records(ids)
    jrecords = []

    for i, record in enumerate(records):
        record_obj = junimarc.json_schema.record_from_json(record.content)
        record_tree = junimarc.ruslan_xml.record_to_xml(record_obj)
        record_dict = rusmarc_template.doc_tree_to_dict(transformers['record_dict'](record_tree, abstract='0'))
        for attr in record_dict:
            values = []
            for value in record_dict[attr]:
                values.append(titles.get_attr_value_title(attr, value))
            record_dict[attr] = values
        jrecords.append({
            'attrs': {
                'income_date': rusmarc_template.get_income_date(record_obj)
            },
            'model': record,
            'dict': record_dict,
            'title': rusmarc_template.get_title(record_obj)
        })
    return {
        'result_page': result_page,
        'linked_records': jrecords
    }


"""
def detail(request):
    id = request.GET.get('id', '')
    records = models.get_records_content([id])

    if not records:
        raise Http404('Record not found')

    record = records[0]
    record_obj = junimarc.json_schema.record_from_json(record.content)
    record_tree = junimarc.ruslan_xml.record_to_xml(record_obj)
    libcard = rusmarc_template.beautify(etree.tostring(transformers['libcard'](record_tree), encoding="utf-8"))
    marc_dump = record_obj.to_html()
    record_dict = make_record_dict(transformers['record_dict'](record_tree, abstract='1'))
    urls = rusmarc_template.get_full_text_url(record_obj)
    local_number = record_dict.get('local_number', [])

    linked_records = _load_linked_records(local_number, request)

    result_record = {
        'FULL_TEXT_PREFIX': FULL_TEXT_PREFIX,
        'COVER_PREFIX': COVER_PREFIX,
        'urls': urls,
        'dict': record_dict,
        'model': record,
        'object': record_obj,
        'libcard': libcard,
        'marc_dump': marc_dump,
        'linked_records': linked_records,

    }

    user = None
    if request.user.is_authenticated():
        user = request.user

    models.DetailAccessLog(record_id=id, user=user, action='detail').save()
    access_count = models.DetailAccessLog.objects.filter(record_id=id, action='detail').count()
    full_text_count = models.DetailAccessLog.objects.filter(record_id=id, action='full_text').count()
    return render(request, 'search/frontend/detail.html', {
        'record': result_record,
        'linked_records': linked_records,
        'access_count': access_count,
        'full_text_count': full_text_count,
    })
"""


def full_text_redirect(request):
    ft_url = request.GET.get('ft_url')
    id = request.GET.get('id')
    search = request.GET.get('search', '')

    user = None
    if request.user.is_authenticated():
        user = request.user

    models.DetailAccessLog(record_id=id, user=user, action='full_text').save()
    slash = ''
    if not FULL_TEXT_PREFIX.endswith('/') and not ft_url.startswith('/'):
        slash = '/'
    url = FULL_TEXT_PREFIX + slash + ft_url
    if search:
        url += u'#search="%s"' % search

    return redirect(url)


def get_title(record_tree):
    r = record_tree.xpath('//span[@class="titleProper"]/text()')
    return r


def make_record_dict(doc_tree):
    doc_dict = {}
    for element in doc_tree.getroot().getchildren():
        attrib = element.attrib['name']
        value = element.text
        # если поле пустое, пропускаем
        if not value: continue
        # value = beautify(value)
        values = doc_dict.get(attrib, None)
        if not values:
            doc_dict[attrib] = [value]
        else:
            values.append(value)
    return doc_dict


def facets(request):
    facets_fields = getattr(settings, 'SEARCH', {}).get('facet_fields', [])
    superuser_facets = getattr(settings, 'SEARCH', {}).get('superuser_facets', [])
    if request.user.is_authenticated() and (request.user.is_superuser or request.user.is_staff):
        facets_fields += superuser_facets

    in_results = request.GET.get('in_results', '0')
    br_attr = request.GET.getlist('br_attr', [])
    br_value = request.GET.getlist('br_value', [])

    br_kvs = []
    if in_results == '1':
        br_kvs = build_kv_dicts(br_attr, br_value)

    attrs = request.GET.getlist('attr', [])
    values = request.GET.getlist('value', [])

    kv_dicts = br_kvs + build_kv_dicts(attrs, values)

    search_conditions = build_search_conditions(kv_dicts)
    query = build_query(search_conditions)
    result = solr.search(query, limit=0, offset=0, facets=facets_fields)
    result_facets = []

    facets = result.get('facets', {})

    for facet_field in facets_fields:
        result_facet = {
            'code': facet_field,
            'title': titles.get_attr_title(facet_field),
            'values': []
        }
        for facet_row in facets.get(facet_field, []):
            result_facet['values'].append({
                'title': titles.get_attr_value_title(facet_field, facet_row['value']),
                'value': facet_row['value'],
                'count': facet_row['count'],
            })
        result_facets.append(result_facet)

    return render(request, 'search/frontend/facets.html', {
        'facets': result_facets
    })


def more_facets(request):
    lm = request.GET.get('lm')
    load_more = json.loads(lm)

    facet_offset = int(load_more['loaded']) - 1
    facet_field = load_more['facet']
    facet_limit = 15

    in_results = request.GET.get('in_results', '0')
    br_attr = request.GET.getlist('br_attr', [])
    br_value = request.GET.getlist('br_value', [])
    priority = request.GET.get('priority', {})
    if priority:
        priority = json.loads(priority)

    br_kvs = []
    if in_results == '1':
        br_kvs = build_kv_dicts(br_attr, br_value)

    attrs = request.GET.getlist('attr', [])
    values = request.GET.getlist('value', [])

    kv_dicts = br_kvs + build_kv_dicts(attrs, values)

    search_conditions = build_search_conditions(kv_dicts)
    query = build_query(search_conditions)
    result = solr.search(query, limit=0, offset=0, facets=[facet_field], facet_offset=facet_offset, facet_limit=15)
    result_facets = []

    facets = result.get('facets', {})

    result_facet = {
        'has_more': True,
        'code': facet_field,
        'title': titles.get_attr_title(facet_field),
        'values': []
    }
    for facet_row in facets.get(facet_field, []):
        result_facet['values'].append({
            'title': titles.get_attr_value_title(facet_field, facet_row['value']),
            'value': facet_row['value'],
            'count': facet_row['count'],
        })

    if len(result_facet['values']) < facet_limit:
        result_facet['has_more'] = False
    return HttpResponse(json.dumps(result_facet, ensure_ascii=False), content_type='text/javascript')


def facet_explore(request):
    fe = request.GET.get('fe')
    fe = json.loads(fe)

    facet_offset = int(request.GET.get('offset', 0))
    if facet_offset < 0:
        facet_offset = 0

    facet_field = fe['facet']
    facet_limit = 15

    attrs = request.GET.getlist('attr', [])
    values = request.GET.getlist('value', [])

    kv_dicts = build_kv_dicts(attrs, values)
    search_conditions = build_search_conditions(kv_dicts)
    query = build_query(search_conditions)
    result = solr.search(query, limit=0, offset=0, facets=[facet_field], facet_offset=facet_offset,
                         facet_limit=facet_limit)
    facets = result.get('facets', {})
    result_facet = {
        'has_prev': False,
        'has_more': True,
        'code': facet_field,
        'title': titles.get_attr_title(facet_field),
        'values': []
    }
    for facet_row in facets.get(facet_field, []):
        result_facet['values'].append({
            'title': titles.get_attr_value_title(facet_field, facet_row['value']),
            'value': facet_row['value'],
            'count': facet_row['count'],
        })

    if len(result_facet['values']) < facet_limit:
        result_facet['has_more'] = False

    if facet_offset:
        facet_offset > 0
        result_facet['has_prev'] = True

    return render(request, 'search/frontend/facet_explore.html', {
        'result_facet': result_facet,
        'next': facet_offset + facet_limit,
        'prev': facet_offset - facet_limit
    })


def make_search_breadcumbs(attrs_values):
    """
    Создание целопчки поисковых фильтров
    :param attrs_values:
    :return:
    """
    search_breadcumbs = []
    search_url = urlresolvers.reverse('search:frontend:index')

    attrs_prepare = []
    values_prepare = []

    for item in attrs_values:
        attr_url_part = u'attr=' + getattr(item, 'attr')
        value_url_part = u'value=' + urlunquote_plus(getattr(item, 'value'))

        search_breadcumbs.append({
            'attr': getattr(item, 'attr'),
            'title': getattr(item, 'title', getattr(item, 'attr')),
            'href': search_url + u'?' + u'&'.join(attrs_prepare) + u'&' + attr_url_part + u'&' + u'&'.join(
                values_prepare) + u'&' + value_url_part,
            'value': titles.get_attr_value_title(getattr(item, 'attr'), getattr(item, 'value')),
        })

        attrs_prepare.append(attr_url_part)
        values_prepare.append(value_url_part)
    return search_breadcumbs


def build_search_conditions(key_value_dicts):
    """
    Формирует список поисковых условий
    :param key_value_dicts: список словарей атрибут-значение полученные из запроса
    :return:
    """
    search_conditions = []
    for item in key_value_dicts:
        attr = item['attr']

        value = u'' + item['value']

        if not value or not attr:
            continue

        if attr.endswith('_s') and value != '*':
            value = '"' + value.replace('"', '\\"') + '"'

        search_conditions.append({
            'attr': attr,
            'value': u'(%s)' % value
        })

    return search_conditions


def build_query(search_conditions, priority={}):
    """
    Формирование solr запроса
    :param search_conditions: список поисковых атрибутов со значениями
    :return: строку запроса
    """

    if not search_conditions:
        return '*:*'

    sc = solr.SearchCriteria('AND')

    for search_condition in search_conditions:
        if search_condition['attr'] == 'query':
            return search_condition['value'].strip()
        if search_condition['attr'] == 'all_t':
            if search_condition['value'].strip() == '*' and len(search_conditions) > 1:
                continue
            sc.add_search_criteria(get_attrs_for_all(search_condition['value'], priority))
        else:
            sc.add_attr(search_condition['attr'], search_condition['value'])

    return sc.to_lucene_query()


def get_attrs_for_all(value, priority={}):
    all_sc = solr.SearchCriteria(u"OR")
    all_sc.add_attr(u'author_t', '%s^%s' % (value, str(priority.get('author_t', 96))))
    all_sc.add_attr(u'title_t', '%s^%s' % (value, str(priority.get('title_t', 64))))
    all_sc.add_attr(u'title_tru', '%s^%s' % (value, str(priority.get('title_t', 30))))
    all_sc.add_attr(u'subject_keywords_tru', '%s^%s' % (value, str(priority.get('subject_keywords_tru',12)))),
    all_sc.add_attr(u'subject_heading_tru', '%s^%s' % (value, str(priority.get('subject_heading_t', 6)))),
    all_sc.add_attr(u'full_text_tru', '%s^%s' % (value, 3)),
    all_sc.add_attr(u'all_tru', '%s^%s' % (value, 2))
    return all_sc


def build_kv_dicts(attrs, values):
    """
    Формирует список словарей атрибут-значение
    :param attrs: атрибуты
    :param values: занчения
    :return: список словарей
    """
    kv_dicts = []
    if len(attrs) == len(values):
        for i in xrange(len(attrs)):
            kv_dicts.append({
                'attr': attrs[i],
                'value': values[i]
            })

    return kv_dicts


def parse_get_params(get_params_string):
    params_dict = {}
    params = get_params_string.replace(u'?', '')
    if params:

        params_parts = params.split('&')
        for param_part in params_parts:
            key_value_pair = param_part.split('=')
            if len(key_value_pair) > 1:
                values = params_dict.get(key_value_pair[0], [])
                if not values:
                    params_dict[key_value_pair[0]] = values
                values.append(urlunquote_plus(key_value_pair[1]))
    return params_dict


@login_required
def saved_search_requests(request):
    saved_requests = models.SavedRequest.objects.filter(user=request.user)
    srequests = []
    for saved_request in saved_requests:
        try:
            srequests.append({
                'saved_request': saved_request,
                'breads': json.loads(saved_request.search_request),
            })
        except json.JSONDecoder:
            srequests.append({
                'saved_request': saved_request,
                'breads': None
            })

    return render(request, 'search/frontend/saved_request.html', {
        'srequests': srequests,
    })


def save_search_request(request):
    if not request.user.is_authenticated():
        return HttpResponse(u'Вы должны быть войти на портал', status=401)
    search_request = request.GET.get('srequest', None)
    if models.SavedRequest.objects.filter(user=request.user).count() > 500:
        return HttpResponse(u'{"status": "error", "error": "Вы достигли максимально разрешенного количества запросов"}')

    models.SavedRequest(user=request.user, search_request=search_request).save()
    return HttpResponse(u'{"status": "ok"}')


def delete_search_request(request, id):
    if not request.user.is_authenticated():
        return HttpResponse(u'Вы должны быть войти на портал', status=401)
    sr = get_object_or_404(models.SavedRequest, user=request.user, id=id)
    sr.delete()
    return HttpResponse(u'{"status": "ok"}')


def income(request):
    sources = getattr(settings, 'INCOME', {}).get('sources', [])

    start_date = None
    end_date = None

    date_filter_form = forms.get_income_filter_form()(request.GET)
    if date_filter_form.is_valid():
        start_date = date_filter_form.cleaned_data['start_date']
        end_date = date_filter_form.cleaned_data['end_date']

    if request.GET.get('short', None):
        template = 'search/frontend/income_short.html'
    else:
        template = 'search/frontend/income_list.html'

    date_range = u''
    if start_date and end_date:
        date_range = u'[%s TO %s]' % (
            start_date.strftime('%Y-%m-%dT%H:%M:%SZ'), end_date.strftime('%Y-%m-%dT%H:%M:%SZ'))
    elif start_date:
        date_range = u'[%s TO *]' % (start_date.strftime('%Y-%m-%dT%H:%M:%SZ'))
    elif end_date:
        date_range = u'[* TO %s]' % (end_date.strftime('%Y-%m-%dT%H:%M:%SZ'))

    collection_field = 'system_source_id_s'
    income_groups = []
    for source in sources:
        income_groups.append({
            'id': source['id'],
            'title': source['title'],
            'date_groups': _get_income_from_collection(source['id'], collection_field, source['days_count'],
                                                       date_range=date_range)
        })
    return render(request, template, {
        'COVER_PREFIX': COVER_PREFIX,

        'income_groups': income_groups,
        'date_filter_form': date_filter_form
    })


def _get_income_from_collection(collection_name, collection_field, days_count=365, date_range=None):
    date_field = 'date_time_of_income_dt'
    date_facet = 'date_time_of_income_s'
    date_query_part = '[NOW-%sDAYS TO NOW]' % days_count
    if date_range:
        date_query_part = date_range

    result = solr.search(
        '%s:%s AND %s:"%s"' % (date_field, date_query_part, collection_field, collection_name),
        limit=0, offset=0, facets=[date_facet], facet_limit=days_count, facet_sort='index'
    )

    dates = []

    for range_item in result.get('facets', {}).get(date_facet, []):
        dates.insert(0, range_item['value'])

    record_content_cache = {}

    date_groups = OrderedDict()

    dates_splice = dates[0:3]
    if date_range:
        dates_splice = dates
    for dateStr in dates_splice:
        date = datetime.strptime(dateStr, '%Y%m%d')
        date_groups[date] = OrderedDict()

        result = solr.search('%s:"%s" AND %s:"%s" ' % (date_facet, dateStr, collection_field, collection_name),
                             limit=100, offset=0, sort=['title_ss asc'])

        for item in result['docs']:
            record_content_cache[item['id']] = None
            date_groups[date][item['id']] = {}

    for record_content in models.get_records(record_content_cache.keys()):
        record_content_cache[record_content.record_id] = record_content

    for date, ids in date_groups.items():
        for id, value in ids.items():
            record_content = record_content_cache[id]
            record_obj = junimarc.json_schema.record_from_json(record_content.content)

            record_tree = junimarc.ruslan_xml.record_to_xml(record_obj)

            value['record_content'] = record_content
            value['libcard'] = rusmarc_template.beautify(
                etree.tostring(transformers['libcard'](record_tree), encoding="utf-8"))
            value['record_dict'] = make_record_dict(transformers['record_dict'](record_tree, abstract='1'))

    return date_groups


def searchable_incomes(request):
    sources = getattr(settings, 'INCOME', {}).get('sources', [])

    start_date = None
    end_date = None

    date_filter_form = forms.get_income_filter_form()(request.GET)
    if date_filter_form.is_valid():
        start_date = date_filter_form.cleaned_data['start_date']
        end_date = date_filter_form.cleaned_data['end_date']

