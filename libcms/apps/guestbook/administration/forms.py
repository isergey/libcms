# -*- coding: utf-8 -*-
from django import forms

from ..models import Feedback


class FeedbackForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, label=u'Текст отзыва')
    comment = forms.CharField(widget=forms.Textarea, label=u'Текст комментария')

    class Meta:
        model = Feedback
        exclude = []

