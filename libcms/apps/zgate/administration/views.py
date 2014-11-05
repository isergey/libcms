# -*- coding: utf-8 -*-
import json
import datetime
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
#from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.urlresolvers import reverse
from guardian.decorators import permission_required_or_403
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from zgate.models import ZCatalog
from zgate.models import requests_count, requests_by_attributes, requests_by_term
from forms import ZCatalogForm, PeriodForm, GroupForm, AttributesForm, ZCatalogForm
from django.forms.models import model_to_dict

from common.access.shortcuts import assign_perm_for_groups_id, get_group_ids_for_object_perm, edit_group_perms_for_object

@permission_required_or_403('zgate.add_zcatalog')
def index(request):
    zcatalogs = ZCatalog.objects.all().order_by('-id')
    paginator = Paginator(zcatalogs, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        zcatalogs_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        zcatalogs_list = paginator.page(paginator.num_pages)

    return render(request, 'zgate/administration/zcatalogs_list.html', {
        'zcatalogs_list': zcatalogs_list,
        'active_module': 'zgate'
    })



@permission_required_or_403('zgate.add_zcatalog')
def create(request):
    if request.method == 'POST':
        form = ZCatalogForm(request.POST)
        if form.is_valid():
            catalog = form.save()
            view_catalog_groups_ids = form.cleaned_data['view_page_groups']
            assign_perm_for_groups_id('view_zcatalog', catalog, view_catalog_groups_ids)

            return HttpResponseRedirect(reverse('administration_zgate_index'))
    else:
        form = ZCatalogForm()

    return render(request, 'zgate/administration/zcatalog_create.html', {
        'form': form,
        'active_module': 'zgate'
    })



@permission_required_or_403('zgate.change_zcatalog')
def edit(request, id):
    zcatalog = get_object_or_404(ZCatalog, id=id)

    old_catalog_groups_ids = get_group_ids_for_object_perm(u'view_zcatalog', zcatalog)

    if request.method == 'POST':
        form = ZCatalogForm(request.POST, instance=zcatalog)
        if form.is_valid():
            catalog = form.save()
            new_catalog_groups_ids = form.cleaned_data['view_catalog_groups']
            edit_group_perms_for_object('view_zcatalog', catalog, old_catalog_groups_ids, new_catalog_groups_ids)
            return HttpResponseRedirect(reverse('administration_zgate_index'))
    else:
        init = model_to_dict(zcatalog)
        init['view_catalog_groups'] = old_catalog_groups_ids

        form = ZCatalogForm(init,instance=zcatalog)
    return render(request, 'zgate/administration/zcatalog_edit.html', {
        'form': form,
        'zcatalog':zcatalog,
        'active_module': 'zgate'
    })




@permission_required_or_403('zgate.delete_zcatalog')
def delete(request, id):
    zcatalog = get_object_or_404(ZCatalog, id=id)
    zcatalog.delete()
    return HttpResponseRedirect(reverse('administration_zgate_index'))


@permission_required_or_403('zgate.change_zcatalog')
def statistics(request):
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

    catalogs = ZCatalog.objects.all()
    start_date = datetime.datetime.now()
    end_date = datetime.datetime.now()
    date_group = u'2' # группировка по дням
    attributes = []

    period_form = PeriodForm()
    group_form = GroupForm()
    attributes_form = AttributesForm()
    catalog_form = ZCatalogForm()
    if request.method == 'POST':
        period_form = PeriodForm(request.POST)
        group_form = GroupForm(request.POST)
        attributes_form = AttributesForm(request.POST)
        catalog_form = ZCatalogForm(request.POST)

        if period_form.is_valid():
            start_date = period_form.cleaned_data['start_date']
            end_date = period_form.cleaned_data['end_date']

        if group_form.is_valid():
            date_group = group_form.cleaned_data['group']

        if attributes_form.is_valid():
            attributes = attributes_form.cleaned_data['attributes']

        if catalog_form.is_valid():
            catalogs = catalog_form.cleaned_data['catalogs']


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


    data_rows =  json.dumps(rows, ensure_ascii=False)


    return render(request, 'zgate/administration/zcatalog_statistics.html', {
        'data_rows':data_rows,
        'catalog_form': catalog_form,
        'period_form': period_form,
        'group_form': group_form,
        'attributes_form': attributes_form,
        'chart_type': chart_type,
        'chart_title': chart_title,
        'y_title': y_title,
        'row_title': row_title,
        'active_module': 'zgate'
    })

