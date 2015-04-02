# -*- coding: utf-8 -*-
from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _

from menu.models import Menu, MenuTitle, MenuItem, MenuItemTitle


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        exclude = ('root_item',)


class MenuItemTitleForm(forms.ModelForm):
    class Meta:
        model = MenuItemTitle
        exclude = ('item', 'lang')


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        exclude = ('parent',)


class MenuTitleForm(forms.Form):
    lang = forms.ChoiceField(label=u"Language", choices=settings.LANGUAGES, widget=forms.HiddenInput)
    title = forms.CharField(label=_(u'Title'), max_length=512)


# def get_content_form(exclude_list = ('page',)):
#    class ContentForm(forms.ModelForm):
#        class Meta:
#            model=Content
#            exclude = exclude_list
#    return ContentForm

