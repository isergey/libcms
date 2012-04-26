# coding: utf-8
import datetime
import zlib
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
    title = models.CharField(max_length=256, verbose_name=u"Source title")
    index_rule = models.TextField(verbose_name=u"Index rule")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name=u"Add date")

    def __unicode__(self):
        return self.title


class ZippedTextField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.postgresql_psycopg2' or connection.settings_dict['ENGINE'] == 'django.db.backends.postgresql':
            return 'bytea'
        else:
            return 'BLOB'

    def to_python(self, value):
        try:
            value = zlib.decompress(value,-15)
            value = value.decode('utf-8')
        except zlib.error:
            pass
        return value


    def get_db_prep_save(self, value, connection):
        if isinstance(value, unicode):
            value.encode('utf-8')
        value = zlib.compress(value)
        if value is None:
            return None
        if connection.settings_dict['ENGINE'] == 'django.db.backends.postgresql_psycopg2' or connection.settings_dict['ENGINE'] == 'django.db.backends.postgresql':
            return psycopg2.Binary(value)
        else:
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
    content = ZippedTextField(verbose_name=u'Xml content')
    add_date = models.DateTimeField(auto_now_add=True, db_index=True)
    update_date = models.DateTimeField(auto_now_add=True, db_index=True)
    deleted= models.BooleanField()
    hash = models.TextField(max_length=16)
    def __unicode__(self):
        return self.record_id
    class Meta:
        db_table = 'sc2'


class Ebook(models.Model):
    source = models.ForeignKey(Source, null=True, blank=True)
    gen_id = models.CharField(max_length=32, unique=True)
    record_id = models.CharField(max_length=32, db_index=True)
    scheme = models.CharField(max_length=16, choices=RECORD_SCHEMES, default='rusmarc', verbose_name=u"Scheme")
    content = ZippedTextField(verbose_name=u'Xml content')
    add_date = models.DateTimeField(auto_now_add=True, db_index=True)
    update_date = models.DateTimeField(auto_now_add=True, db_index=True)
    deleted= models.BooleanField()
    hash = models.TextField(max_length=16)
    def __unicode__(self):
        return self.record_id
    class Meta:
        db_table = 'ebooks'




class SavedRequest(models.Model):
    user = models.ForeignKey(User, related_name='saved_request_user')
    search_request = models.CharField(max_length=1024)
    add_time = models.DateTimeField(auto_now_add=True)





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




def requests_count(start_date=None, end_date=None, group=u'2', catalogs=list()):
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
            where.append('AND ' + 'ssearch_searchrequestlog.catalog = "%s" ' % catalog  )
        else:
            catalogs_where = []
            for catalog in catalogs:
                catalogs_where.append(' ssearch_searchrequestlog.catalog = "%s" ' % catalog)
            where.append('AND (' + u'OR'.join(catalogs_where) + ')' )
#        print catalog
#        catalog_ids = []
#        for catalog in catalogs:
#            catalog_ids.append(unicode(catalog))
#        catalog_ids = u', '.join(catalog_ids)
#        print u', '.join(catalogs)
#        print ' AND ssearch_searchrequestlog.catalog in (%s)' % u', '.join(catalogs)
#        where.append(' AND ssearch_searchrequestlog.catalog in (%s)' % u', '.join(catalogs))

    where = u' '.join(where)
    results = execute( select + where + group_by, params)



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
        for catalog in catalogs:
            where.append(' AND ssearch_searchrequestlog.catalog = "%s"' % catalog)

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
            count(ssearch_searchrequestlog.not_normalize) as count, ssearch_searchrequestlog.not_normalize as normalize
        FROM
            ssearch_searchrequestlog
    """
    params = []




    where = [u'WHERE date(datetime) BETWEEN %s  AND  %s']
    params.append(start_date)
    params.append(end_date)


    if catalogs:
        if len(catalogs) == 1:
            where.append('AND ' + 'ssearch_searchrequestlog.catalog = "%s" ' % catalog  )
        else:
            catalogs_where = []
            for catalog in catalogs:
                catalogs_where.append(' ssearch_searchrequestlog.catalog = "%s" ' % catalog)
            where.append('AND (' + u'OR'.join(catalogs_where) + ')' )

    if attributes:
        attributes_args = []
        for attribute in attributes:
            attributes_args.append(u'%s')
            params.append(attribute)

        attributes_args = u', '.join(attributes_args)
        where.append(u'AND ssearch_searchrequestlog.use in (%s)' % attributes_args)

    where = u' '.join(where)

    results = execute(
        'select normalize, count from (' + select + ' ' + where +
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
        rows.append((row['normalize'], row['count']))
    return rows


class SearchRequestLog(models.Model):
    catalog = models.CharField(max_length=32, null=True, db_index=True)
    search_id = models.CharField(max_length=32, verbose_name=u'Идентификатор запроса', db_index=True)
    use = models.CharField(max_length=32, verbose_name=u"Точка доступа", db_index=True)
    normalize = models.CharField(max_length=256, verbose_name=u'Нормализованный терм', db_index=True)
    not_normalize = models.CharField(max_length=256, verbose_name=u'Ненормализованный терм', db_index=True)
    datetime = models.DateTimeField(auto_now_add=True, auto_now=True, db_index=True)