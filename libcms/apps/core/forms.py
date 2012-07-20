# encoding: utf-8
from django.conf import settings
from django import forms
from django.contrib.auth.models import Group

class LanguageForm(forms.Form):
    lang = forms.ChoiceField(choices=settings.LANGUAGES, label=u"language")

def get_permissions_form(queryset, initial=list()):
    class PermissionsForm(forms.Form):
        perms = forms.ModelMultipleChoiceField(
            initial=initial,
            queryset=queryset,
            widget=forms.CheckboxSelectMultiple,
            required=False
        )

    return PermissionsForm


def get_groups_form(queryset, initial=list()):
    class GroupsForm(forms.Form):
        groups = forms.ModelMultipleChoiceField(queryset=queryset,
            label=u'Группы',
            widget=forms.CheckboxSelectMultiple(),
            required=False,
            initial=initial
        )
    return GroupsForm