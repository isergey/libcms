# -*- coding: utf-8 -*-
from django import forms
from participants.models import Library

class OrderForm(forms.Form):
    gen_id = forms.CharField(max_length=32, widget=forms.HiddenInput)
    manager_id = forms.IntegerField(label=u'Укажите библиотеку в которой хотите получить заказ', widget=forms.Select(attrs={'class':'hiden'}))
    comments = forms.CharField(max_length=1024, required=False, label=u'Коментарии к заказу', widget=forms.Textarea)

    def clean_manager_id(self):
        manager_id = self.cleaned_data['manager_id']
        if not Library.objects.filter(id=manager_id).exclude(parent=None).count():
            raise forms.ValidationError(u'Wrong library select')
        return manager_id


class CopyOrderForm(OrderForm):
    copy_info = forms.CharField(
        max_length=1024,
        required=False,
        label=u'Информация о копировании',
        widget=forms.Textarea, help_text=u'Укажите содержание документа, которое необходимо скопировать')

class DeliveryOrderForm(OrderForm):
    pass
