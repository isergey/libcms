import datetime
from collections import OrderedDict, Counter
from django.db import models, connection
from django.contrib.auth.models import User
from sso_ruslan.models import RuslanUser

class Statistics(models.Model):
    class Meta:
        permissions = [
            ['view_org_statistic', u'Can view self org statistic reports'],
            ['view_all_statistic', u'Can view all statistic reports']
        ]


class PageView(models.Model):
    user = models.ForeignKey(User, null=True)
    path = models.CharField(max_length=1024, blank=True)
    query = models.CharField(max_length=1024, blank=True)
    url_hash = models.CharField(max_length=32, db_index=True)
    session = models.CharField(max_length=32, db_index=True)
    datetime = models.DateTimeField(auto_now_add=True, db_index=True)


def log_page_view(path, query, url_hash, session, user=None):
    PageView.objects.bulk_create([
        PageView(path=path[:1024], query=query[:1024], url_hash=url_hash[:32], session=session[:32], user=user)
    ])


def get_view_count_stats(from_date, to_date, period, visit_type='view', url_filter=''):
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
    distinct = ''
    if visit_type == 'visit':
        distinct = 'distinct'
    select = """count(%s session) as count, %s as date""" % (distinct, date_format)
    frm = 'statistics_pageview'
    where = 'datetime >= %s AND datetime < %s'
    args += [from_date, to_date + datetime.timedelta(days=1)]

    if url_filter:
        where += " AND path ~* %s"
        args += [url_filter]
    query = u' '.join(['SELECT', select, 'FROM', frm, 'WHERE', where, 'GROUP BY', group_by])

    cursor.execute(query, args)
    row_hash = OrderedDict()

    for row in _dictfetchall(cursor):
        row_hash[row['date']] = row['count']

    results = []
    for date in date_range:
        results.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': row_hash.get(date, 0)
        })

    return results


"""
date_groups = {
  '20161206': {
    'user_id': {
      'org_id': 1
    }
  }
}
"""
def get_users_at_mini_sites(from_date, to_date):
    ruslan_users = list(RuslanUser.objects.values('user_id', 'username').all())
    ruslan_users_index = {}
    for ruslan_user in ruslan_users:
        print 'ruslan_user', ruslan_user
        ruslan_users_index[ruslan_user['user_id']] = ruslan_user

    date_range = _generate_dates(from_date, to_date, 'd')
    cursor = connection.cursor()
    args = []

    select = '*'
    frm = 'statistics_pageview'
    where = 'datetime >= %s AND datetime < %s'
    args += [from_date, to_date + datetime.timedelta(days=1)]

    query = u' '.join(['SELECT', select, 'FROM', frm, 'WHERE', where])
    cursor.execute(query, args)
    row_hash = OrderedDict()

    date_groups = OrderedDict()
    for row in _dictfetchall(cursor):
        org_id = ''
        path = row['path']
        if path.startswith('/site'):
            path_parts = path.split('/')
            if len(path_parts) > 2:
                org_id = path_parts[2]
        if not org_id:
            continue

        dt = row['datetime']
        str_date = datetime.date(year=dt.year, month=dt.month, day=dt.day)
        user_groups = date_groups.get(str_date, None)
        if user_groups is None:
            user_groups = {}
            date_groups[str_date] = user_groups
        org_groups = user_groups.get(row['user_id'], None)
        if org_groups is None:
            org_groups = Counter()
            user_groups[row['user_id']] = org_groups
        org_groups[org_id] += 1

    # flatting
    lines = []
    for date, user_groups in date_groups.items():
        for user_id, org_groups in user_groups.items():
            for org_id, count in org_groups.items():
                lines.append({
                    'date': date.strftime('%Y%m%d'),
                    'reader_id': ruslan_users_index.get(user_id, {}).get('username') or '000000000',
                    'user_id': user_id or 0,
                    'org_id': org_id,
                    'count': count,
                    'target': '4',
                    'user_data': '4'
                })

    # results = []
    # for date in date_range:
    #     results.append({
    #         'date': date,
    #         'data': date_groups.get(date, {})
    #     })
    return lines


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
            date_range.append(datetime.date(year=year, month=1, day=1))
    elif period == 'm':
        for date in _monthrange(from_date, to_date):
            date_range.append(datetime.date(year=date.year, month=date.month, day=1))
    else:
        for date in _daysrange(from_date, to_date):
            date_range.append(datetime.date(year=date.year, month=date.month, day=date.day))

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
