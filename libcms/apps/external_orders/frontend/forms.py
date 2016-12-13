# coding=utf-8
from django import forms


class OrderForm(forms.Form):
    last_name = forms.CharField(
        label=u'Фамилия',
        max_length=64,
        required=True
    )
    first_name = forms.CharField(
        label=u'Имя',
        max_length=64,
        required=True
    )
    patronymic_name = forms.CharField(
        label=u'Отчество',
        max_length=64,
    )
    email = forms.EmailField(
        label=u'Адрес электронной почты',
        max_length=64,
        required=True,
    )
    phone = forms.RegexField(
        label=u'Телефон',
        regex=r'^\+7\d{9,15}$',
        error_message=u'Телефон должен быть в формате: "+71234567890"',
        required=False,
        help_text=u'Телефон должен быть в формате: "+71234567890". Используется для связи с Вами'
    )
