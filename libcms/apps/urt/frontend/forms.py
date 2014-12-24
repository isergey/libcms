# -*- encoding: utf-8 -*-
from django import forms
from ..models import LibReader


class LibReaderForm(forms.ModelForm):
    password = forms.CharField(
        label=u'Пароль',
        required=True,
        max_length=255,
        help_text=u'Введите пароль, который Вы получили в библиотке',
        widget=forms.PasswordInput
    )
    class Meta:
        model = LibReader
        exclude = ['user',]
        widgets = {
            'lib_password': forms.PasswordInput
        }

    def clean_reader_id(self):
        reader_id = self.cleaned_data['reader_id']
        if LibReader.objects.filter(reader_id=reader_id).exists():
            raise forms.ValidationError(u'Читательский билет уже зарегистрирован')
        return reader_id

class LibReaderAuthForm(forms.ModelForm):
    """
    Связь(аутентификация) с явным указанием библиотеки
    """
    lib_password = forms.CharField(widget=forms.PasswordInput, label=u'Пароль, выданный библиотекой')
    class Meta:
        model = LibReader
        exclude = ['user','library']
