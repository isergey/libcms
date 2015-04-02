# -*- encoding: utf-8 -*-
from django import forms
from datetime import date
from .. import models


class EventSubscribeForm(forms.ModelForm):
    class Meta:
        model = models.EventSubscribe
        exclude = ('user', 'library', 'create_date')
        widgets = {
            'age_category': forms.CheckboxSelectMultiple(),
            'event_type': forms.CheckboxSelectMultiple()
        }

    def clean_email(self):
        return self.cleaned_data['email'].strip().lower()


class NotificationForm(forms.ModelForm):
    class Meta:
        model = models.EventNotification
        exclude = ('notification_time', 'is_notificated', 'event')

    def clean_email(self):
        return self.cleaned_data['email'].strip().lower()


DAY_CHOISE = (
    (u'1', u'За один день'),
    (u'3', u'За три дня'),
    (u'5', u'За пять дней'),
)

REMEMBER_SYSTEMS_CHOISE = (
    (u'0', u'email'),
    # (u'1', u'sms'),
)


class CommentEventForm(forms.Form):
    text = forms.CharField(min_length=6, max_length=255,
                           label=u"Текст комментария", widget=forms.Textarea)


class AddToFavoriteForm(forms.Form):
    days_for_remember = forms.MultipleChoiceField(choices=DAY_CHOISE,
                                                  widget=forms.CheckboxSelectMultiple(),
                                                  label=u"Напомнить")
    remember_system = forms.ChoiceField(choices=REMEMBER_SYSTEMS_CHOISE, initial='0',
                                        label=u"Выслать напоминания по")


def get_years_choice():
    year = date.today().year
    choices = []
    for i, y in enumerate(xrange(year - 1, year + 2)):
        choices.append((y, y))
    return choices


def get_current_year_choice():
    year = date.today().year
    return year


MONTH_CHOICES = (
    ('1', u"Январь"),
    ('2', u"Февраль"),
    ('3', u"Март"),
    ('4', u"Апрель"),
    ('5', u"Май"),
    ('6', u"Июнь"),
    ('7', u"Июль"),
    ('8', u"Август"),
    ('9', u"Сентябрь"),
    ('10', u"Октябрь"),
    ('11', u"Ноябрь"),
    ('12', u"Декабрь"),
)


def get_current_month_choice():
    month = date.today().month
    return month


class CalendarFilterForm(forms.Form):
    month = forms.ChoiceField(choices=MONTH_CHOICES,
                              label=u"Месяц",
                              widget=forms.Select(attrs={'onchange': 'this.form.submit();'}))
    year = forms.ChoiceField(choices=get_years_choice(),
                             label=u"Год",
                             widget=forms.Select(attrs={'onchange': 'this.form.submit();'}))
    #Возвращаем список из предыдущего текущего и следующего года