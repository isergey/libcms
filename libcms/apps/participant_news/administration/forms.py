# -*- coding: utf-8 -*-
from django import forms

from ..models import News


class NewsForm(forms.ModelForm):
    class Meta:
        model=News
        exclude = ('avatar_img_name', 'library')

