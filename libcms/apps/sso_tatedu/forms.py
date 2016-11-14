# coding=utf-8
from django import forms


class RuslanAuthForm(forms.Form):
    reader_id = forms.CharField(max_length=128, label=u'Идентификатор читатлеьского билета')
    password = forms.CharField(max_length=128, label=u'Пароль', widget=forms.PasswordInput)
