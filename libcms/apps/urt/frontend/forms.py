# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=50, label=u"Логин", help_text=u"Разрешены буквы латинского алфавита и цифры")
    password = forms.CharField( min_length=6, max_length=50,
        label=u"Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(min_length=6, max_length=50,
        label=u"Повторите пароль", widget=forms.PasswordInput)
    email = forms.EmailField(label=u"Электронная почта")
    first_name = forms.CharField(max_length=50, label=u"Имя")
    last_name = forms.CharField(max_length=50, label=u"Фамилия")

    def clean_username(self):
        import re
        format = re.compile(r"^[a-zA-z0-9]+$")
        if re.match(format,self.cleaned_data["username"]) == None:
            raise forms.ValidationError(u"Имя пользователя может содержать только латинские символы")

        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise forms.ValidationError(u"Такой логин уже существует.")
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise forms.ValidationError(u"Такой email уже зарегистрирован.")


    def clean_password2(self):
        password = self.cleaned_data.get("password", "")
        password2 = self.cleaned_data["password2"]
        if password != password2:
            raise forms.ValidationError(u'пароли не совпадают')
        return password2

