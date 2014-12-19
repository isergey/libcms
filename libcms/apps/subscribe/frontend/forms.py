# encoding: utf-8
from django import forms
from .. import models


class EmailForm(forms.Form):
    email = forms.EmailField(label=u'Адрес email', help_text=u'На этот адрес будут приходить письма рассылки')


def get_subscriber_form(subscribes_qs):
    class SubscriberForm(forms.Form):
        subscribes = forms.ModelMultipleChoiceField(
            queryset=subscribes_qs,
            widget=forms.CheckboxSelectMultiple,
            required=False,
            label=u'Выберите темы:'
        )
    return SubscriberForm
