from django import forms


class AuthorizeParamsFrom(forms.Form):
    client_id = forms.CharField(max_length=128)
    redirect_uri = forms.URLField(max_length=255)
    scope = forms.CharField(max_length=255, required=False)
    state = forms.CharField(max_length=255, required=False)


class AccessTokenParamsFrom(forms.Form):
    client_id = forms.CharField(max_length=128)
    client_secret = forms.CharField(max_length=128)
    code = forms.CharField(max_length=128)
    redirect_uri = forms.URLField(max_length=255)