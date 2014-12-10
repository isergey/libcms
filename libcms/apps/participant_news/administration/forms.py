# -*- coding: utf-8 -*-
from django import forms

from ..models import News, NewsImage


class NewsForm(forms.ModelForm):
    class Meta:
        model=News
        exclude = ('avatar_img_name', 'library')


class NewsImageForm(forms.ModelForm):
    class Meta:
        model = NewsImage
        exclude = ('news',)