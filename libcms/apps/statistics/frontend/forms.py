# coding=utf-8
from django import forms


class ReportForm(forms.Form):
    code = forms.CharField(max_length=255)
