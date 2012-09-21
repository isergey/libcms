# -*- coding: utf-8 -*-
from django import forms

from ..models import Item, ItemContent

class ItemForm(forms.ModelForm):
    class Meta:
        model=Item
        exclude = ('avatar_img_name',)

class ItemContentForm(forms.ModelForm):
    class Meta:
        model=ItemContent
        exclude = ('item', 'lang')
