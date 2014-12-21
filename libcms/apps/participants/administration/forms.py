# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group

from ..models import Library, LibraryType, District, UserLibrary


class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        exclude = ('parent',)


class LibraryTypeForm(forms.ModelForm):
    class Meta:
        model = LibraryType


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District


class UserLibraryForm(forms.ModelForm):
    class Meta:
        model = UserLibrary
        exclude = ('library',)


# from pages.models import Page, Content
#
#class PageForm(forms.ModelForm):
#    class Meta:
#        model=Page
#        exclude = ('parent',)
#
#class ContentForm(forms.ModelForm):
#    class Meta:
#        model=Content
#        exclude = ('page',)
#
#
#
#def get_content_form(exclude_list = ('page',)):
#    class ContentForm(forms.ModelForm):
#        class Meta:
#            model=Content
#            exclude = exclude_list
#    return ContentForm

