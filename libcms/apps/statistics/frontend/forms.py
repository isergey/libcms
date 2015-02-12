# coding=utf-8
from django import forms


PERIOD_CHOICES = (
    ('d', u'День'),
    ('m', u'Месяц'),
    ('y', u'Год'),
)

class PeriodForm(forms.Form):
    from_date = forms.DateField(label=u'Дата начала')
    to_date = forms.DateField(label=u'Дата окончания')
    period = forms.ChoiceField(choices=PERIOD_CHOICES, initial=PERIOD_CHOICES[0], label=u'Период', required=False)

VISIT_TYPES = (
    ('view', u'Просмотр'),
    ('visit', u'Посетители'),
)
class ParamForm(forms.Form):
    visit_type = forms.ChoiceField(label=u'Тип визита', choices=VISIT_TYPES)
    url_filter = forms.CharField(label=u'Фильтр URL (без учета префикса локали)', required=False)
