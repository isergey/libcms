import datetime
from collections import OrderedDict
from django.db import models, connection


class Statistics(models.Model):
    class Meta:
        permissions = [
            ['view_org_statistic', u'Can view self org statistic reports'],
            ['view_all_statistic', u'Can view all statistic reports']
        ]


class PageView(models.Model):
    path = models.CharField(max_length=1024, blank=True)
    query = models.CharField(max_length=1024, blank=True)
    url_hash = models.CharField(max_length=32, db_index=True)
    session = models.CharField(max_length=32, db_index=True)
    datetime = models.DateTimeField(auto_now_add=True, db_index=True)


def log_page_view(path, query, url_hash, session):
    PageView.objects.bulk_create([
        PageView(path=path[:1024], query=query[:1024], url_hash=url_hash[:32], session=session[:32])
    ])


def get_view_count_stats(from_date, to_date, period, visit_type='view', url_filter=''):
    date_range = _generate_dates(from_date, to_date, period)

    group_by = 'year(datetime), month(datetime), day(datetime)'
    date_format = "date_format(datetime, '%%Y-%%m-%%d')"
    if period == 'y':
        group_by = 'year(datetime)'
        date_format = "date_format(datetime, '%%Y-01-01')"
    elif period == 'm':
        group_by = 'year(datetime), month(datetime)'
        date_format = "date_format(datetime, '%%Y-%%m-01')"
    else:
        pass

    cursor = connection.cursor()
    args = []
    distinct = ''
    if visit_type == 'visit':
        distinct = 'distinct'
    select = """count(%s session) as count, %s as date""" % (distinct, date_format)
    frm = 'statistics_pageview'
    where = 'datetime >= %s AND datetime < %s'
    args += [from_date, to_date + datetime.timedelta(days=1)]

    if url_filter:
        where += " AND path REGEXP %s"
        args += [url_filter]
    query = u' '.join(['SELECT', select, 'FROM', frm, 'WHERE', where, 'GROUP BY', group_by])

    cursor.execute(query, args)
    row_hash = OrderedDict()

    for row in _dictfetchall(cursor):
        row_hash[row['date']] = row['count']

    results = []
    for date in date_range:
        results.append({
            'date': date,
            'count': row_hash.get(date, 0)
        })

    return results


def _dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
        ]


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
