import uuid
import json
import hashlib
import datetime
from urlparse import urlparse
import requests
from localeurl import utils
from django.views.decorators.cache import never_cache
from django.shortcuts import render, HttpResponse
from .. import models
from . import forms
from participants.models import Library
from ssearch.models import request_group_by_date

URL_TIMEOUT = 1 # mins

def index(request):
    period_form = forms.PeriodForm(request.GET, prefix='pe')
    param_form = forms.ParamForm(request.GET, prefix='pa')
    results = []
    if period_form.is_valid() and param_form.is_valid():
        results = models.get_view_count_stats(
            from_date=period_form.cleaned_data['from_date'],
            to_date=period_form.cleaned_data['to_date'],
            period=period_form.cleaned_data['period'],
            url_filter=param_form.cleaned_data['url_filter'],
            visit_type=param_form.cleaned_data['visit_type'],
            #url_filter='/site/[0-9]+/?$'
        )
    return render(request, 'statistics/frontend/index.html', {
        'period_form': period_form,
        'param_form': param_form,
        'results': results
    })

def org_stats(request):
    org_code = request.GET.get('org_code', None)
    org_name = ''
    libs = Library.objects.filter(code=org_code)[:1]
    if libs:
        org_name = libs[0].name
    if not Library.objects.filter(code=org_code).exists():
        return HttpResponse(u'Org with code %s not exist' % org_code, status=400)

    responce_dict = {
        'org_code': org_code,
        'org_name': org_name
    }
    period_form = forms.PeriodForm(request.GET, prefix='pe')
    if period_form.is_valid():
        from_date=period_form.cleaned_data['from_date']
        to_date=period_form.cleaned_data['to_date']
        period=period_form.cleaned_data['period']
        url_filter=u'/site/%s/' % org_code

        results = models.get_view_count_stats(
            from_date=from_date,
            to_date=to_date,
            period=period,
            url_filter=url_filter
        )
        responce_dict['views'] = results
        results = models.get_view_count_stats(
            from_date=from_date,
            to_date=to_date,
            period=period,
            url_filter=url_filter,
            visit_type='visit'
        )
        responce_dict['visits'] = results

        results = request_group_by_date(
            from_date=from_date,
            to_date=to_date,
            period=period,
            library_code=org_code
        )

        responce_dict['search_requests'] = results

        print 'search results', results

    else:
        return HttpResponse(u'Wrong pe params %s' % period_form.errors, status=400)

    return HttpResponse(json.dumps(responce_dict, ensure_ascii=False), content_type='application/json')


def search_stats(request):
    period_form = forms.PeriodForm(request.GET, prefix='pe')
    responce_dict= {
        'not_specified': [],
        'catalogs': {}
    }
    if period_form.is_valid():
        from_date=period_form.cleaned_data['from_date']
        to_date=period_form.cleaned_data['to_date']
        period=period_form.cleaned_data['period']

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
    if models.PageView.objects.filter(datetime__gt=before, session=session, url_hash=url_hash).exists():
        ignore = True

    if session and not ignore:
        models.log_page_view(path=path, query=query, url_hash=url_hash, session=session)

    return response




# METRIKA_URL = 'http://api-metrika.yandex.ru'
# # 444c680b612b47178114c8eef3811e5a
# def index(request):
#     response = requests.get(METRIKA_URL + '/counters', headers={
#         'Accept': 'application/x-yametrika+json',
#         'Content-type': 'application/x-yametrika+json',
#         'Authorization': 'OAuth 444c680b612b47178114c8eef3811e5a'
#     })
#
#     response = requests.get(METRIKA_URL + '/stat/content/popular', headers={
#         'Accept': 'application/x-yametrika+json',
#         'Content-type': 'application/x-yametrika+json',
#         'Authorization': 'OAuth 444c680b612b47178114c8eef3811e5a'
#     }, params={
#         'id': '3927343',
#         'table_mode': 'tree'
#     })
#
#     print response.text
#
#
#     return render(request, 'statistics/frontend/index.html')