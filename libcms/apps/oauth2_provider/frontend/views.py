# -*- coding: utf-8 -*-
import urllib
import json
from datetime import datetime, timedelta
from django.shortcuts import HttpResponse, redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required

from . import forms
from .. import models


AUTH_CODE_TIMEOUT = 60 * 60  # Время действия кода для получения токена
AUTH_CODE_LIMIT = 1000  # Количество авторизаций приложения за период  AUTH_CODE_LIMIT_PERIOD
AUTH_CODE_LIMIT_PERIOD = 60 * 60 * 24  # период действия лимита получения кода  аутенификации в секундах


def index(request):
    return HttpResponse(u'Ok')


@login_required
@transaction.atomic()
def authorize(request):
    authorize_from = forms.AuthorizeParamsFrom(request.GET)

    if not authorize_from.is_valid():
        return HttpResponse(u'Некорректные параметры %s' % authorize_from.errors)

    try:
        application = models.Application.objects.values('id').get(
            user=request.user,
            client_id=authorize_from.cleaned_data['client_id']
        )
    except models.Application.DoesNotExist:
        return HttpResponse(u'Client id not found', status=401)

    code = models.generate_uuid()
    params = {
        'code': code
    }

    if authorize_from.cleaned_data['state']:
        params['state'] = authorize_from.cleaned_data['state']

    now = datetime.now()
    limit_period = now + timedelta(seconds=AUTH_CODE_LIMIT_PERIOD)
    expired = now + timedelta(seconds=AUTH_CODE_TIMEOUT)

    if models.AuthCode.filter(application=application['id'], expired__gt=limit_period).count() > AUTH_CODE_LIMIT:
        return HttpResponse(u'Лимит аутентификаций исчерпан')

    models.AuthCode(code=code, application=application['id'], expired=expired).save()

    return redirect(u'%s?%s' % (authorize_from.cleaned_data['redirect_uri'], urllib.urlencode(params)))


@transaction.atomic()
def access_token(request):
    access_token = models.generate_uuid()

    results = {
        'access_token': access_token,
        'scope': 'repo,gist',
        'token_type': 'bearer'
    }
    return HttpResponse(json.dumps(results, ensure_ascii=False), content_type=u'application/json')