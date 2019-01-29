# -*- encoding: utf-8 -*-
from django import forms
from datetime import date
from django.utils.translation import gettext_lazy as _


def get_years_choice():
    year = date.today().year
    choices = []
    for i, y in enumerate(xrange(year - 1, year + 2)):
        choices.append((y, y))
    return choices


def get_current_year_choice():
    year = date.today().year
    return year


# MONTH_CHOICES = (
#     ('1', _(u"Январь")),
#     ('2', u"Февраль"),
#     ('3', u"Март"),
#     ('4', u"Апрель"),
#     ('5', u"Май"),
#     ('6', u"Июнь"),
#     ('7', u"Июль"),
#     ('8', u"Август"),
#     ('9', u"Сентябрь"),
#     ('10', u"Октябрь"),
#     ('11', u"Ноябрь"),
#     ('12', u"Декабрь"),
# )

MONTH_CHOICES = (
    ('1', _('January')),
    ('2', _('February')),
    ('3', _('March')),
    ('4', _('April')),
    ('5', _('May')),
    ('6', _('June')),
    ('7', _('July')),
    ('8', _('August')),
    ('9', _('September')),
    ('10', _('October')),
    ('11', _('November')),
    ('12', _('December')),
)


def get_current_month_choice():
    month = date.today().month
    return month


class CalendarFilterForm(forms.Form):
    month = forms.ChoiceField(choices=MONTH_CHOICES,
                              label=u"Месяц",
                              widget=forms.Select(attrs={'onchange': 'this.form.submit();', 'class': 'form-control'}))
    year = forms.ChoiceField(choices=get_years_choice(),
                             label=u"Год",
                             widget=forms.Select(attrs={'onchange': 'this.form.submit();', 'class': 'form-control'}))
    # Возвращаем список из предыдущего текущего и следующего года
