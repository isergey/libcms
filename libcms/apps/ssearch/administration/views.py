# coding: utf-8
import MySQLdb
import zlib
import re
import datetime
import hashlib
import sunburnt
from lxml import etree
from django.conf import settings
from django.core.files.storage import default_storage
from forms import UploadForm
from ssearch.models import Upload, Record, Ebook, IndexStatus
from django.shortcuts import render, redirect, HttpResponse, Http404
from pymarc2 import reader, record, field, marcxml
from django.db import transaction#, connection, connections




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

#Our initial page
def initial(request):
    return render(request, 'ssearch/administration/upload.html', {
        'form': UploadForm(),
        })


#Our file upload handler that the form will post to
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


@transaction.commit_on_success
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
        gen_id =  unicode(hashlib.md5(record.as_marc()).hexdigest())
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

xslt_root = etree.parse('libcms/xsl/record_indexing.xsl')
xslt_transformer = etree.XSLT(xslt_root)


def xml_to_dict(doc_tree):
    for el in doc_tree.get_root():
        print el

def indexing(request):
    reset = request.GET.get('reset', u'0')
    if reset == u'1':
        reset = True
    else:
        reset = False

    for slug in settings.SOLR['catalogs'].keys():
        _indexing(slug, reset)
        break

    return HttpResponse('Ok')



# регулярки, с помощью которых вычленяются номера томов
re_t1_t2 = re.compile(ur"(?P<t1>\d+)\D+(?P<t2>\d+)" ,re.UNICODE)
re_t1 = re.compile(ur"(?P<t1>\d+)" ,re.UNICODE)

@transaction.commit_on_success
def _indexing(slug, reset=False):


    try:
        solr_address = settings.SOLR['host']
        db_conf =  settings.DATABASES.get(settings.SOLR['catalogs'][slug]['database'], None)
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
            port=int(db_conf['PORT']
            ),
            cursorclass =MySQLdb.cursors.SSDictCursor
        )
    except MySQLdb.OperationalError as e:
        conn = MySQLdb.connect(
            unix_socket=db_conf['HOST'],
            user=db_conf['USER'],
            passwd=db_conf['PASSWORD'],
            db=db_conf['NAME'],
            port=int(db_conf['PORT']
            ),
            cursorclass =MySQLdb.cursors.SSDictCursor
        )


    try:
        index_status = IndexStatus.objects.get(catalog=slug)
    except IndexStatus.DoesNotExist:
        index_status = None

    if not index_status and not reset:
        index_status = IndexStatus(catalog=slug)
        select_query = "SELECT * FROM %s where deleted = 0" % (settings.SOLR['catalogs'][slug]['table'],)
    elif reset:
        select_query = "SELECT * FROM %s where deleted = 0" % (settings.SOLR['catalogs'][slug]['table'],)
    else:
        select_query = "SELECT * FROM %s where (update_date > '%s' or  update_date = '%s') and deleted = 0" % \
                       (
                           settings.SOLR['catalogs'][slug]['table'],
                           str(index_status.last_index_date),
                           str(index_status.last_index_date)
                           )


    solr = sunburnt.SolrInterface(solr_address)
    docs = list()

    start_index_date = datetime.datetime.now()

    conn.query(select_query)
    rows=conn.use_result()
    res = rows.fetch_row(how=1)

    i=0
    while res:
        content = zlib.decompress(res[0]['content'],-15).decode('utf-8')
        doc_tree = etree.XML(content)
        doc_tree = xslt_transformer(doc_tree)
        doc = doc_tree_to_dict(doc_tree)
        doc = add_sort_fields(doc)

        # для сортировки по тому, извлекаем строку содержащую номер тома или промежуток и посещаем резултат вычисления
        # в поле tom_f, которое в последствии сортируется
        # если трока типа т.1 то в том добавляется float 1
        # если строка содержит т.1-2 то добавляется float (1+2) / 2 - средне арифметическое, чтобы усреднить для сортировки

        tom = doc.get('tom_s', None)
        if tom and isinstance(tom, unicode):
            tom = tom.strip().replace(u' ',u'')
            r = re_t1_t2.search(tom)
            if r:
                groups = r.groups()
                doc['tom_f'] = (int(groups[0]) + int(groups[1])) / 2.0
            else:
                r = re_t1.search(tom)
                if r:
                    doc['tom_f'] = float(r.groups()[0])

        doc['system-add-date_dt'] = res[0]['add_date']
        doc['system-update-date_dt'] = res[0]['update_date']
        doc['system-catalog_s'] = slug




        if slug == 'ebooks':
            full_text_file =None
#            doc['system-update-date_dt'] = res[0]['doc-id_s']
            urls = doc.get('doc-id_s', None)
            if urls and type(urls) == list:
                for url in doc.get('doc-id_s', None):
                    full_text_file =  url.split('/')[-1]
            else:
                full_text_file =  urls.split('/')[-1]
            if full_text_file:
                text =  full_text_extract(full_text_file)
                if text:
                    doc['full-text'] = text
        docs.append(doc)
        i+=1
        if len(docs) > 200:
            print i
            solr.add(docs)
            docs = list()

        res = rows.fetch_row(how=1)

    if docs:
        solr.add(docs)

    solr.commit()
    index_status.indexed = i

    # удаление
    records = []
    if slug == 'sc2':
        if IndexStatus(catalog=slug).last_index_date:
            records = Record.objects.using('records').filter(deleted=True, update_date__gte=index_status.last_index_date).values('gen_id')
        else:
            records = Record.objects.using('records').filter(deleted=True).values('gen_id')
    if slug == 'ebooks':
        if IndexStatus(catalog=slug).last_index_date:
            records = Ebook.objects.using('records').filter(deleted=True, update_date__gte=index_status.last_index_date).values('gen_id')
        else:
            records = Ebook.objects.using('records').filter(deleted=True).values('gen_id')


    record_gen_ids = []
    for record in records:
        record_gen_ids.append(record['gen_id'])


    if record_gen_ids:
        solr.delete(record_gen_ids)
        solr.commit()

    index_status.deleted = len(record_gen_ids)
    index_status.last_index_date = start_index_date
    index_status.save()

    return True


from ..common import resolve_date
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

        #если поле пустое, пропускаем
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
            doc_dict[attrib] = value
        elif type(old_value) != list:
            doc_dict[attrib] = [doc_dict[attrib], value]
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
    try:
#        print settings.EBOOKS_STORE + zip_file_name + '.edoc'
        file = zipfile.ZipFile( settings.EBOOKS_STORE + zip_file_name + '.edoc', "r")
        # читаем содержимое, попутно вырезая ять в коне слова
        text =  file.read("Text.txt").decode('utf-8').replace(u'ъ ', u'').replace(u'ъ,', u',').replace(u'ъ.', u'.').replace(u'ъ:', u':').replace(u'ъ;', u';')
        file.close()
        return text
    except IOError:
        return None


