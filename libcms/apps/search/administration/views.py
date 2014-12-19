# coding: utf-8
import json as simplejson
import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse

from guardian.decorators import permission_required_or_403
from forms import AttributesForm, GroupForm, PeriodForm, CatalogForm
from ..models import requests_count, requests_by_attributes, requests_by_term


@login_required
@permission_required_or_403('search.view_statistics')
def index(request):
    return render(request, 'search/administration/index.html')

#def statistics(request, catalog=None):
#    return HttpResponse(u'Статистика')

@login_required
@permission_required_or_403('search.view_statistics')
def statistics(request, catalog=None):
    """
    тип графика
    название графика
    массив название
    массив данных
    подпись по x
    подпись по y
    """
    chart_type = 'column'
    chart_title = u'Название графика'
    row_title = u'Параметр'
    y_title = u'Ось Y'


    statistics = request.GET.get('statistics', 'requests')
    catalogs = []
    if not catalog:
        catalogs += ['records']
    else:
        catalogs.append(catalog)
#    catalogs = ZCatalog.objects.all()
    start_date = datetime.datetime.now()
    end_date = datetime.datetime.now()
    date_group = u'2' # группировка по дням
    attributes = []


    if request.method == 'POST':
        period_form = PeriodForm(request.POST)
        group_form = GroupForm(request.POST)
        attributes_form = AttributesForm(request.POST)
        catalog_form = CatalogForm(request.POST)

        if period_form.is_valid():
            start_date = period_form.cleaned_data['start_date']
            end_date = period_form.cleaned_data['end_date']
        if group_form.is_valid():
            date_group = group_form.cleaned_data['group']

        if attributes_form.is_valid():
            attributes = attributes_form.cleaned_data['attributes']

        if catalog_form.is_valid():
            catalogs = catalog_form.cleaned_data['catalogs']
    else:
        period_form = PeriodForm()
        group_form = GroupForm()
        attributes_form = AttributesForm()
        catalog_form = CatalogForm()

    if statistics == 'requests':
        attributes_form = None
        rows = requests_count(
            start_date = start_date,
            end_date = end_date,
            group = date_group,
            catalogs = catalogs
        )
        chart_title = u'Число поисковых запросов по дате'
        row_title = u'Число поисковых запросов'
        y_title = u'Число поисковых запросов'

    elif statistics == 'attributes':
        group_form = None
        rows = requests_by_attributes(
            start_date = start_date,
            end_date = end_date,
            attributes = attributes,
            catalogs = catalogs
        )

        chart_title = u'Число поисковых запросов по поисковым атрибутам'
        row_title = u'Число поисковых запросов'
        y_title = u'Число поисковых запросов'
        chart_type = 'bar'

    elif statistics == 'terms':
        group_form = None
        rows = requests_by_term(
            start_date = start_date,
            end_date = end_date,
            attributes = attributes,
            catalogs = catalogs
        )

        chart_title = u'Число поисковых запросов по фразам'
        row_title = u'Число поисковых запросов'
        y_title = u'Число поисковых запросов'
        chart_type = 'bar'
    else:
        return HttpResponse(u'Неправильный тип статистики')


    data_rows =  simplejson.dumps(rows, ensure_ascii=False)


    return render(request, 'search/administration/statistics.html', {
        'data_rows':data_rows,
        'catalog_form': catalog_form,
        'period_form': period_form,
        'group_form': group_form,
        'attributes_form': attributes_form,
        'chart_type': chart_type,
        'chart_title': chart_title,
        'y_title': y_title,
        'row_title': row_title,
    })





