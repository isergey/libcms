# -*- coding: utf-8 -*-
from django.conf import settings
from django import forms


from ..models import Category, CategoryTitle, Question
from mptt.forms import TreeNodeChoiceField

class AnswerQuestionForm(forms.ModelForm):
    category = TreeNodeChoiceField(queryset=Category.objects.all(), required=False, label="Тематика", help_text=u'Если тематика не соотвевует вопросу, укажите другую.')
    class Meta:
        model = Question
        exclude = ('user', 'status', 'create_date', 'manager', 'start_process_date', 'end_process_date')


class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        exclude = ('parent')



class CategoryTitleForm(forms.ModelForm):
    class Meta:
        model=CategoryTitle
        exclude = ('category', 'lang')



