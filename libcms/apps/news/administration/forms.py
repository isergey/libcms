# -*- coding: utf-8 -*-
from django.conf import settings
from django import forms

from news.models import NewsContent, News


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        exclude = []


class NewsContentForm(forms.ModelForm):
    class Meta:
        model = NewsContent
        exclude = ('news', 'lang')




