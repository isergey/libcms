# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group

from ..models import Page, Content

class PageForm(forms.ModelForm):
    class Meta:
        model=Page
        exclude = ('parent', 'library', 'url_path')

class ContentForm(forms.ModelForm):
    class Meta:
        model=Content
        exclude = ('page',)



def get_content_form(exclude_list = ('page',)):
    class ContentForm(forms.ModelForm):
        class Meta:
            model=Content
            exclude = exclude_list
    return ContentForm

