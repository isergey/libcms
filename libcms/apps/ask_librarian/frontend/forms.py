# -*- encoding: utf-8 -*-

from django import forms
from ..models import Question, Category, Recomendation
from mptt.forms import TreeNodeChoiceField

class QuestionForm(forms.ModelForm):
    category = TreeNodeChoiceField(queryset=Category.objects.all(), required=False, label="Тематика", help_text=u'Укажите тематику, к которой относиться вопрос. Если не знаете - не указывайте.')
    class Meta:
        model = Question
        exclude = ('user', 'answer', 'status', 'create_date', 'manager', 'start_process_date', 'end_process_date')


class RecomendationForm(forms.ModelForm):
    class Meta:
        model = Recomendation
        exclude = ('user', 'question', 'public', 'create_date')