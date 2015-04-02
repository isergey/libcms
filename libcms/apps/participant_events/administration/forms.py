# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin import widgets

from ..models import EventContent, Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('library',)
        widgets = {
            'start_date': widgets.AdminSplitDateTime(),
            'end_date': widgets.AdminSplitDateTime(),
            'age_category': forms.CheckboxSelectMultiple(),
            'event_type': forms.CheckboxSelectMultiple()
        }


class EventContentForm(forms.ModelForm):
    class Meta:
        model = EventContent
        exclude = ('event', 'lang')




