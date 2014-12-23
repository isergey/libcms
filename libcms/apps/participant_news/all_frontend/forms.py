# coding=utf-8
from django import forms
from .. import models


class NewsFilter(forms.Form):
    library = forms.ModelChoiceField(
        label=u'По библиотеке:',
        empty_label=u'Выберите из списка',
        required=False,
        queryset=models.Library.objects.filter(parent=None)
    )
