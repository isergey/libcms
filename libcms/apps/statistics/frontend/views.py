import uuid
import hashlib
import datetime
from urlparse import urlparse
import requests
from localeurl import utils
from django.views.decorators.cache import never_cache
from django.shortcuts import render, HttpResponse
from .. import models
from . import forms

URL_TIMEOUT = 10 # mins

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