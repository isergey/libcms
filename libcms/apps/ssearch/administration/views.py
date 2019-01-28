# coding: utf-8
import datetime
import hashlib
import io
import json
import os
import re
import sys
import zlib

import MySQLdb
import httplib2
import sunburnt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.db import transaction  # , connection, connections
from django.shortcuts import render, redirect, HttpResponse, Http404
from guardian.decorators import permission_required_or_403
from lxml import etree
from participants.models import Library
from pymarc2 import reader, record, field, marcxml
from ssearch.models import Upload, Record, IndexStatus

from forms import AttributesForm, GroupForm, PeriodForm, CatalogForm
from forms import UploadForm
from libcms.libs.common.xslt_transformers import xslt_indexing_transformer
from ..common import resolve_date
from ..models import requests_count, requests_by_attributes, requests_by_term, Source

SIGLA_DELIMITER = "\n"

BASE_PATH = getattr(settings, 'PROJECT_PATH')


@login_required
@permission_required_or_403('ssearch.view_statistics')
def index(request):
    return render(request, 'ssearch/administration/index.html')


# def statistics(request, catalog=None):
#    return HttpResponse(u'Статистика')

@login_required
@permission_required_or_403('ssearch.view_statistics')
def statistics(request, catalog=None):
    """
    тип графика
    название графика
    массив название
    массив данных
    подпись по x
    подпись по y
    """
    chart_type = 'column'
    chart_title = u'Название графика'
    row_title = u'Параметр'
    y_title = u'Ось Y'

    statistics = request.GET.get('statistics', 'requests')
    catalogs = []
    if not catalog:
        catalogs += ['sc2', 'ebooks']
    else:
        catalogs.append(catalog)
    # catalogs = ZCatalog.objects.all()
    start_date = datetime.datetime.now()
    end_date = datetime.datetime.now()
    date_group = u'2'  # группировка по дням
    attributes = []

    period_form = PeriodForm()
    group_form = GroupForm()
    attributes_form = AttributesForm()
    catalog_form = CatalogForm()
    if request.method == 'POST':
        period_form = PeriodForm(request.POST)
        group_form = GroupForm(request.POST)
        attributes_form = AttributesForm(request.POST)
        catalog_form = CatalogForm(request.POST)

        if period_form.is_valid():
            start_date = period_form.cleaned_data['start_date']
            end_date = period_form.cleaned_data['end_date']

        if group_form.is_valid():
            date_group = group_form.cleaned_data['group']

        if attributes_form.is_valid():
            attributes = attributes_form.cleaned_data['attributes']

        if catalog_form.is_valid():
            catalogs = catalog_form.cleaned_data['catalogs']

    if statistics == 'requests':
        attributes_form = None
        rows = requests_count(
            start_date=start_date,
            end_date=end_date,
            group=date_group,
            catalogs=catalogs
        )
        chart_title = u'Число поисковых запросов по дате'
        row_title = u'Число поисковых запросов'
        y_title = u'Число поисковых запросов'

    elif statistics == 'attributes':
        group_form = None
        rows = requests_by_attributes(
            start_date=start_date,
            end_date=end_date,
            attributes=attributes,
            catalogs=catalogs
        )

        chart_title = u'Число поисковых запросов по поисковым атрибутам'
        row_title = u'Число поисковых запросов'
        y_title = u'Число поисковых запросов'
        chart_type = 'bar'

    elif statistics == 'terms':
        group_form = None
        rows = requests_by_term(
            start_date=start_date,
            end_date=end_date,
            attributes=attributes,
            catalogs=catalogs
        )

        chart_title = u'Число поисковых запросов по фразам'
        row_title = u'Число поисковых запросов'
        y_title = u'Число поисковых запросов'
        chart_type = 'bar'
    else:
        return HttpResponse(u'Неправильный тип статистики')

    data_rows = json.dumps(rows, ensure_ascii=False)

    return render(request, 'ssearch/administration/statistics.html', {
        'data_rows': data_rows,
        'catalog_form': catalog_form,
        'period_form': period_form,
        'group_form': group_form,
        'attributes_form': attributes_form,
        'chart_type': chart_type,
        'chart_title': chart_title,
        'y_title': y_title,
        'row_title': row_title,
        'active_module': 'zgate'
    })


def return_record_class(scheme):
    if scheme == 'rusmarc' or scheme == 'unimarc':
        return record.UnimarcRecord
    elif scheme == 'usmarc':
        return record.Record
    else:
        raise Exception(u'Wrong record scheme')


def check_iso2709(source, scheme, encoding='utf-8'):
    record_cls = return_record_class(scheme)
    if not len(reader.Reader(record_cls, source, encoding)):
        raise Exception(u'File is not contains records')


def check_xml(source):
    try:
        etree.parse(source)
    except Exception as e:
        raise Exception(u'Wrong XML records file. Error: ' + e.message)


# Our initial page
def initial(request):
    return render(request, 'ssearch/administration/upload.html', {
        'form': UploadForm(),
    })


# Our file upload handler that the form will post to
def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            source = default_storage.open(uploaded_file.file)

            try:
                if uploaded_file.records_format == 'iso2709':
                    check_iso2709(source, uploaded_file.records_scheme, uploaded_file.records_encodings)
                elif uploaded_file.records_format == 'xml':
                    check_xml(source)
                else:
                    return HttpResponse(u"Wrong file format")
            except Exception as e:
                default_storage.delete(uploaded_file.file)
                uploaded_file.delete()
                return HttpResponse(u"Error: wrong records file structure: " + e.message)

    return redirect('ssearch:administration:initial')


@transaction.atomic
def pocess(request):
    uploaded_file = Upload.objects.filter(processed=False)[:1]

    if not uploaded_file:
        return HttpResponse(u'No files')
    else:
        uploaded_file = uploaded_file[0]

    source = default_storage.open(uploaded_file.file)
    record_cls = return_record_class(uploaded_file.records_scheme)

    records = []
    if uploaded_file.records_format == 'iso2709':
        for mrecord in reader.Reader(record_cls, source):
            if len(records) > 10:
                inset_records(records, uploaded_file.records_scheme)
                records = []
            records.append(mrecord)
        inset_records(records, uploaded_file.records_scheme)

    elif uploaded_file.records_format == 'xml':
        raise Exception(u"Not yeat emplemented")
    else:
        return HttpResponse(u"Wrong file format")

    return HttpResponse(u'ok')


def inset_records(records, scheme):
    for record in records:
        # gen id md5 hash of original marc record encoded in utf-8
        gen_id = unicode(hashlib.md5(record.as_marc()).hexdigest())
        if record['001']:
            record_id = record['001'][0].data
            record['001'][0].data = gen_id
        else:
            record.add_field(field.ControlField(tag=u'001', data=gen_id))
            record_id = gen_id

        filter_attrs = {
            'record_id': record_id
        }
        attrs = {
            'gen_id': gen_id,
            'record_id': record_id,
            'scheme': scheme,
            'content': etree.tostring(marcxml.record_to_rustam_xml(record, syntax=scheme), encoding='utf-8'),
            'add_date': datetime.datetime.now()
        }

        rows = Record.objects.filter(**filter_attrs).update(**attrs)
        if not rows:
            attrs.update(filter_attrs)
            obj = Record.objects.create(**attrs)


def convert(request):
    pass


def indexing(request):
    reset = request.GET.get('reset', u'0')
    if reset == u'1':
        reset = True
    else:
        reset = False

    for slug in settings.SOLR['catalogs'].keys():
        _indexing(slug, reset)

    return HttpResponse('Ok')


# регулярки, с помощью которых вычленяются номера томов
re_t1_t2 = re.compile(ur"(?P<t1>\d+)\D+(?P<t2>\d+)", re.UNICODE)
re_t1 = re.compile(ur"(?P<t1>\d+)", re.UNICODE)


def gs(obj):
    size = 0
    size += sys.getsizeof(obj)
    if isinstance(obj, dict):
        for key, val in obj.items():
            size += gs(val)
            size += gs(key)
    elif isinstance(obj, list) or isinstance(obj, tuple):
        for item in obj:
            size += gs(item)
    return size


@transaction.atomic
def _indexing(slug, reset=False):
    sources_index = {}
    sources = list(Source.objects.using('records').all())

    for source in sources:
        sources_index[source.id] = source

    try:
        solr_address = settings.SOLR['host']
        db_conf = settings.DATABASES.get(settings.SOLR['catalogs'][slug]['database'], None)
    except KeyError:
        raise Http404(u'Catalog not founded')

    if not db_conf:
        raise Exception(u'Settings not have inforamation about database, where contains records.')

    if db_conf['ENGINE'] != 'django.db.backends.mysql':
        raise Exception(u' Support only Mysql Database where contains records.')
    try:
        conn = MySQLdb.connect(
            host=db_conf['HOST'],
            user=db_conf['USER'],
            passwd=db_conf['PASSWORD'],
            db=db_conf['NAME'],
            port=int(db_conf['PORT']),
            compress=True,
            charset='utf8',
            use_unicode=True,
            cursorclass=MySQLdb.cursors.SSDictCursor
        )
    except MySQLdb.OperationalError as e:
        conn = MySQLdb.connect(
            unix_socket=db_conf['HOST'],
            user=db_conf['USER'],
            passwd=db_conf['PASSWORD'],
            db=db_conf['NAME'],
            port=int(db_conf['PORT']),
            compress=True,
            charset='utf8',
            use_unicode=True,
            cursorclass=MySQLdb.cursors.SSDictCursor
        )
    holdings_index = _load_holdings(conn)
    orgs_index = _load_orgs()
    sources_index = _load_sources()

    try:
        index_status = IndexStatus.objects.get(catalog=slug)
    except IndexStatus.DoesNotExist:
        index_status = IndexStatus(catalog=slug)
    # select_query = "SELECT * FROM records where deleted = 0 AND LENGTH(content) > 0 and record_id='ru\\\\nlrt\\\\1359411'"
    select_query = "SELECT * FROM records where deleted = 0 AND LENGTH(content) > 0"
    # if not getattr(index_status, 'last_index_date', None):
    #     select_query = "SELECT * FROM records where deleted = 0 and content != NULL"
    # else:
    #     select_query = "SELECT * FROM records where update_date >= '%s' and deleted = 0" % (
    #         str(index_status.last_index_date))

    solr = sunburnt.SolrInterface(solr_address, http_connection=httplib2.Http(disable_ssl_certificate_validation=True))
    docs = list()

    start_index_date = datetime.datetime.now()

    conn.query(select_query)
    rows = conn.use_result()
    res = rows.fetch_row(how=1)

    i = 0
    while res:
        if not res[0]['content']:
            res = rows.fetch_row(how=1)
            continue
        zf = zipfile.ZipFile(io.BytesIO((res[0]['content'])))
        content = zf.read('1.xml').decode('utf-8')
        doc_tree = etree.XML(content)
        doc_tree = xslt_indexing_transformer(doc_tree)
        doc = doc_tree_to_dict(doc_tree)
        doc = add_sort_fields(doc)

        # для сортировки по тому, извлекаем строку содержащую номер тома или промежуток и посещаем резултат вычисления
        # в поле tom_f, которое в последствии сортируется
        # если трока типа т.1 то в том добавляется float 1
        # если строка содержит т.1-2 то добавляется float (1+2) / 2 - средне арифметическое, чтобы усреднить для сортировки

        tom = doc.get('tom_s', None)
        if tom and isinstance(tom, unicode):
            tom = tom.strip().replace(u' ', u'')
            r = re_t1_t2.search(tom)
            if r:
                groups = r.groups()
                doc['tom_f'] = (int(groups[0]) + int(groups[1])) / 2.0
            else:
                r = re_t1.search(tom)
                if r:
                    doc['tom_f'] = float(r.groups()[0])

        issn = doc.get('issn_t')
        if issn:
            for issn_item in issn:
                new_issn_value = issn_item.replace('-', '').replace(' ', '')
                if new_issn_value != issn_item:
                    doc['issn_t'].append(new_issn_value)

        isbn = doc.get('isbn_t')
        if isbn:
            for isbn_item in isbn:
                new_isbn_value = isbn_item.replace('-', '').replace(' ', '')
                if new_isbn_value != isbn_item:
                    doc['isbn_t'].append(new_isbn_value)

        try:
            record_create_date = doc.get('record-create-date_dt', None)
            # print 'record_create_date1', record_create_date
            if record_create_date:
                doc['record-create-date_dts'] = record_create_date
        except Exception as e:
            print 'Error record-create-date_dt'

        holder_codes = _get_holdings(
            source_id=res[0]['source_id'],
            record_id=res[0]['record_id'],
            orgs_index=orgs_index,
            holdings_index=holdings_index,
            sources_index=sources_index
        )

        # if holder_codes:
        #     print holder_codes

        if holder_codes:
            doc['system-holder_s'] = holder_codes

            org_types = set()
            for holder_code in holder_codes:
                org_type = orgs_index.get('code', {}).get(holder_code, {}).get('org_type', '')
                if org_type:
                    org_types.add(org_type)

            if org_types:
                doc['org_type_s'] = list(org_types)

        doc['system-add-date_dt'] = res[0]['add_date']
        doc['system-add-date_dts'] = res[0]['add_date']
        doc['system-update-date_dt'] = res[0]['update_date']
        doc['system-update-date_dts'] = res[0]['update_date']
        doc['system-catalog_s'] = res[0]['source_id']
        # doc['source-type_s'] = sources_index[res[0]['source_id']].source_type
        if str(doc['system-catalog_s']) == '2':
            full_text_file = None
            #            doc['system-update-date_dt'] = res[0]['doc-id_s']
            urls = doc.get('doc-id_s', None)
            if urls and type(urls) == list:
                for url in doc.get('doc-id_s', None):
                    if url:
                        full_text_file = url.split('/')[-1]
            else:
                if urls:
                    full_text_file = urls.split('/')[-1]
            if full_text_file:
                text = full_text_extract(full_text_file)
                if text:
                    doc['full-text'] = text

        docs.append(doc)
        i += 1
        if i % 100 == 0:
            print 'indexed', i
        if len(docs) > 100:
            pass
            solr.add(docs)
            docs = list()
        res = rows.fetch_row(how=1)

    if docs:
        pass
        solr.add(docs)

    solr.commit()
    index_status.indexed = i

    # удаление
    records = []

    if getattr(index_status, 'last_index_date', None):
        records = Record.objects.using('records').filter(
            deleted=True,
            update_date__gte=index_status.last_index_date
        ).values('gen_id')
    else:
        records = Record.objects.using('records').filter(deleted=True).values('gen_id', 'update_date')

    record_gen_ids = []
    for record in list(records):
        record_gen_ids.append(record['gen_id'])

    if record_gen_ids:
        solr.delete(record_gen_ids)
        solr.commit()

    index_status.deleted = len(record_gen_ids)
    index_status.last_index_date = start_index_date
    index_status.save()
    conn.query('DELETE FROM records WHERE deleted = 1')
    return True


@transaction.atomic
def local_records_indexing(request):
    slug = 'local_records'
    try:
        solr_address = settings.SOLR['local_records_host']
        db_conf = settings.DATABASES.get('local_records')
    except KeyError:
        raise Http404(u'Catalog not founded')

    if not db_conf:
        raise Exception(u'Settings not have inforamation about database, where contains records.')

    if db_conf['ENGINE'] != 'django.db.backends.mysql':
        raise Exception(u' Support only Mysql Database where contains records.')
    try:
        conn = MySQLdb.connect(
            host=db_conf['HOST'],
            user=db_conf['USER'],
            passwd=db_conf['PASSWORD'],
            db=db_conf['NAME'],
            port=int(db_conf['PORT']),
            charset='utf8',
            use_unicode=True,
            cursorclass=MySQLdb.cursors.SSDictCursor
        )
    except MySQLdb.OperationalError as e:
        conn = MySQLdb.connect(
            unix_socket=db_conf['HOST'],
            user=db_conf['USER'],
            passwd=db_conf['PASSWORD'],
            db=db_conf['NAME'],
            port=int(db_conf['PORT']),
            charset='utf8',
            use_unicode=True,
            cursorclass=MySQLdb.cursors.SSDictCursor
        )

    print 'indexing start',
    try:
        index_status = IndexStatus.objects.get(catalog=slug)
    except IndexStatus.DoesNotExist:
        index_status = IndexStatus(catalog=slug)

    if not getattr(index_status, 'last_index_date', None):
        select_query = "SELECT * FROM records where deleted = 0 and content != NULL"
    else:
        select_query = "SELECT * FROM records where update_date >= '%s' and deleted = 0 and content != NULL" % (
            str(index_status.last_index_date))

    print 'records finded',
    solr = sunburnt.SolrInterface(solr_address, http_connection=httplib2.Http(disable_ssl_certificate_validation=True))
    docs = list()

    start_index_date = datetime.datetime.now()

    conn.query(select_query)
    rows = conn.use_result()
    res = rows.fetch_row(how=1)
    print 'records fetched',
    i = 0
    while res:
        content = zlib.decompress(res[0]['content'], -15).decode('utf-8')
        doc_tree = etree.XML(content)
        doc_tree = xslt_indexing_transformer(doc_tree)
        doc = doc_tree_to_dict(doc_tree)
        doc = add_sort_fields(doc)

        # для сортировки по тому, извлекаем строку содержащую номер тома или промежуток и посещаем резултат вычисления
        # в поле tom_f, которое в последствии сортируется
        # если трока типа т.1 то в том добавляется float 1
        # если строка содержит т.1-2 то добавляется float (1+2) / 2 - средне арифметическое, чтобы усреднить для сортировки

        tom = doc.get('tom_s', None)
        if tom and isinstance(tom, unicode):
            tom = tom.strip().replace(u' ', u'')
            r = re_t1_t2.search(tom)
            if r:
                groups = r.groups()
                doc['tom_f'] = (int(groups[0]) + int(groups[1])) / 2.0
            else:
                r = re_t1.search(tom)
                if r:
                    doc['tom_f'] = float(r.groups()[0])
        try:
            record_create_date = doc.get('record-create-date_dt', None)
            # print 'record_create_date1', record_create_date
            if record_create_date:
                doc['record-create-date_dts'] = record_create_date
        except Exception as e:
            print 'Error record-create-date_dt', e.message

        doc['system-add-date_dt'] = res[0]['add_date']
        doc['system-add-date_dts'] = res[0]['add_date']
        doc['system-update-date_dt'] = res[0]['update_date']
        doc['system-update-date_dts'] = res[0]['update_date']
        doc['system-catalog_s'] = res[0]['source_id']

        if str(doc['system-catalog_s']) == '2':
            full_text_file = None
            #            doc['system-update-date_dt'] = res[0]['doc-id_s']
            urls = doc.get('doc-id_s', None)
            if urls and type(urls) == list:
                for url in doc.get('doc-id_s', None):
                    if url:
                        full_text_file = url.split('/')[-1]
            else:
                if urls:
                    full_text_file = urls.split('/')[-1]
            if full_text_file:
                text = full_text_extract(full_text_file)
                if text:
                    doc['full-text'] = text

        docs.append(doc)
        i += 1
        if len(docs) > 25:
            solr.add(docs)
            print i
            docs = list()
        res = rows.fetch_row(how=1)

    if docs:
        solr.add(docs)

    solr.commit()
    index_status.indexed = i

    # удаление
    records = []

    if getattr(index_status, 'last_index_date', None):
        records = Record.objects.using('records').filter(deleted=True,
                                                         update_date__gte=index_status.last_index_date).values('gen_id')
    else:
        records = Record.objects.using('records').filter(deleted=True).values('gen_id', 'update_date')

    record_gen_ids = []
    for record in list(records):
        record_gen_ids.append(record['gen_id'])

    if record_gen_ids:
        solr.delete(record_gen_ids)
        solr.commit()

    index_status.deleted = len(record_gen_ids)
    index_status.last_index_date = start_index_date
    index_status.save()
    conn.query('DELETE FROM records WHERE deleted = 1')
    return True


# распознование типа
resolvers = {
    'dt': resolve_date,
    'dts': resolve_date,
    'dtf': resolve_date,
}
# тип поля, которое может быть только одно в документе
origin_types = ['ts', 'ss', 'dts']


def doc_tree_to_dict(doc_tree):
    doc_dict = {}
    for element in doc_tree.getroot().getchildren():
        attrib = element.attrib['name']
        value = element.text

        # если поле пустое, пропускаем
        if not value: continue

        value_type = attrib.split('_')[-1]

        if value_type in resolvers:
            try:
                value = resolvers[value_type](value)
                if type(value) == tuple or type(value) == list and value:
                    value = value[0]
            except ValueError:
                # если значение не соответвует объявленному типу, то пропускаем
                continue

        old_value = doc_dict.get(attrib, None)

        # если неповторяемое поле было установленно ранее, пропускаем новое
        if old_value and value_type in origin_types:
            continue

        if not old_value:
            doc_dict[attrib] = [value]
        else:
            doc_dict[attrib].append(value)

    return doc_dict


replace_pattern = re.compile(ur'\W', re.UNICODE)


def add_sort_fields(doc):
    for key in doc.keys():
        splited_key = key.split('_')
        if len(splited_key) > 1:
            if (splited_key[-1] == 't' or splited_key[-1] == 's'):
                doc[key + 's'] = re.sub(replace_pattern, u'', u''.join(doc[key]))
            elif splited_key[-1] == 'dt':
                if type(doc[key]) == list:
                    doc[key + 's'] = doc[key][0]
                else:
                    doc[key + 's'] = doc[key]
            else:
                continue
    return doc


import zipfile


def full_text_extract(zip_file_name):
    #    zip_file_name = settings.EBOOKS_STORE + zip_file_name
    book_pathes = (
        settings.EBOOKS_STORE + zip_file_name + '.edoc',
        settings.EBOOKS_STORE + zip_file_name + '.2.edoc',
        settings.EBOOKS_STORE + zip_file_name + '.1.edoc',
    )

    book_file = None
    for book_path in book_pathes:
        if os.path.isfile(book_path):
            book_file = book_path

    if book_file:
        file = zipfile.ZipFile(book_file, "r")
        # читаем содержимое, попутно вырезая ять в коне слова
        text = file.read("Text.txt").decode('utf-8').replace(u'ъ ', u'').replace(u'ъ,', u',').replace(u'ъ.',
                                                                                                      u'.').replace(
            u'ъ:', u':').replace(u'ъ;', u';')
        file.close()
        return text
    return None


def _calculate_holdings_hash(record_id, source_id):
    return record_id
    # return binascii.crc32(record_id)
    # return hashlib.md5(record_id + str(source_id)).digest()


def _load_holdings(conn):
    select_query = "SELECT * FROM ssearch_holdings"
    # select_query = "SELECT * FROM ssearch_holdings WHERE record_id='ru\\\\nlrt\\\\1359411'"

    conn.query(select_query)
    rows = conn.use_result()
    holdings_index = {}
    res = rows.fetch_row(how=1)
    i = 0
    while res:
        if i % 100000 == 0:
            print i
        i += 1
        id = res[0]['id']
        record_id = res[0]['record_id']
        source_id = res[0]['source_id']
        department = _clean_sigla(res[0]['department'])
        hash = _calculate_holdings_hash(record_id, source_id)
        departments = holdings_index.get(hash, None)
        if not departments:
            departments = {}
            holdings_index[hash] = departments

        source_ids = departments.get(department, None)
        if not source_ids:
            source_ids = []
            departments[department] = source_ids
        source_ids.append(source_id)
        res = rows.fetch_row(how=1)
    return holdings_index


def _get_holdings(source_id, record_id, holdings_index, orgs_index, sources_index):
    holding_codes = set()
    department_siglas = holdings_index.get(_calculate_holdings_hash(record_id, source_id), {})

    for department_sigla, source_ids in department_siglas.items():
        for source_id in source_ids:
            code = _get_org_code_by_departament(
                orgs_index=orgs_index,
                sources_index=sources_index,
                source_id=source_id,
                department_sigla=department_sigla
            )
            if code:
                holding_codes.add(code)

    if not holding_codes:
        source = sources_index.get(source_id, None)
        if source:
            org = orgs_index['code'].get(source.organization_code, None)
            if org:
                for descendant in _get_org_leafs(org, orgs_index):
                    if descendant['default_holder']:
                        holding_codes.add(descendant['code'])
                        break
                if not holding_codes:
                    holding_codes.add(org['code'])

    return holding_codes


def _get_org_code_by_departament(orgs_index, sources_index, source_id, department_sigla):
    cleaned_sigla = _clean_sigla(department_sigla)
    exist_source = sources_index.get(source_id, None)
    if not exist_source:
        return ''
    organization_code = exist_source.organization_code
    organization = orgs_index['code'].get(organization_code, None)
    if not organization:
        return ''

    if _is_exist_sigla_in_org(organization, cleaned_sigla):
        return organization_code

    leaf_orgs = _get_org_leafs(organization, orgs_index)
    for leaf_org in leaf_orgs:
        if _is_exist_sigla_in_org(leaf_org, cleaned_sigla):
            return leaf_org['code']

    if organization['default_holder']:
        return organization_code

    for leaf_org in leaf_orgs:
        if leaf_org['default_holder']:
            return leaf_org['code']
    return organization_code


def _is_exist_sigla_in_org(organization, sigla):
    siglas = _extract_siglas(organization['sigla'])
    return sigla in siglas


def _load_sources():
    sources = list(Source.objects.using('records').all())
    sources_index = {}
    for source in sources:
        sources_index[source.id] = source
    return sources_index


def _get_org_ancestors(org, orgs_index):
    ancestors = []
    parent_id = org['parent_id']
    while parent_id:
        parent_org = orgs_index['id'].get(parent_id, None)
        if not parent_org:
            break
        ancestors.append(parent_org)
        parent_id = parent_org['id']
    return ancestors


def _get_org_children(org, orgs_index):
    children = []
    for child_org in orgs_index['parent_id'].get(org['id'], []):
        children.append(child_org)
    return children


def _get_org_leafs(org, org_index):
    leafs = []
    for child in _get_org_children(org, org_index):
        leafs.append(child)
        leafs += _get_org_leafs(child, org_index)
    return leafs


def _load_orgs():
    orgs = Library.objects.values('id', 'parent_id', 'code', 'sigla', 'default_holder', 'name', 'org_type').all()
    orgs_index = {
        'id': {},
        'parent_id': {},
        'code': {},
        'sigla': {}
    }
    for org in orgs:
        orgs_index['id'][org['id']] = org
        if org['parent_id']:
            orgs = orgs_index['parent_id'].get(org['parent_id'], None)
            if not orgs:
                orgs = []
                orgs_index['parent_id'][org['parent_id']] = orgs
            orgs.append(org)
        orgs_index['code'][org['code']] = org
        if org['sigla']:
            for sigla in _extract_siglas(org['sigla']):
                orgs_index['code'][org['code'] + _clean_sigla(sigla)] = org
    return orgs_index


def _clean_sigla(sigla):
    return sigla.strip().lower()


def _extract_siglas(siglas_str):
    cleaned_siglas = []
    for sigla in siglas_str.strip().replace("\r", "").split(SIGLA_DELIMITER):
        cleaned_sigla = _clean_sigla(sigla)
        if cleaned_sigla:
            cleaned_siglas.append(cleaned_sigla)
    return cleaned_siglas
