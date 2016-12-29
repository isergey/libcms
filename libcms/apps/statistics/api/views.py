import uuid
import json
import hashlib
import datetime
import dicttoxml
import collections
from urlparse import urlparse
from localeurl import utils
from django.views.decorators.cache import never_cache
from django.shortcuts import render, HttpResponse, get_object_or_404
from .. import models
from . import forms
from participants.models import Library
from ssearch.models import request_group_by_date
from participants import models as pmodels
from participant_pages import models as ppmodels
from participant_news import models as pnmodels
from participant_events import models as pemodels
from sso_ruslan import models as sso_ruslan_models
from news import models as news_models

URL_TIMEOUT = 1  # mins


def index(request):
    period_form = forms.PeriodForm(request.GET, prefix='pe')
    param_form = forms.ParamForm(request.GET, prefix='pa')
    results = []
    if period_form.is_valid() and param_form.is_valid():
        from_date, to_date = period_form.get_period_dates()
        period = period_form.cleaned_data['period']
        results = models.get_view_count_stats(
            from_date=from_date,
            to_date=to_date,
            period=period,
            url_filter=param_form.cleaned_data['url_filter'],
            visit_type=param_form.cleaned_data['visit_type'],
            # url_filter='/site/[0-9]+/?$'
        )
    return render(request, 'statistics/api/index.html', {
        'period_form': period_form,
        'param_form': param_form,
        'results': results
    })


def org_stats(request):
    params = request.GET.get('params', '')
    params_parts = []
    for param in params.strip().split(','):
        if param:
            params_parts.append(param)

    scheme = request.GET.get('scheme', 'xml')
    schemes = ['xml', 'json']
    if scheme not in schemes:
        scheme = 'xml'

    org_code = request.GET.get('code', None)

    org=None
    org_name = ''
    if org_code:
        try:
            org = Library.objects.get(code=org_code)
            org_name = org.name
        except Library.DoesNotExist:
            return HttpResponse(u'Org with code %s not exist' % org_code, status=400)

    # if org_code and not Library.objects.filter(code=org_code).exists():
    #     return HttpResponse(u'Org with code %s not exist' % org_code, status=400)

    responce_dict = {
        'org_code': org_code,
        'org_name': org_name,
    }
    period_form = forms.PeriodForm(request.GET, prefix='pe')

    url_filter = '/'
    if org_code:
        url_filter = u'/site/%s/' % org_code

    if period_form.is_valid():
        from_date, to_date = period_form.get_period_dates()
        period = period_form.cleaned_data['period']
        url_filter = url_filter
        if not params_parts or 'views' in params_parts:
            results = models.get_view_count_stats(
                from_date=from_date,
                to_date=to_date,
                period=period,
                url_filter=url_filter
            )
            responce_dict['views'] = results

        if not params_parts or 'visits' in params_parts:
            results = models.get_view_count_stats(
                from_date=from_date,
                to_date=to_date,
                period=period,
                url_filter=url_filter,
                visit_type='visit'
            )
            responce_dict['visits'] = results

        if not params_parts or 'search_requests' in params_parts:
            results = request_group_by_date(
                from_date=from_date,
                to_date=to_date,
                period=period,
                library_code=org_code
            )

            responce_dict['search_requests'] = results

    else:
        return HttpResponse(u'Wrong pe params %s' % period_form.errors, status=400)

    if scheme == 'xml':
        return HttpResponse(dicttoxml.dicttoxml(
            responce_dict, custom_root='fields', attr_type=False),
            content_type='application/xml'
        )

    return HttpResponse(json.dumps(responce_dict, ensure_ascii=False), content_type='application/json')


def search_stats(request):
    period_form = forms.PeriodForm(request.GET, prefix='pe')
    responce_dict = {
        'not_specified': [],
        'catalogs': {}
    }
    if period_form.is_valid():
        from_date, to_date = period_form.get_period_dates()
        period = period_form.cleaned_data['period']

        results = request_group_by_date(
            from_date=from_date,
            to_date=to_date,
            period=period,
        )

        responce_dict['not_specified'] = results

        catalogs = ['sc2', 'ebooks']
        for catalog in catalogs:
            results = request_group_by_date(
                from_date=from_date,
                to_date=to_date,
                period=period,
                catalog=catalog
            )
            responce_dict['catalogs'][catalog] = results

    return HttpResponse(json.dumps(responce_dict, ensure_ascii=False), content_type='application/json')


@never_cache
def watch(request):
    response = HttpResponse(status=200)
    session = request.COOKIES.get('_sc', None)

    if not session:
        session = uuid.uuid4().hex
        response.set_cookie('_sc', session, max_age=60 * 60 * 24 * 365)

    http_referer = request.META.get('HTTP_REFERER', None)
    if not http_referer:
        return response

    url_parts = urlparse(http_referer)
    path_parts = utils.strip_path(url_parts.path)
    if len(path_parts) > 1:
        path = path_parts[1]
    else:
        path = path_parts[0]
    ignore = False

    query = url_parts.query

    url_hash = hashlib.md5((path + query).encode('utf-8')).hexdigest()

    before = (datetime.datetime.now() - datetime.timedelta(minutes=URL_TIMEOUT))
    # if models.PageView.objects.filter(datetime__gt=before, session=session, url_hash=url_hash).exists():
    #     ignore = True

    user = None
    if request.user.is_authenticated():
        user = request.user
    if session and not ignore:
        models.log_page_view(path=path, query=query, url_hash=url_hash, session=session, user=user)

    return response


@never_cache
def users_at_mini_sites(request):
    formats = ['txt', 'json']
    format = request.GET.get('format', formats[0])
    if format not in formats:
        format = 'txt'
    period_form = forms.PeriodForm(request.GET, prefix='pe')
    if period_form.is_valid():
        from_date, to_date = period_form.get_period_dates()
        period = period_form.cleaned_data['period']
        results = models.get_users_at_mini_sites(from_date, to_date)
        if format == 'json':
            return HttpResponse(json.dumps(results, ensure_ascii=False), content_type='application/json')
        else:
            lines = []
            for result in results:
                lines.append(
                    u'\t'.join([
                        result['date'],
                        unicode(result['reader_id']),
                        result['target'],
                        result['user_data'],
                        result['org_id'],
                        unicode(result['count']),
                    ])
                )
            lines = u'\n'.join(lines)
            return HttpResponse(lines, content_type='text/plain; charset=utf-8')
    else:
        return HttpResponse(json.dumps(period_form.errors, ensure_ascii=False))


def orgs_statistic(request):
    now = datetime.datetime.now()
    scheme = request.GET.get('scheme', 'xml')
    schemes = ['xml', 'json']

    if scheme not in schemes:
        scheme = 'xml'

    total_orgs = pmodels.Library.objects.all().count()
    page_libs = set()
    for page in ppmodels.Page.objects.values('library_id').filter(parent=None).iterator():
        page_libs.add(page['library_id'])

    news_count = pnmodels.News.objects.all().count()
    ruslan_users = sso_ruslan_models.RuslanUser.objects.all().count()
    events_count = pemodels.Event.objects.all().count()
    evet_subscibe_users = set()
    for subscribe in pemodels.EventSubscribe.objects.values('user_id').all().iterator():
        evet_subscibe_users.add(subscribe['user_id'])
    site_views_count = models.PageView.objects.filter(path__startswith='/site/').count()
    result = {
        'orgs_count': total_orgs,
        'sites_count': len(page_libs),
        'ruslan_users': ruslan_users,
        'news_count': news_count,
        'events_count': events_count,
        'event_subscribe_users_count': len(evet_subscibe_users),
        'site_views_count': site_views_count,
        'date_time': now.strftime('%Y-%m-%dT%H:%M:%S')
    }

    response = ''
    if scheme == 'json':
        response = json.dumps(result, ensure_ascii=False)
    else:
        response = dicttoxml.dicttoxml(result, custom_root='fields', attr_type=False)
    return HttpResponse(response, content_type='application/' + scheme)


def org_statistic(request):
    now = datetime.datetime.now()
    scheme = request.GET.get('scheme', 'xml')
    schemes = ['xml', 'json']

    if scheme not in schemes:
        scheme = 'xml'

    code = request.GET.get('code', '')
    library = get_object_or_404(Library, code=code)

    period_form = forms.PeriodForm(request.GET, prefix='pe')

    if not period_form.is_valid():
        return HttpResponse(json.dumps(period_form.errors, ensure_ascii=False))

    has_mini_site = False
    if library:
        if ppmodels.Page.objects.filter(library=library).exists():
            has_mini_site = True
        elif pnmodels.News.objects.filter(library=library).exists():
            has_mini_site = True
        elif pemodels.Event.objects.filter(library=library).exists():
            has_mini_site = True

    from_date, to_date = period_form.get_period_dates()
    period = period_form.cleaned_data['period']

    dates = models._generate_dates(from_date=from_date, to_date=to_date, period=period)

    date_groups = collections.OrderedDict()
    for date in dates:
        date_groups[_get_date_str(date, period)] = collections.Counter({
            'news_count': 0,
            'events_count': 0,
            'event_subscribes_count': 0,
            'has_mini_site': has_mini_site,
        })

    news_iterator = pnmodels.News.objects.values('create_date').filter(
        library=library,
        create_date__gte=from_date,
        create_date__lt=to_date + datetime.timedelta(days=1)
    ).iterator()

    for news in news_iterator:
        create_date = news['create_date']
        date_groups[_get_date_str(create_date, period)]['news_count'] += 1

    events_iterator = pemodels.Event.objects.values('create_date').filter(
        library=library,
        create_date__gte=from_date,
        create_date__lt=to_date + datetime.timedelta(days=1)
    ).iterator()

    for event in events_iterator:
        create_date = event['create_date']
        date_groups[_get_date_str(create_date, period)]['events_count'] += 1

    event_subscribes_iterator = pemodels.EventNotification.objects.values('create_date').filter(
        event__library=library,
        create_date__gte=from_date,
        create_date__lt=to_date + datetime.timedelta(days=1)
    ).iterator()
    for event_subscribe in event_subscribes_iterator:
        create_date = event_subscribe['create_date']
        date_groups[_get_date_str(create_date, period)]['event_subscribes_count'] += 1

    response = ''
    if scheme == 'json':
        response = json.dumps(date_groups, ensure_ascii=False)
    else:
        response = dicttoxml.dicttoxml(date_groups, custom_root='fields', attr_type=False)
    return HttpResponse(response, content_type='application/' + scheme)


def portal_statistic(request):
    scheme = request.GET.get('scheme', 'xml')
    schemes = ['xml', 'json']

    if scheme not in schemes:
        scheme = 'xml'

    code = request.GET.get('code', '')

    period_form = forms.PeriodForm(request.GET, prefix='pe')

    if not period_form.is_valid():
        return HttpResponse(json.dumps(period_form.errors, ensure_ascii=False))

    from_date, to_date = period_form.get_period_dates()
    period = period_form.cleaned_data['period']

    dates = models._generate_dates(from_date=from_date, to_date=to_date, period=period)

    date_groups = collections.OrderedDict()
    for date in dates:
        date_groups[_get_date_str(date, period)] = collections.Counter({
            'news_count': 0,
        })

    news_iterator = news_models.News.objects.values('create_date').filter(
        create_date__gte=from_date,
        create_date__lt=to_date + datetime.timedelta(days=1)
    ).iterator()

    for news in news_iterator:
        create_date = news['create_date']
        date_groups[_get_date_str(create_date, period)]['news_count'] += 1

    response = ''
    if scheme == 'json':
        response = json.dumps(date_groups, ensure_ascii=False)
    else:
        response = dicttoxml.dicttoxml(date_groups, custom_root='fields', attr_type=False)
    return HttpResponse(response, content_type='application/' + scheme)


def _get_date_str(date, period):
    if period == 'y':
        res_date = datetime.date(year=date.year, month=1, day=1)
    elif period == 'm':
        res_date = datetime.date(year=date.year, month=date.month, day=1)
    else:
        res_date = datetime.date(year=date.year, month=date.month, day=date.day)
    return res_date.strftime('%Y-%m-%d')
