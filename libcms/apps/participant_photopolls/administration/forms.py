# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin import widgets

from ..models import PollContent, Poll, PollImage, PollImageContent


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        exclude = ('library',)
        widgets = {
            'start_date': widgets.AdminSplitDateTime(),
            'end_date': widgets.AdminSplitDateTime()
        }


class PollContentForm(forms.ModelForm):
    class Meta:
        model = PollContent
        exclude = ('poll', 'lang')


class PollImageForm(forms.ModelForm):
    class Meta:
        model = PollImage
        exclude = ('poll',)


class PollImageContentForm(forms.ModelForm):
    class Meta:
        model = PollImageContent
        exclude = ('poll_image', 'lang')