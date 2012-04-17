# -*- coding: utf-8 -*-
from django import forms
from ..models import SavedDocument

class SavedDocumentForm(forms.ModelForm):
    gen_id = forms.CharField(widget=forms.HiddenInput)
    comments = forms.CharField(widget=forms.Textarea, label=u'Комментарии', required=False)
    class Meta:
        model = SavedDocument
        exclude = ['user']
