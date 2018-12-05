from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import forms
from . import models

@login_required
def change_email(request):
    form = forms.ChangeEmailForm()
    ruslan_user = models.get_ruslan_user(request)
    return render(request, 'sso_ruslan/change_email.html', {
        'form': form,
    })
