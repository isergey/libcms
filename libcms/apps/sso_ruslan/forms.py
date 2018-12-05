# coding=utf-8
from django import forms


class ChangeEmailForm(forms.Form):
    email = forms.EmailField(
        max_length=256,
        required=True,
        label=u'Новый адрес электронной почты'
    )
