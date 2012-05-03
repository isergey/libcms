# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group

from pages.models import Page, Content

class PageForm(forms.ModelForm):
    class Meta:
        model=Page
        exclude = ('parent','url_path')
    def __init__(self, parent=None, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        self.parent = parent

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if self.instance.slug:
            return slug
        else:
            if Page.objects.filter(parent=self.parent, slug=slug).count():
                raise forms.ValidationError(u'На этом уровне страницы с таким slug уже существует')
        return slug
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

