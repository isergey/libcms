# encoding: utf-8
from datetime import datetime
from django import forms
from django.contrib.admin import widgets

def get_income_filter_form():
    class Form(forms.Form):
        start_date = forms.DateField(label=u'C',required=False, initial=datetime.now, widget=widgets.AdminDateWidget())
        end_date = forms.DateField(label=u'По', required=False, initial=datetime.now, widget=widgets.AdminDateWidget())
    return Form