# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User


from ..models import LibReader

class LibReaderForm(forms.ModelForm):
    class Meta:
        model = LibReader
        exclude = ['user', 'library']