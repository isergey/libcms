from django import forms
from .. import models


class ItemForm(forms.ModelForm):
    class Meta:
        model = models.Item
        exclude = []


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = models.ItemAttachment
        exclude = ['item']