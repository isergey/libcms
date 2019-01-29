# coding=utf-8
import re
import io
import datetime
import sunburnt
import MySQLdb
import zipfile
import httplib2
import os
from lxml import etree
from django.db import transaction
from django.conf import settings
from participants.models import Library
from ssearch.models import Upload, Record, IndexStatus
from .models import requests_count, requests_by_attributes, requests_by_term, Source
from libcms.libs.common.xslt_transformers import xslt_indexing_transformer
from .common import resolve_date

ONLY_DIGITS_RE = re.compile('\d+')

SIGLA_DELIMITER = "\n"

replace_pattern = re.compile(ur'\W', re.UNICODE)

# распознование типа
resolvers = {
    'dt': resolve_date,
    'dts': resolve_date,
    'dtf': resolve_date,
}

# тип поля, которое может быть только одно в документе
origin_types = ['ts', 'ss', 'dts']

# регулярки, с помощью которых вычленяются номера томов
re_t1_t2 = re.compile(ur"(?P<t1>\d+)\D+(?P<t2>\d+)", re.UNICODE)
re_t1 = re.compile(ur"(?P<t1>\d+)", re.UNICODE)


def _clean_sigla(sigla):
    return sigla.strip().lower()


def _extract_siglas(siglas_str):
    cleaned_siglas = []
    for sigla in siglas_str.strip().replace("\r", "").split(SIGLA_DELIMITER):
        cleaned_sigla = _clean_sigla(sigla)
        if cleaned_sigla:
            cleaned_siglas.append(cleaned_sigla)
    return cleaned_siglas


def _is_exist_sigla_in_org(organization, sigla):
    siglas = _extract_siglas(organization['sigla'])
    return sigla in siglas


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


def _get_org_leafs(org, org_index):
    leafs = []
    for child in _get_org_children(org, org_index):
        leafs.append(child)
        leafs += _get_org_leafs(child, org_index)
    return leafs


def _get_org_children(org, orgs_index):
    children = []
    for child_org in orgs_index['parent_id'].get(org['id'], []):
        children.append(child_org)
    return children


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
        text = file.read("Text.txt").decode('utf-8') \
            .replace(u'ъ ', u'') \
            .replace(u'ъ,', u',') \
            .replace(u'ъ.', u'.') \
            .replace(u'ъ:', u':') \
            .replace(u'ъ;', u';')
        file.close()
        return text
    return None


@transaction.atomic
def _indexing(slug, reset=False):
    sources_index = {}

    print 'getting source'
    sources = list(Source.objects.using('records').all())

    print 'total sources', len(sources)
    for source in sources:
        sources_index[source.id] = source

    try:
        solr_address = settings.SOLR['host']
        db_conf = settings.DATABASES.get(settings.SOLR['catalogs'][slug]['database'], None)
    except KeyError:
        raise Exception(u'Catalog not founded')

    if not db_conf:
        raise Exception(u'Settings not have inforamation about database, where contains records.')

    if db_conf['ENGINE'] != 'django.db.backends.mysql':
        raise Exception(u' Support only Mysql Database where contains records.')

    print 'connect to db', db_conf['HOST']
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

    print 'connected to db'

    print 'load holdings'
    holdings_index = _load_holdings(conn)

    print 'load orgs'
    orgs_index = _load_orgs()

    print 'load sources'
    sources_index = _load_sources()

    try:
        index_status = IndexStatus.objects.get(catalog=slug)
    except IndexStatus.DoesNotExist:
        index_status = IndexStatus(catalog=slug)

    print 'index_status', index_status.last_index_date
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
    print 'execute query', select_query
    conn.query(select_query)
    print 'query executed', select_query

    rows = conn.use_result()

    res = rows.fetch_row(how=1)
    print 'start fetching'

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

        date_of_publication = doc.get('date-of-publication_s')
        if date_of_publication:
            cleaned_date_of_publication = ''.join(ONLY_DIGITS_RE.findall(date_of_publication[0]))
            if cleaned_date_of_publication:
                doc.doc['date_of_publication_ls'] = [cleaned_date_of_publication]
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
