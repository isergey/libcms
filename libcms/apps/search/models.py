# coding=utf-8
from django.conf import settings
import datetime
import uuid
from django.db import models, connection
from django.contrib.auth.models import User
import titles

DB_CONNECTION = getattr(settings, 'SEARCH', {}).get('db_connection', 'default')


class Records(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    original_id = models.CharField(max_length=32)
    hash = models.CharField(max_length=32)
    source = models.CharField(max_length=32)
    record_scheme = models.CharField(max_length=32)
    format = models.CharField(max_length=32)
    session_id = models.BigIntegerField()
    create_date = models.DateTimeField()
    update_date = models.DateTimeField()
    deleted = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'records'


class RecordsContent(models.Model):
    record = models.ForeignKey(Records, primary_key=True)
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'records_content'


# class Holdings(models.Model):
#     original_id = models.CharField(max_length=255, db_index=True)
#     department = models.CharField(max_length=255, db_index=True)
#     source = models.CharField(max_length=32, db_index=True)
#
#     class Meta:
#         unique_together = ['record_id', 'department_sigla', 'source']


def get_records(ids=list()):
    records = list(RecordsContent.objects.using(DB_CONNECTION).filter(record_id__in=ids))
    records_dict = {}
    for record in records:
        records_dict[record.record_id] = record
    result_records = []
    for id in ids:
        record = records_dict.get(id, None)
        if not record: continue
        result_records.append(record)
    return result_records


ACTION_CHOICES = (
    ('detail', u'Детальная информация'),
    ('full_text', u'Просмотр полного текста'),
)


class DetailAccessLog(models.Model):
    record_id = models.CharField(
        max_length=64, db_index=True,
        verbose_name=u'Документ, к которому было произведено обращение'
    )
    action = models.CharField(max_length=64, db_index=True, verbose_name=u'Действие', choices=ACTION_CHOICES)
    user = models.ForeignKey(User, null=True, blank=True)
    # catalog = models.CharField(max_length=32, db_index=True, verbose_name=u'Каталог, в котором находиться документ', blank=True)
    date_time = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name=u'Время обращения')


class SavedRequest(models.Model):
    user = models.ForeignKey(User, related_name='saved_request_user')
    search_request = models.CharField(max_length=1024)
    add_time = models.DateTimeField(auto_now_add=True)


# #####################################################################################################################

class SearchRequestLog(models.Model):
    catalog = models.CharField(max_length=32, null=True, db_index=True)
    search_id = models.CharField(max_length=32, verbose_name=u'Идентификатор запроса', db_index=True)
    use = models.CharField(max_length=32, verbose_name=u"Точка доступа", db_index=True)
    normalize = models.CharField(max_length=256, verbose_name=u'Нормализованный терм', db_index=True)
    not_normalize = models.CharField(max_length=256, verbose_name=u'Ненормализованный терм', db_index=True)
    datetime = models.DateTimeField(auto_now_add=True, auto_now=True, db_index=True)


DEFAULT_LANG_CHICES = (
    ('rus', u'Русский'),
    ('eng', u'English'),
    ('tat', u'Татарский'),
)


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
         search_searchrequestlog.use as attribute
    FROM
        search_searchrequestlog
    GROUP BY
        search_searchrequestlog.use
    """
    results = execute(select, [])
    choices = []

    for row in results:
        choices.append(
            (
                row['attribute'],
                titles.get_attr_title(row['attribute'])
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
            count(search_searchrequestlog.use) as count, search_searchrequestlog.datetime as datetime
        FROM
            search_searchrequestlog
    """
    params = []
    where = ['WHERE date(datetime) BETWEEN %s  AND  %s ']
    params.append(start_date)
    params.append(end_date)

    if catalogs:
        # if len(catalogs) == 1:
        # where.append('AND ' + 'search_searchrequestlog.catalog = "%s" ' % catalogs[0]  )
        #        else:
        catalogs_where = []
        for catalog in catalogs:
            catalogs_where.append(' search_searchrequestlog.catalog = "%s" ' % catalog)
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
            count(search_searchrequestlog.use) as count, search_searchrequestlog.use as attribute
        FROM
            search_searchrequestlog
    """
    params = []

    where = ['WHERE date(datetime) BETWEEN %s  AND  %s ']
    params.append(start_date)
    params.append(end_date)

    if catalogs:
        # if len(catalogs) == 1:
        # where.append('AND ' + 'search_searchrequestlog.catalog = "%s" ' % catalogs[0]  )
        #        else:
        catalogs_where = []
        for catalog in catalogs:
            catalogs_where.append(' search_searchrequestlog.catalog = "%s" ' % catalog)
        where.append('AND (' + u'OR'.join(catalogs_where) + ')')

    if attributes:
        attributes_args = []
        for attribute in attributes:
            attributes_args.append(u'%s')
            params.append(attribute)

        attributes_args = u', '.join(attributes_args)
        where.append(' AND search_searchrequestlog.use in (%s) ' % attributes_args)

    where = u' '.join(where)

    results = execute(
        select + ' ' + where +
        u"""
        GROUP BY
            search_searchrequestlog.use
        ORDER BY
            count desc;
        """,
        params
    )

    rows = []

    for row in results:
        rows.append((titles.get_attr_title(row['attribute']), row['count']))
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
            count(search_searchrequestlog.not_normalize) as count, search_searchrequestlog.not_normalize as normalize
        FROM
            search_searchrequestlog
    """
    params = []

    where = [u' WHERE date(datetime) BETWEEN %s  AND  %s ']
    params.append(start_date)
    params.append(end_date)

    if catalogs:
        # if len(catalogs) == 1:
        # where.append('AND ' + 'search_searchrequestlog.catalog = "%s" ' % catalogs[0]  )
        #        else:
        catalogs_where = []
        for catalog in catalogs:
            catalogs_where.append(' search_searchrequestlog.catalog = "%s" ' % catalog)
        where.append('AND (' + u'OR'.join(catalogs_where) + ')')

    if attributes:
        attributes_args = []
        for attribute in attributes:
            attributes_args.append(u'%s')
            params.append(attribute)

        attributes_args = u', '.join(attributes_args)
        where.append(u' AND search_searchrequestlog.use in (%s) ' % attributes_args)

    where = u' '.join(where)

    results = execute(
        'select normalize, count from (' + select + ' ' + where +
        u"""
        GROUP BY
            search_searchrequestlog.not_normalize
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


def log_search_request(last_search_value):
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

    for part in last_search_value:
        term = part.get('value', None)
        if term:
            forms = clean_term(term)
            term_groups.append({
                'nn': forms[0],
                'n': forms[1],
                'use': u'_'.join(part.get('attr', u'not defined').split('_')[:-1])
            })

    models = []
    for group in term_groups:
        srl = SearchRequestLog(
            catalog=u'*',
            search_id=search_request_id,
            use=group['use'],
            normalize=group['n'],
            not_normalize=group['nn'],
        )
        models.append(srl)
    SearchRequestLog.objects.bulk_create(models)
