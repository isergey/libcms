# coding=utf-8
from django import forms
from django.core.validators import RegexValidator
from django.contrib.admin import widgets
from .. import models

validator = RegexValidator(regex=r'^[/_\-0-9A-Za-z\s\.]+$', message=u'Допускаются цифры, символы "_", "-", ".", латинские буквы, пробелы')


class BannerForm(forms.ModelForm):
    class Meta:
        model = models.Banner
        exclude = ['libraries', 'library_creator', 'in_descendants', 'global_banner']
        widgets = {
            'start_date': widgets.AdminSplitDateTime(),
            'end_date': widgets.AdminSplitDateTime()
        }

    def clean_image(self):
        image = self.cleaned_data['image']
        validator(image)
        return image