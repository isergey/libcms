# -*- coding: utf-8 -*-
import re
from django import forms
from django.contrib.auth.models import User, Group
from accounts.models import GroupTitle

from .. import models


class LibraryForm(forms.ModelForm):
    class Meta:
        model = models.Library
        exclude = ('parent',)


class DepartamentForm(forms.ModelForm):
    class Meta:
        model = models.Department
        exclude = ('library',)


class LibraryTypeForm(forms.ModelForm):
    class Meta:
        model = models.LibraryType
        exclude = []


class DistrictForm(forms.ModelForm):
    class Meta:
        model = models.District
        exclude = []



class UserForm(forms.ModelForm):
    password = forms.CharField(
        max_length=64, label=u'Пароль *', required=False,
        help_text=u'Длина пароля от 6-ти символов, должны присутвовать A-Z, a-z, 0-9 и (или) !#$%&?')
    email = forms.EmailField(label=u'Адрес электронной почты', help_text=u'Только в домене @tatar.ru ')
    last_name = forms.CharField(label=u'Фамилия', max_length=30)
    first_name = forms.CharField(label=u'Имя', max_length=30)

    class Meta:
        model = User
        fields = ['email', 'password', 'last_name', 'first_name']

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not email.endswith('@tatar.ru'):
            raise forms.ValidationError(u'Адрес электронной почты должен заканчиваться на @tatar.ru')
        if self.instance.email != email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError(u'Такой адрес уже зарегистрирован')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        email = self.cleaned_data['email']
        email_parts = email.split('@')
        email_check = email
        if len(email_parts) > 1:
            email_check = email_parts[0]

        if password.lower().find(email_check.lower()) > -1:
            raise forms.ValidationError(u'В пароле не должно содержаться часть логина')

        if not self.check_psw(password):
            raise forms.ValidationError(
                u'Длина пароля от 6-ти символов, должны присутвовать A-Z, a-z, 0-9 и (или) !#$%&?')

        if not self.instance.pk and not password:
            raise forms.ValidationError(u'Укажите или сгенерируйте пароль')
        return password

    def check_psw(self, psw):
        return len(psw) >= 6 and \
               bool(re.match("^.*[A-Z]+.*$", psw) and \
                    re.match("^.*[a-z]+.*$", psw) and \
                    (re.match("^.*[0-9]+.*$", psw)) or re.match("^.*[\W]+.*$", psw))


class UserLibraryForm(forms.ModelForm):
    class Meta:
        model = models.UserLibrary
        exclude = ('library', 'user')
        widgets = {
            'roles': forms.CheckboxSelectMultiple()
        }


def get_role_choices():
    groups = Group.objects.filter(name__startswith='role_')
    group_titles = GroupTitle.objects.filter(group__in=groups)

    group_titles_dict = {}

    for group_title in group_titles:
        group_titles_dict[group_title.group_id] = group_title.title
    choices = []
    for group in groups:
        choices.append(
            (group.id, group_titles_dict.get(group.id, group.name))
        )
    return choices


class UserLibraryGroupsFrom(forms.ModelForm):
    class Meta:
        model = User
        fields = ['groups']
        widgets = {
            'groups': forms.CheckboxSelectMultiple
        }


def get_district_form(districts=None):
    if not districts:
        queryset = models.District.objects.all()
    else:
        queryset = models.District.objects.filter(id__in=districts)

    class SelectDistrictForm(forms.Form):
        district = forms.ModelChoiceField(queryset=queryset, label=u'Выберите район', required=False)

    return SelectDistrictForm


class SelectUserPositionForm(forms.Form):
    position = forms.ModelChoiceField(queryset=models.UserLibraryPosition.objects.all(), label=u'Должность',
                                      required=False)


class SelectUserRoleForm(forms.Form):
    role = forms.ModelChoiceField(queryset=Group.objects.filter(name__startswith='role_'), label=u'Роль',
                                  required=False)


class UserAttrForm(forms.Form):
    fio = forms.CharField(
        label=u'',
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': u'ФИО'})
    )
    login = forms.CharField(
        label=u'',
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': u'Логин'})
    )
    email = forms.CharField(
        label=u'',
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': u'Email'})
    )


def get_add_user_library_form(queryset=None):
    if not queryset:
        queryset = models.Library.objects.all()

    class AddUserDistrictForm(forms.Form):
        library = forms.ModelChoiceField(
            queryset=queryset,
            label=u'Выберите библиотеку'
        )

    return AddUserDistrictForm
