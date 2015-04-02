# -*- coding: utf-8 -*-
from django import forms

from ..models import Page, Content


def get_page_form(parent=None):
    class PageForm(forms.ModelForm):
        class Meta:
            model = Page
            exclude = ('parent', 'library', 'url_path')

        def clean_slug(self):
            slug = self.cleaned_data['slug']
            if self.instance.slug:
                return slug
            else:
                if Page.objects.filter(parent=parent, slug=slug).count():
                    raise forms.ValidationError(u'На этом уровне страницы с таким slug уже существует')
            return slug

    return PageForm


class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        exclude = ('page',)

def get_content_form(exclude_list=('page',)):
    class ContentForm(forms.ModelForm):
        class Meta:
            model = Content
            exclude = exclude_list

    return ContentForm

