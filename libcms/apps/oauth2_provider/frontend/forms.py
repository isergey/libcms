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


def get_confirm_auth_form(authorization_key):
    class ConfirmAuthForm(forms.Form):
        authorization_key = forms.CharField(widget=forms.HiddenInput)

        def clean_authorization_key(self):
            clean_authorization_key = self.cleaned_data['authorization_key']
            if clean_authorization_key != authorization_key:
                raise forms.ValidationError(u'Wrong authorization from key')
            return clean_authorization_key

    return ConfirmAuthForm