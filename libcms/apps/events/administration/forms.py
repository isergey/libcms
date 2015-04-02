# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin import widgets

from events.models import EventContent, Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = []

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget = widgets.AdminSplitDateTime()
        self.fields['end_date'].widget = widgets.AdminSplitDateTime()


class EventContentForm(forms.ModelForm):
    class Meta:
        model = EventContent
        exclude = ('event', 'lang')




