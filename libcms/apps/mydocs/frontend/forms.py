# -*- coding: utf-8 -*-
from django import forms
from ..models import SavedDocument, List


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        exclude = ['user']


class SavedDocumentForm(forms.ModelForm):
    gen_id = forms.CharField(widget=forms.HiddenInput, max_length=32)
    comments = forms.CharField(widget=forms.Textarea, label=u'Комментарии', required=False)

    class Meta:
        model = SavedDocument
        exclude = ['user']
