# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
import re
import datetime
from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH
from django.contrib.auth.models import User, Group
from accounts.models import GroupTitle

from .. import models


class LibraryFilterForm(forms.Form):
    org_type = forms.ChoiceField(
        label=u'Тип организации',
        choices=BLANK_CHOICE_DASH + list(models.ORG_TYPES),
        required=False
    )


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
        if not password:
            if not self.instance.pk:
                raise forms.ValidationError(u'Поле обязательно для заполнения')
            else:
                return password

        if not self.check_psw(password):
            raise forms.ValidationError(
                u'Длина пароля от 6-ти символов, должны присутвовать A-Z, a-z, 0-9 и (или) !#$%&?')

        if not self.instance.pk and not password:
            raise forms.ValidationError(u'Укажите или сгенерируйте пароль')
        return password

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password', '')
        email = cleaned_data.get('email', '')
        if not password or not email:
            return
        email_check = email

        if email_check.lower().find(password.lower()) > -1:
            self.add_error('password', u'В пароле не должно содержаться часть логина')

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

    def clean_birth_date(self):
        now = datetime.datetime.now()
        birth_date = self.cleaned_data['birth_date']
        if not birth_date:
            return birth_date
        max_birth_date = now - relativedelta(years=10)
        min_birth_date = now - relativedelta(years=100)
        if birth_date > datetime.date(max_birth_date.year, max_birth_date.month, max_birth_date.day):
            raise forms.ValidationError(u'Дата рождения должна быть меньше %s' % (max_birth_date,))

        if birth_date < datetime.date(min_birth_date.year, min_birth_date.month, min_birth_date.day):
            raise forms.ValidationError(u'Дата рождения должна быть больше %s' % (min_birth_date,))

        return birth_date


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


class WiFiPointForm(forms.ModelForm):
    class Meta:
        model = models.WiFiPoint
        exclude = ['library']


class WiFiPointAttrForm(forms.Form):
    mac = forms.CharField(
        label=u'MAC адрес',
        max_length=17,
        required=False
    )
    status = forms.ChoiceField(
        label=u'Статус',
        choices=BLANK_CHOICE_DASH + list(models.WIFI_POINT_STATUSES),
        required=False,

    )
    comments = forms.CharField(
        label=u'Комментарии',
        max_length=255,
        required=False
    )


class InternetConnectionForm(forms.ModelForm):
    class Meta:
        model = models.InternetConnection
        exclude = ['library']


class InternetConnectionAttrForm(forms.Form):
    is_exist = forms.ChoiceField(
        label=u'Наличие подключения',
        required=False,
        choices=BLANK_CHOICE_DASH + list(models.IS_CONNECTION_EXIST_CHOICES)
    )
    connection_type = forms.ChoiceField(
        label=u'Тип подключения',
        required=False,
        choices=BLANK_CHOICE_DASH + list(models.CONNECTION_TYPE_CHOICES)
    )
    incoming_speed = forms.CharField(
        label=u'Входящая скорость Мб/сек',
        required=False,
        help_text=u'Диапазон указать через "-". Например: 10-20'
    )
    outbound_speed = forms.CharField(
        label=u'Исходящая скорость (Мб/сек)',
        required=False,
        help_text=u'Диапазон указать через "-". Например: 10-20'
    )


class OracleConnectionForm(forms.ModelForm):
    class Meta:
        model=models.OracleConnection
        exclude = ['library']
        widgets = {
            'password': forms.PasswordInput()
        }