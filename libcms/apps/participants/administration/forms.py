# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group

from ..models import Library, LibraryType, District, UserLibrary, UserRole, UserLibraryPosition


class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        exclude = ('parent',)


class LibraryTypeForm(forms.ModelForm):
    class Meta:
        model = LibraryType


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District


class UserForm(forms.ModelForm):
    password = forms.CharField(max_length=64, label=u'Пароль', required=False)
    email = forms.EmailField(label=u'Адрес электронной почты', help_text=u'Только в домене @tatar.ru ')

    class Meta:
        model = User
        fields = ['email', 'password', 'last_name', 'first_name']

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        # if not email.endswith('@tatar.ru'):
        # raise forms.ValidationError(u'Адрес электронной почты должен заканчиваться на @tatar.ru')
        if self.instance.email != email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError(u'Такой адрес1 уже зарегистрирован')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.instance.pk and not password:
            raise forms.ValidationError(u'Укажите или сгенерируйте пароль')
        return password


class UserLibraryForm(forms.ModelForm):
    class Meta:
        model = UserLibrary
        exclude = ('library', 'user')
        widgets = {
            'roles': forms.CheckboxSelectMultiple()
        }


class SelectDistrictForm(forms.Form):
    district = forms.ModelChoiceField(queryset=District.objects.all(), label=u'Выберите район', required=False)


class SelectUserRoleForm(forms.Form):
    role = forms.ModelChoiceField(queryset=UserRole.objects.all(), label=u'Роль', required=False)


class SelectUserPositionForm(forms.Form):
    role = forms.ModelChoiceField(queryset=UserLibraryPosition.objects.all(), label=u'Должность', required=False)


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


def get_add_user_library_form():
    class AddUserDistrictForm(forms.Form):
        library = forms.ModelChoiceField(
            queryset=Library.objects.all(),
            label=u'Выберите библиотеку'
        )

    return AddUserDistrictForm


# class UserLibrary(forms.ModelForm):
# class Meta:
# model = UserLibrary
# exclude = ('library',)


# from pages.models import Page, Content
#
# class PageForm(forms.ModelForm):
# class Meta:
#        model=Page
#        exclude = ('parent',)
#
#class ContentForm(forms.ModelForm):
#    class Meta:
#        model=Content
#        exclude = ('page',)
#
#
#
#def get_content_form(exclude_list = ('page',)):
#    class ContentForm(forms.ModelForm):
#        class Meta:
#            model=Content
#            exclude = exclude_list
#    return ContentForm

