# coding: utf-8
import datetime
from django import forms
from ssearch.models import Upload
from ..models import get_search_attributes_in_log
from django.contrib.admin import widgets


class UploadForm(forms.models.ModelForm):
    class Meta:
        model = Upload
        exclude = ('timestamp', 'processed', 'success')


GROUP_CHOICES = (
    (u'2', u'По дням'),
    (u'1', u'По месяцам'),
    (u'0', u'По годам'),
)


class PeriodForm(forms.Form):
    start_date = forms.DateTimeField(
        label=u'Дата начала периода', widget=widgets.AdminDateWidget,
        initial=datetime.datetime.now()
    )

    end_date = forms.DateTimeField(
        label=u'Дата конца периода', widget=widgets.AdminDateWidget,
        initial=datetime.datetime.now()
    )


class GroupForm(forms.Form):
    group = forms.ChoiceField(label=u'Группировка', choices=GROUP_CHOICES, initial=2)


class AttributesForm(forms.Form):
    attributes = forms.MultipleChoiceField(
        label=u'Отображаемые атрибуты',
        choices=get_search_attributes_in_log(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )


catalogs = (
    ('sc2', u'Сводный каталог'),
    ('ebooks', u'"Электронная коллекция')
)


class CatalogForm(forms.Form):
    catalogs = forms.MultipleChoiceField(
        choices=catalogs,
        label=u'Каталоги',
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )