from django import forms
from participants.models import Library

from .. import models


class AvatarForm(forms.ModelForm):
    class Meta:
        model = models.LibraryAvatar
        exclude = ['library', 'width', 'height']


class LibraryInfoForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ['profile', 'phone', 'plans', 'postal_address', 'http_service', 'mail', 'latitude', 'longitude']