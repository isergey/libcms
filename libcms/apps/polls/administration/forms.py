# -*- coding: utf-8 -*-
from django import forms
from ..models import Poll, Choice
import datetime


class PollForm(forms.ModelForm):
    start_poll_date = forms.DateTimeField(('%d.%m.%Y %H:%M:%S',), label=u"Дата начала голосования",
                                          widget=forms.DateTimeInput(format='%d.%m.%Y %H:%M:%S'),
                                          initial=datetime.datetime.now()
                                          )
    end_poll_date = forms.DateTimeField(('%d.%m.%Y %H:%M:%S',), label=u"Дата окончания голосования",
                                        widget=forms.DateTimeInput(format='%d.%m.%Y %H:%M:%S'),
                                        initial=datetime.datetime.now()
                                        )

    class Meta:
        model = Poll
        exclude = []

    def clean_end_poll_date(self):
        end_poll_date = self.cleaned_data['end_poll_date']

        start_poll_date = self.cleaned_data.get('start_poll_date')
        if not start_poll_date:
            return end_poll_date

        if end_poll_date < start_poll_date:
            raise forms.ValidationError(u"Дата окончания голосования меньше даты начала")
        return end_poll_date


"""
class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
"""


class ChoiceForm(forms.ModelForm):
    #    choice = forms.CharField(label=u"Вариант ответа",
    #                              max_length=255, required=True)
    #    votes = forms.IntegerField(label=u"Количество голосов", initial=0)
    #    sort = forms.IntegerField(label=u"Сортировка", initial=0)
    class Meta:
        model = Choice
        exclude = ('poll', )

    def clean_votes(self):
        votes = self.cleaned_data['votes']
        if votes < 0:
            raise forms.ValidationError(u"Количество голосов должно быть больше или равно 0")
        return votes
