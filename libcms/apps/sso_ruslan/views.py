# coding=utf-8
from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from ruslan import connection_pool, humanize, grs, client
from . import forms
from . import models

RUSLAN = getattr(settings, 'RUSLAN', {})
API_ADDRESS = RUSLAN.get('api_address', 'http://localhost/')
API_USERNAME = RUSLAN.get('username')
API_PASSWORD = RUSLAN.get('password')
RUSLAN_USERS_DATABASE = RUSLAN.get('users_database', 'allusers')

EMAIL_FIELD_TAG = '122'
RECORD_ID_TAG = '1'


@login_required
def change_email(request):
    try:
        models.RuslanUser.objects.get(user=request.user)
    except models.RuslanUser.DoesNotExist:
        return HttpResponse(u'Вы не являетесь читателем')
    ruslan_user = models.get_ruslan_user(request)
    portal_client = connection_pool.get_client(API_ADDRESS, API_USERNAME, API_PASSWORD)
    sru_response = portal_client.get_user(ruslan_user.username, RUSLAN_USERS_DATABASE)
    sru_records = humanize.get_records(sru_response)

    if not sru_records:
        return HttpResponse(u'Не найден читатель')

    record_content = humanize.get_record_content(sru_records[0])
    grs_record = grs.Record.from_dict(record_content)
    if request.method == 'POST':
        form = forms.ChangeEmailForm(request.POST)
        if form.is_valid():
            email_fields = grs_record.get_field(EMAIL_FIELD_TAG)
            if email_fields:
                email_fields[0].content = form.cleaned_data['email']
                portal_client.update_grs(grs_record, RUSLAN_USERS_DATABASE, grs_record.get_field_value(RECORD_ID_TAG))
    else:
        form = forms.ChangeEmailForm()

    current_email = grs_record.get_field_value(EMAIL_FIELD_TAG, '')
    return render(request, 'sso_ruslan/change_email.html', {
        'form': form,
        'current_email': current_email,
    })
