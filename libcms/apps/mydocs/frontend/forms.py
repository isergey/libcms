# -*- coding: utf-8 -*-
from django import forms
from ..models import SavedDocument, List


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        exclude = ['user']


def get_saved_document_form(user):
    class SavedDocumentForm(forms.ModelForm):
        gen_id = forms.CharField(widget=forms.HiddenInput, max_length=32)
        list = forms.ModelChoiceField(
            label=u'Список',
            queryset=List.objects.filter(user=user)
        )
        comments = forms.CharField(widget=forms.Textarea, label=u'Комментарии', required=False)

        class Meta:
            model = SavedDocument
            exclude = ['user']
    return SavedDocumentForm

