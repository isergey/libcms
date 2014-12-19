# coding: utf-8
import datetime
from django import forms
from ..models import get_search_attributes_in_log
from django.contrib.admin import widgets


GROUP_CHOICES = (
    (u'2', u'По дням'),
    (u'1', u'По месяцам'),
    (u'0', u'По годам'),
    )


class PeriodForm(forms.Form):
    start_date = forms.DateField(
        label=u'Дата начала периода',
        initial=datetime.datetime.now(),
    )

    end_date = forms.DateField(
        label=u'Дата конца периода',
        initial=datetime.datetime.now()
    )



class GroupForm(forms.Form):
    group = forms.ChoiceField(label=u'Группировка', choices=GROUP_CHOICES, initial=2)

get_search_attributes_in_log1 = get_search_attributes_in_log()

class AttributesForm(forms.Form):
    attributes = forms.MultipleChoiceField(
        label=u'Отображаемые атрибуты',
        choices=get_search_attributes_in_log1,
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

catalogs = (
    ('sc2', u'Сводный каталог'),
    ('ebooks', u'"Электронная коллекция')
)

from django.conf import settings
def get_catalogs():
    catalogs = []
    solr_catalogs = settings.SEARCH.get('catalogs', {})
    for key in solr_catalogs.keys():
        catalogs.append((
            key, key
        ))
    return catalogs

class CatalogForm(forms.Form):
    catalogs = forms.MultipleChoiceField(
        choices=get_catalogs(),
        label=u'Каталоги',
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )