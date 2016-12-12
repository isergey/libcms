# coding: utf-8
import io
from collections import OrderedDict
import datetime
import zlib
import zipfile
from django.db import connection
from django.db import models
from django.contrib.auth.models import User

RECORD_SCHEMES = (
    ('rusmarc', u"Rusmarc"),
    ('usmarc', u"Usmarc"),
    ('unimarc', u"Unimarc"),
)

RECORD_FORMATS = (
    ('iso2709', u"ISO 2709"),
    ('xml', u"XML"),
)

RECORD_ENCODINGS = (
    ('utf-8', u"UTF-8"),
    ('cp1251', u"Windows 1251"),
    ('koi8-r', u"koi8-r"),
    ('latin-1', u"Unimarc"),
    ('marc8', u"Marc 8"),
)


class Upload(models.Model):
    """Uploaded files."""
    file = models.FileField(upload_to='uploads', )
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    records_scheme = models.CharField(max_length=16, choices=RECORD_SCHEMES, default='rusmarc')
    records_format = models.CharField(max_length=16, choices=RECORD_FORMATS, default='iso2709')
    records_encodings = models.CharField(max_length=16, choices=RECORD_ENCODINGS, default='utf-8')

    notes = models.CharField(max_length=255, blank=True)
    processed = models.BooleanField(default=False, db_index=True)
    success = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ['-timestamp', ]

    def __unicode__(self):
        return unicode(self.file)

    @property
    def size(self):
        return filesizeformat(self.file.size)


class Source(models.Model):
    source_type = models.CharField(max_length=32)
    organization_code = models.CharField(max_length=32)
    database_group = models.CharField(max_length=32)
    databse_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'source'


class ZippedTextField(models.BinaryField):
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        zf = zipfile.ZipFile(io.BytesIO(value))
        value = zf.read('1.xml')
        return value

    def get_db_prep_save(self, value, connection):
        if isinstance(value, unicode):
            value.encode('utf-8')
        value = zlib.compress(value)
        if value is None:
            return None
        return value

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return value


class IndexStatus(models.Model):
    catalog = models.CharField(max_length=32, unique=True)
    last_index_date = models.DateTimeField()
    indexed = models.IntegerField(default=0)
    deleted = models.IntegerField(default=0)


class Record(models.Model):
    source = models.ForeignKey(Source, null=True, blank=True)
    gen_id = models.CharField(max_length=32, unique=True)
    record_id = models.CharField(max_length=32, db_index=True)
    scheme = models.CharField(max_length=16, choices=RECORD_SCHEMES, default='rusmarc', verbose_name=u"Scheme")
    content = ZippedTextField(verbose_name=u'Xml content', null=True)
    add_date = models.DateTimeField(auto_now_add=True, db_index=True)
    update_date = models.DateTimeField(auto_now_add=True, db_index=True)
    deleted = models.BooleanField(default=False)
    hash = models.TextField(max_length=16)

    def __unicode__(self):
        return self.record_id

    class Meta:
        db_table = 'records'


class Holdings(models.Model):
    original_id = models.CharField(max_length=255, db_index=True)
    department = models.CharField(max_length=255, db_index=True)
    source = models.CharField(max_length=32, db_index=True)

    class Meta:
        managed = False
        unique_together = ['original_id', 'department', 'source']
        index_together = ['original_id', 'department', 'source']
        db_table = 'ssearch_holdings'



class Ebook(models.Model):
    source = models.ForeignKey(Source, null=True, blank=True)
    gen_id = models.CharField(max_length=32, unique=True)
    record_id = models.CharField(max_length=32, db_index=True)
    scheme = models.CharField(max_length=16, choices=RECORD_SCHEMES, default='rusmarc', verbose_name=u"Scheme")
    content = ZippedTextField(verbose_name=u'Xml content', null=True)
    add_date = models.DateTimeField(auto_now_add=True, db_index=True)
    update_date = models.DateTimeField(auto_now_add=True, db_index=True)
    deleted = models.BooleanField(default=False)
    hash = models.TextField(max_length=16)

    def __unicode__(self):
        return self.record_id

    class Meta:
        db_table = 'ebooks'

def get_records(doc_ids=[]):
    records_dict = {}
    records = list(Record.objects.using('records').filter(gen_id__in=doc_ids).exclude(content=None))

    for record in records:
        records_dict[record.gen_id] = record

    result_records = []
    for doc_id in doc_ids:
        rec = records_dict.get(doc_id)
        if rec:
            result_records.append(rec)

    return result_records


class Collection(models.Model):
    source = models.ForeignKey(Source, null=True, blank=True)
    gen_id = models.CharField(max_length=32, unique=True)
    record_id = models.CharField(max_length=32, db_index=True)
    scheme = models.CharField(max_length=16, choices=RECORD_SCHEMES, default='rusmarc', verbose_name=u"Scheme")
    content = ZippedTextField(verbose_name=u'Xml content')
    add_date = models.DateTimeField(auto_now_add=True, db_index=True)
    update_date = models.DateTimeField(auto_now_add=True, db_index=True)
    deleted = models.BooleanField(default=False)
    hash = models.TextField(max_length=16)

    def __unicode__(self):
        return self.record_id

    class Meta:
        db_table = 'collections'


class DetailAccessLog(models.Model):
    gen_id = models.CharField(max_length=64, db_index=True,
                              verbose_name=u'Документ, к которому было произведено обращение')
    catalog = models.CharField(max_length=32, db_index=True, verbose_name=u'Каталог, в котором находиться документ')
    date_time = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name=u'Время обращения')


class SavedRequest(models.Model):
    user = models.ForeignKey(User, related_name='saved_request_user')
    search_request = models.CharField(max_length=1024)
    catalog = models.CharField(max_length=64, blank=True, null=True)
    add_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"%s %s %s" % (self.search_request, self.catalog, unicode(self.add_time))


class SearchRequestLog(models.Model):
    catalog = models.CharField(max_length=32, null=True, db_index=True)
    library_code = models.CharField(max_length=32, db_index=True, blank=True)
    search_id = models.CharField(max_length=32, verbose_name=u'Идентификатор запроса', db_index=True)
    use = models.CharField(max_length=32, verbose_name=u"Точка доступа", db_index=True)
    not_normalize = models.CharField(max_length=256, verbose_name=u'Ненормализованный терм', db_index=True)
    datetime = models.DateTimeField(auto_now_add=True, db_index=True)





DUBLET_STATUSES = (
    (0, u'На обработке'),
    (1, u'Обработан'),
)


class Dublet(models.Model):
    key = models.CharField(verbose_name=u'Ключ дублетности', db_index=True, unique=True, max_length=128)
    statuc = models.IntegerField(choices=DUBLET_STATUSES, db_index=True)
    change_date = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=u"Время изменения статуса")
    owner = models.ForeignKey(User)


CATALOGS_CHOICES = (
    ('records', u'Сводный'),
    ('ebooks', u'Электронная библиотека'),
)


class WrongRecord(models.Model):
    gen_id = models.CharField(max_length=32, unique=True)
    record_id = models.CharField(max_length=32, db_index=True)
    key = models.CharField(verbose_name=u'Ключ дублетности', db_index=True, unique=True, max_length=128)
    sender = models.ForeignKey(User)
    catalog = models.CharField(choices=CATALOGS_CHOICES, db_index=True, max_length=16)
    send_date = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=u"Время добавления статуса")


DEFAULT_LANG_CHICES = (
    ('rus', u'Русский'),
    ('eng', u'English'),
    ('tat', u'Татарский'),
)

ATTRIBUTES = {
    'fond': u'Коллекция',
    'title': u'Заглавие',
    'author': u'Автор',
    'content-type': u'Тип содержания',
    'date-of-publication': u'Год публикации',
    'subject-heading': u'Тематика',
    'anywhere': u'Везде',
    'code-language': u'Язык',
    'text': u'Везде',
    'full-text': u'Полный текст',
}


def dictfetchall(cursor):
    """Returns all rows from a cursor as a dict"""
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
        ]


def execute(query, params):
    cursor = connection.cursor()
    cursor.execute(query, params)
    return dictfetchall(cursor)


def get_search_attributes_in_log():
    select = """
    SELECT
         ssearch_searchrequestlog.use as attribute
    FROM
        ssearch_searchrequestlog
    GROUP BY
        ssearch_searchrequestlog.use
    """
    results = execute(select, [])
    choices = []

    for row in results:
        choices.append(
            (
                row['attribute'],
                ATTRIBUTES.get(row['attribute'], row['attribute'])
            )
        )

    return choices


def date_group(group):
    group_by = ['YEAR(datetime)']

    if group > u'0':
        group_by.append('MONTH(datetime)')

    if group > u'1':
        group_by.append('DAY(datetime)')

    group_by = 'GROUP BY ' + ', '.join(group_by)

    return group_by


def requests_count(start_date=None, end_date=None, group=u'2', catalogs=list(), library_code=''):
    """
    Статистика по количеству запросов в каталог(и)
    """
    if not start_date:
        start_date = datetime.datetime.now()

    if not end_date:
        end_date = datetime.datetime.now()

    start_date = start_date.strftime('%Y-%m-%d 00:00:00')
    end_date = end_date.strftime('%Y-%m-%d 23:59:59')

    group_by = date_group(group)

    select = """
        SELECT
            count(ssearch_searchrequestlog.use) as count, ssearch_searchrequestlog.datetime as datetime
        FROM
            ssearch_searchrequestlog
    """
    params = []
    where = ['WHERE date(datetime) BETWEEN %s  AND  %s']

    params.append(start_date)
    params.append(end_date)

    if catalogs:
        if len(catalogs) == 1:
            where.append('AND ' + 'ssearch_searchrequestlog.catalog = "%s" ' % catalogs[0])
        else:
            catalogs_where = []
            for catalog in catalogs:
                catalogs_where.append(' ssearch_searchrequestlog.catalog = "%s" ' % catalog)
            where.append('AND (' + u'OR'.join(catalogs_where) + ')')

    where = u' '.join(where)
    results = execute(select + where + group_by, params)

    rows = []
    format = '%d.%m.%Y'
    if group == u'0':
        format = '%Y'
    if group == u'1':
        format = '%m.%Y'
    if group == u'2':
        format = '%d.%m.%Y'

    for row in results:
        rows.append((row['datetime'].strftime(format), row['count']))
    return rows


def requests_by_attributes(start_date=None, end_date=None, attributes=list(), catalogs=list()):
    if not start_date:
        start_date = datetime.datetime.now()

    if not end_date:
        end_date = datetime.datetime.now()

    start_date = start_date.strftime('%Y-%m-%d 00:00:00')
    end_date = end_date.strftime('%Y-%m-%d 23:59:59')

    select = u"""
        SELECT
            count(ssearch_searchrequestlog.use) as count, ssearch_searchrequestlog.use as attribute
        FROM
            ssearch_searchrequestlog
    """
    params = []

    where = ['WHERE date(datetime) BETWEEN %s  AND  %s']
    params.append(start_date)
    params.append(end_date)

    if catalogs:
        if len(catalogs) == 1:
            where.append('AND ' + 'ssearch_searchrequestlog.catalog = "%s" ' % catalogs[0])
        else:
            catalogs_where = []
            for catalog in catalogs:
                catalogs_where.append(' ssearch_searchrequestlog.catalog = "%s" ' % catalog)
            where.append('AND (' + u'OR'.join(catalogs_where) + ')')

    if attributes:
        attributes_args = []
        for attribute in attributes:
            attributes_args.append(u'%s')
            params.append(attribute)

        attributes_args = u', '.join(attributes_args)
        where.append('AND ssearch_searchrequestlog.use in (%s)' % attributes_args)

    where = u' '.join(where)

    results = execute(
        select + ' ' + where +
        u"""
        GROUP BY
            ssearch_searchrequestlog.use
        ORDER BY
            count desc;
        """,
        params
    )

    rows = []

    for row in results:
        rows.append((ATTRIBUTES.get(row['attribute'], row['attribute']), row['count']))
    return rows


def requests_by_term(start_date=None, end_date=None, attributes=list(), catalogs=list()):
    if not start_date:
        start_date = datetime.datetime.now()

    if not end_date:
        end_date = datetime.datetime.now()

    start_date = start_date.strftime('%Y-%m-%d 00:00:00')
    end_date = end_date.strftime('%Y-%m-%d 23:59:59')

    select = u"""
        SELECT
            count(ssearch_searchrequestlog.not_normalize) as count, ssearch_searchrequestlog.not_normalize as not_normalize
        FROM
            ssearch_searchrequestlog
    """
    params = []

    where = [u'WHERE date(datetime) BETWEEN %s  AND  %s']
    params.append(start_date)
    params.append(end_date)

    if catalogs:
        if len(catalogs) == 1:
            where.append('AND ' + 'ssearch_searchrequestlog.catalog = "%s" ' % catalogs[0])
        else:
            catalogs_where = []
            for catalog in catalogs:
                catalogs_where.append(' ssearch_searchrequestlog.catalog = "%s" ' % catalog)
            where.append('AND (' + u'OR'.join(catalogs_where) + ')')

    if attributes:
        attributes_args = []
        for attribute in attributes:
            attributes_args.append(u'%s')
            params.append(attribute)

        attributes_args = u', '.join(attributes_args)
        where.append(u'AND ssearch_searchrequestlog.use in (%s)' % attributes_args)

    where = u' '.join(where)

    results = execute(
        'select not_normalize, count from (' + select + ' ' + where +
        u"""
        GROUP BY
            ssearch_searchrequestlog.not_normalize
        ORDER BY
            count desc
        LIMIT 100) as res where res.count > 1;
        """,
        params
    )

    rows = []

    for row in results:
        rows.append((row['not_normalize'], row['count']))
    return rows


def request_group_by_date(from_date, to_date, period, catalog='', library_code=''):
    date_range = _generate_dates(from_date, to_date, period)

    group_by = 'date'
    date_format = "to_char(datetime, 'YYYY-MM-DD')"
    if period == 'y':
        date_format = "to_char(datetime, 'YYYY-01-01')"
    elif period == 'm':
        date_format = "to_char(datetime, 'YYYY-MM-01')"
    else:
        pass

    cursor = connection.cursor()
    args = []
    select = """count(distinct search_id) as count, %s as date""" % (date_format)
    frm = 'ssearch_searchrequestlog'
    where = 'datetime >= %s AND datetime < %s'
    args += [from_date, to_date + datetime.timedelta(days=1)]
    if library_code:
        where += ' AND library_code = %s'
        args.append(library_code)

    if catalog:
        where += " AND catalog = %s"
        args.append(catalog)
    else:
        where += " AND catalog is null"
    query = u' '.join(['SELECT', select, 'FROM', frm, 'WHERE', where, 'GROUP BY', group_by])

    cursor.execute(query, args)
    row_hash = OrderedDict()

    for row in dictfetchall(cursor):
        row_hash[row['date']] = row['count']

    results = []
    for date in date_range:
        results.append({
            'date': date,
            'count': row_hash.get(date, 0)
        })
    return results


def _generate_dates(from_date, to_date, period):
    date_range = []
    if period == 'y':
        for year in range(from_date.year, to_date.year) + [to_date.year]:
            date_range.append(u'%s-01-01' % year)
    elif period == 'm':
        for date in _monthrange(from_date, to_date):
            date_range.append(date.strftime('%Y-%m-01'))
    else:
        for date in _daysrange(from_date, to_date):
            date_range.append(date.strftime('%Y-%m-%d'))

    return date_range


def _monthrange(start, finish):
    months = (finish.year - start.year) * 12 + finish.month + 1
    for i in xrange(start.month, months):
        year = (i - 1) / 12 + start.year
        month = (i - 1) % 12 + 1
        yield datetime.date(year, month, 1)


def _daysrange(start, end):
    dates = []
    delta = end - start
    for i in range(delta.days + 1):
        dates.append(start + datetime.timedelta(days=i))
    return dates
