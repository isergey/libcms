# -*- coding: utf-8 -*-
from django import forms
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group


class UserForm(forms.ModelForm):
    password = forms.CharField(
        label=_(u'Password'),
        required=False,
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        exclude = [
            'password',
            'is_staff',
            'last_login',
            'date_joined'
        ]
        widgets = {
            'groups': forms.CheckboxSelectMultiple(),
        }


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['name'].help_text = u"Может содержать только латинские буквы, цифры и знак подчеркивания"
        self.fields['name'].validators = [validators.validate_slug]
        self.fields.keyOrder = ['name', 'permissions']


