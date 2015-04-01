# -*- coding: utf-8 -*-
from django import forms
from captcha.fields import ReCaptchaField

from ..models import Feedback


class FeedbackForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, label=u'Текст отзыва')
    captcha = ReCaptchaField(label=u'Защита от спама')
    class Meta:
        model=Feedback
        exclude = ('comment', 'publicated')
