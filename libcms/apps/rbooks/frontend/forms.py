# -*- coding: utf-8 -*-
from django import forms
from ..models import Bookmarc

class BookmarcForm(forms.ModelForm):
    gen_id = forms.CharField(widget=forms.HiddenInput, max_length=32)
    comments = forms.CharField(widget=forms.Textarea, label=u'Комментарии', required=False)
    page_number = forms.IntegerField(widget=forms.HiddenInput())
    position_x = forms.FloatField(widget=forms.HiddenInput())
    position_y = forms.FloatField(widget=forms.HiddenInput())
    class Meta:
        model = Bookmarc
        exclude = ['user', 'page_number', 'position_x', 'position_y']
