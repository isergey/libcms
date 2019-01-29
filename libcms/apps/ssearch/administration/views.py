# coding: utf-8
import datetime
import hashlib
import json
import sys
import zlib

import MySQLdb
import httplib2
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.db import transaction  # , connection, connections
from django.shortcuts import render, redirect, HttpResponse, Http404
from guardian.decorators import permission_required_or_403
from lxml import etree

import sunburnt
from forms import AttributesForm, GroupForm, PeriodForm, CatalogForm
from forms import UploadForm
from libcms.libs.common.xslt_transformers import xslt_indexing_transformer
from pymarc2 import reader, record, field, marcxml
from ssearch.models import Upload, Record, IndexStatus
from ..models import requests_count, requests_by_attributes, requests_by_term
from .. import tasks

BASE_PATH = getattr(settings, 'PROJECT_PATH')

from ..indexing import doc_tree_to_dict, full_text_extract, add_sort_fields, re_t1_t2, re_t1


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
        # _indexing(slug, reset)
        tasks.indexing(slug, reset)
    return HttpResponse('Ok')


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
