# coding=utf-8
from django.conf import settings
from django.core.cache import caches
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect, resolve_url

import requests
from participants.decorators import must_be_org_user
from . import forms

cache = caches['default']

TOKEN = '123'

TATAR_STATISTICS = getattr(settings, 'TATAR_STATISTICS', {})
REPORT_SERVER = TATAR_STATISTICS.get('report_server', 'http://10.14.0.52/reports/')

# template = etree.XSLT(etree.parse(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modern.xsl')))


def _make_request(method, **kwargs):
    request_method = getattr(requests, method)
    error = None
    response = None
    try:
        response = request_method(**kwargs)
        response.raise_for_status()
    except requests.Timeout:
        error = u'Таймаут соединения с сервером статистки'
    except requests.HTTPError:
        error = u'Ошибка связи с сервером статистики'

    return (response, error)


def _check_for_error(response_dict):
    error = None
    if not response_dict.get('ok', False):
        error = response_dict.get('errorMessage', u'Описание ошибки отсутвует')
    return error


def _get_security(managed_libraries, user):
    security = u'Организация=Total,00000000'
    if user.has_perm('statistics.view_all_statistic'):
        return security

    if managed_libraries:
        if managed_libraries[0].is_root_node():
            root_code = managed_libraries[0].code
        else:
            root_code = managed_libraries[0].get_root().code
        security = u'Организация=' + root_code

    return security

@login_required
@must_be_org_user
def index(request, managed_libraries=[]):
    if not request.user.has_perm('statistics.view_org_statistic') and \
            not request.user.has_perm('statistics.view_all_statistic') and not managed_libraries:
        return HttpResponse(u'Доступ запрещен', status=403)
    category_param = request.GET.get('category', '')

    security = _get_security(managed_libraries, request.user)

    response, error = _make_request('get', url=REPORT_SERVER + 'reports', params={
        'token': TOKEN,
        'format': 'json',
        'category': category_param,
        'security': security,
    })
    response_dict = {}
    if not error:
        # response_dict = response.text
        try:
            response_dict = response.json()
            error = _check_for_error(response_dict)
        except ValueError:
            error = u'Неожиданный ответ от сервера статистики'

    categories = response_dict.get('categories', [])
    category_codes = set()
    if categories:
        for category in categories:
            code = category.get('code')
            if code:
                category_codes.add(code)

        if category_param not in category_codes:
            return redirect(resolve_url('statistics:frontend:index') + '?category=' + categories[0].get('code'))

    if categories and not category:
        for category in categories:
            if category.get('isSelected'):
                return redirect(resolve_url('statistics:frontend:index') + '?category=' + category.get('code'))
        return redirect(resolve_url('statistics:frontend:index') + '?category=' + categories[0].get('code'))

    return render(request, 'statistics/frontend/index.html', {
        'response_dict': response_dict,
        'error': error,
        'managed_libraries': managed_libraries,
        'category': category_param,
    })


@login_required
@must_be_org_user
def report(request, managed_libraries=[]):
    view = request.GET.get('view', 'modern2')
    category = request.GET.get('category', '')
    security = u'Организация=Total,00000000'
    access = False

    if request.user.has_perm('statistics.view_all_statistic'):
        access = True
    else:
        if managed_libraries:
            access = True
            security = _get_security(managed_libraries, request.user)

    if not access:
        return HttpResponse(u'Доступ запрещен', status=403)

    report_form = forms.ReportForm(request.GET)
    parameters = request.GET.get('parameters', '')
    error = None
    report_body = u''
    if report_form.is_valid():
        params = {
            'token': TOKEN,
            'view': view,
            'code': report_form.cleaned_data['code'],
            'security': security,
            'parameters': parameters,
            'category': category
        }

        response, error = _make_request('get', url=REPORT_SERVER + 'report', params=params)
        if not error:
            print response.headers
            content_type = response.headers.get('content-type', 'text/html')
            if content_type != 'text/html':
                dj_response = HttpResponse(response.content, content_type=content_type)
                content_disposition = response.headers.get('content-disposition')
                if content_disposition:
                    dj_response['content-disposition'] = content_disposition
                return dj_response
            report_body = response.content  # unicode(template(etree.fromstring(response.content)))
    else:
        error = unicode(report_form.errors)
    return render(request, 'statistics/frontend/reports.html', {
        'report_body': report_body,
        'error': error
    })
