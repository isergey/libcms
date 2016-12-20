# coding=utf-8
import datetime
import calendar
from django import forms

PERIOD_CHOICES = (
    ('d', u'День'),
    ('m', u'Месяц'),
    ('y', u'Год'),
)


class PeriodForm(forms.Form):
    from_date = forms.DateField(label=u'Дата начала')
    to_date = forms.DateField(label=u'Дата окончания', required=False)
    complete_to_month = forms.BooleanField(label=u'Дополнить до конца месяца', required=False, initial=False)
    period = forms.ChoiceField(choices=PERIOD_CHOICES, initial=PERIOD_CHOICES[0], label=u'Период', required=False)

    def clean(self):
        to_date = self.cleaned_data['to_date']
        complete_to_month = self.cleaned_data['complete_to_month']
        if not to_date and complete_to_month:
            self.add_error('to_date', u'Необходимо указать конечную дату либо выставить параметр complete_to_month=true')

        return to_date

    def get_period_dates(self):
        from_date = self.cleaned_data['from_date']
        to_date = self.cleaned_data['to_date']
        complete_to_month = self.cleaned_data['complete_to_month']
        if not to_date and complete_to_month:
            to_date = datetime.date(
                year=from_date.year,
                month=from_date.month,
                day=calendar.monthrange(from_date.year, from_date.month)[1]
            )
        print 'from_date, to_date', from_date, to_date
        return from_date, to_date


VISIT_TYPES = (
    ('view', u'Просмотр'),
    ('visit', u'Посетители'),
)


class ParamForm(forms.Form):
    visit_type = forms.ChoiceField(label=u'Тип визита', choices=VISIT_TYPES)
    url_filter = forms.CharField(label=u'Фильтр URL (без учета префикса локали)', required=False)
