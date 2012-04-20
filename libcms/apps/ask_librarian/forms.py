# -*- coding: utf-8 -*-
from django import forms
from models import Question, AnswerLanguage, Category
from mptt.forms import TreeNodeChoiceField

class QuestionForm(forms.ModelForm):
    answer_language = forms.ModelMultipleChoiceField(
        queryset=AnswerLanguage.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    category = TreeNodeChoiceField(
        queryset=Category.objects.all(),
        required=False,
        #widget=TreeNodeChoiceField
    )
    class Meta:
        model = Question
        exclude = ['user']

