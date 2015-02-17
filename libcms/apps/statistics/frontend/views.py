# coding=utf-8
import os
import requests
from lxml import etree
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, urlresolvers
from . import forms

TOKEN = '123'
REPORT_SERVER = 'http://statat.ipq.co/reports/'

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


@login_required
def index(request):
    response, error = _make_request('get', url=REPORT_SERVER + 'reports', params={
        'token': TOKEN,
        'format': 'json'
    })
    response_dict = {}
    if not error:
        print response.text
        #response_dict = response.text
        try:
            response_dict = response.json()
            error = _check_for_error(response_dict)
        except ValueError:
            error = u'Неожиданный ответ от сервера статистики'


    return render(request, 'statistics/frontend/index.html', {
        'response_dict': response_dict,
        'error': error
    })

@login_required
def report(request):
    report_form = forms.ReportForm(request.GET)
    parameters = request.GET.get('parameters', '')
    error = None
    report_body = u''
    if report_form.is_valid():
        response, error = _make_request('get', url=REPORT_SERVER + 'report', params={
            'token': TOKEN,
            'view': 'source',
            'code': report_form.cleaned_data['code'],
            'security': 'Организация=Total,00000000',
            'parameters': parameters
        })
        if not error:
            template = etree.XSLT(etree.parse(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modern.xsl')))
            report_body = unicode(template(etree.fromstring(response.content)))
            # report_body = response.text
            #
            # root = html.fromstring(report_body)
            # print root.xpath('//div[class=')
            # print report_body.decode('cp1251')
    else:
        error = unicode(report_form.errors)
    return render(request, 'statistics/frontend/reports.html', {
        'report_body': report_body,
        'error': error
    })