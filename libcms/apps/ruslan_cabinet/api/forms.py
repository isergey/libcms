from django.conf import settings
from django import forms

RUSLAN = getattr(settings, 'RUSLAN', {})
ORG_CODES = RUSLAN.get('org_codes', {})

ORG_CODES_CHOISES = [(title, code) for title, code in ORG_CODES.items()]

class GetRecordsForm(forms.Form):
    id_list = forms.CharField(max_length=1024)
    opac = forms.BooleanField(initial=False, required=False)


class MakeReservationForm(forms.Form):
    record_id = forms.CharField(max_length=255)
    org = forms.ChoiceField(choices=ORG_CODES_CHOISES)
    branch = forms.CharField(max_length=255)