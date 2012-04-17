# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

from participants.models import Library
from ..models import LibReader


class LibReaderForm(forms.ModelForm):
    library = forms.ModelChoiceField(queryset=Library.objects.filter(parent=None).exclude(z_service=''),
        label=u'Укажите ЦБС, в которой Вы получили идентификатор читателя и пароль.'
    )
    lib_password = forms.CharField(widget=forms.PasswordInput, label=u'Пароль, выданный библиотекой')
    class Meta:
        model = LibReader
        exclude = ['user',]

    def clean_library(self):
        library = self.cleaned_data['library']
        # ЦБС на верхнем уровне. Не имеет родителя.
        if library.parent_id:
            raise forms.ValidationError(u'Необходимо выбрать ЦБС')

        return library

class LibReaderAuthForm(forms.ModelForm):
    """
    Связь(аутентификация) с явным указанием библиотеки
    """
    lib_password = forms.CharField(widget=forms.PasswordInput, label=u'Пароль, выданный библиотекой')
    class Meta:
        model = LibReader
        exclude = ['user','library']
