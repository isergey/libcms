# coding=utf-8
from lxml import etree
from django import forms

from ..transformers import transformers

TRANSFORMERS_CHOICES = []
for key in transformers.keys():
    TRANSFORMERS_CHOICES.append((key, key))


class TransformForm(forms.Form):
    transformer = forms.ChoiceField(choices=TRANSFORMERS_CHOICES)
    xml = forms.CharField(
        max_length=1024 * 1024,
        widget=forms.Textarea,
        help_text=u'Не указывйте параметр кодировки в xml декларации'
    )

    def clean_xml(self):
        xml = self.cleaned_data['xml']
        try:
            etree.fromstring(xml.encode('utf-8'))
        except etree.Error as e:
            raise forms.ValidationError(u'Некорректный xml: %s' % (e.message, ))
        except ValueError as e:
            raise forms.ValidationError(u'Некорректный xml: %s' % (e.message, ))
        return xml