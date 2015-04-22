from django import forms


class AuthorizeParamsFrom(forms.Form):
    client_id = forms.CharField(max_length=128)
    redirect_uri = forms.URLField(max_length=255)
    scope = forms.CharField(max_length=255, required=False)
    state = forms.CharField(max_length=255, required=False)