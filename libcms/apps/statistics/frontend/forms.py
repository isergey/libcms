# coding=utf-8
from django import forms


PERIOD_CHOICES = (
    ('d', u'День'),
    ('m', u'Месяц'),
    ('y', u'Год'),
)

class PeriodForm(forms.Form):
    from_date = forms.DateField(required=True)
    to_date = forms.DateField(required=True)
    period = forms.ChoiceField(choices=PERIOD_CHOICES, required=True, initial=PERIOD_CHOICES[0])