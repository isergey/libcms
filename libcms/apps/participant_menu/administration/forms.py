# -*- coding: utf-8 -*-
from django import forms

from ..models import Menu, MenuItem


class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        exclude = ('root_item', 'library')


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        exclude = ('parent',)


