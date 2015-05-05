from django import forms
from django.contrib.admin import widgets
from .. import models


class BannerForm(forms.ModelForm):
    class Meta:
        model = models.Banner
        exclude = ['libraries', 'library_creator', 'in_descendants', 'global_banner']
        widgets = {
            'start_date': widgets.AdminSplitDateTime(),
            'end_date': widgets.AdminSplitDateTime()
        }