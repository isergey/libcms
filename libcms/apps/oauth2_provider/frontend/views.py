# -*- coding: utf-8 -*-
import urllib
import json
from importlib import import_module
from django.conf import settings
from datetime import datetime, timedelta
from django.shortcuts import HttpResponse, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.contrib.auth.decorators import login_required

from . import forms
from .. import models


AUTH_CODE_TIMEOUT = 60 * 60  # Время действия кода для получения токена
AUTH_CODE_LIMIT = 1000  # Количество авторизаций приложения за период  AUTH_CODE_LIMIT_PERIOD
AUTH_CODE_LIMIT_PERIOD = 60 * 60 * 24  # период действия лимита получения кода  аутенификации в секундах
ACCESS_TOKEN_TIMEOUT = 60 * 60 * 24


def index(request):
    return HttpResponse(u'Ok')


@login_required
@transaction.atomic()
def authorize(request):
    authorize_from = forms.AuthorizeParamsFrom(request.GET)

    if not authorize_from.is_valid():
        return HttpResponse(u'Некорректные параметры %s' % authorize_from.errors)

    try:
        application = models.Application.objects.get(
            client_id=authorize_from.cleaned_data['client_id']
        )
    except models.Application.DoesNotExist:
        return HttpResponse(u'Client id not found', status=401)

    if not application.skip_authorization:
        if request.method == 'POST':
            confirm_auth_form = forms.get_confirm_auth_form(request.session.get('oauth_authorization_key', ''))(request.POST)
            if not confirm_auth_form.is_valid():
                return render(request, 'oauth2_provider/frontend/authorize.html', {
                    'form': confirm_auth_form,
                    'application': application
                })
        else:
            authorization_key = models.generate_uuid()
            request.session['oauth_authorization_key'] = authorization_key
            confirm_auth_form = forms.get_confirm_auth_form(authorization_key)(initial={
                'authorization_key': authorization_key
            })

            return render(request, 'oauth2_provider/frontend/authorize.html', {
                'form': confirm_auth_form,
                'application': application
            })

    code = models.generate_uuid()

    params = {
        'code': code
    }

    if authorize_from.cleaned_data['state']:
        params['state'] = authorize_from.cleaned_data['state']

    now = datetime.now()
    limit_period = now + timedelta(seconds=AUTH_CODE_LIMIT_PERIOD)
    expired = now + timedelta(seconds=AUTH_CODE_TIMEOUT)

    if models.AuthCode.objects.filter(application_id=application, expired__gt=limit_period).count() > AUTH_CODE_LIMIT:
        return HttpResponse(u'Лимит аутентификаций исчерпан')

    models.AuthCode(auth_user=request.user, code=code, application=application, expired=expired).save()
    return redirect(u'%s?%s' % (authorize_from.cleaned_data['redirect_uri'], urllib.urlencode(params)))





@csrf_exempt
@require_http_methods(['POST'])
@transaction.atomic()
def access_token(request):
    access_token_form = forms.AccessTokenParamsFrom(request.POST)
    now = datetime.now()
    if not access_token_form.is_valid():
        return HttpResponse(u'Wrong params %s' % access_token_form.errors, status=400)

    try:
        application = models.Application.objects.get(
            client_id=access_token_form.cleaned_data['client_id'],
            client_secret=access_token_form.cleaned_data['client_secret']
        )
    except models.Application.DoesNotExist:
        return HttpResponse(u'Application with client id or client secret does not exists', status=400)

    try:
        auth_code = models.AuthCode.objects.get(application=application, code=access_token_form.cleaned_data['code'])
    except models.AuthCode.DoesNotExist:
        return HttpResponse(u'Wrong auth code', status=400)

    access_token_model = None
    try:
        access_token_model = models.AccessToken.objects.get(
            application=application,
            auth_user_id=auth_code.auth_user_id,
        )
        if access_token_model.expired <= now:
            access_token_model.delete()
            access_token_model = None
    except models.AccessToken.DoesNotExist:
        pass

    if not access_token_model:
        engine = import_module(settings.SESSION_ENGINE)
        expired = now + timedelta(seconds=ACCESS_TOKEN_TIMEOUT)
        session = engine.SessionStore()
        session['oauth'] = 'session_oauth'
        session.set_expiry(expired)
        session.save()
        access_token_model = models.AccessToken(
            auth_user_id=auth_code.auth_user_id,
            token=session.session_key,
            application=application,
            expired=expired
        )
        access_token_model.save()

    auth_code.delete()

    results = {
        'access_token': access_token_model.token,
        # 'scope': 'repo,gist',
        'token_type': 'bearer',
        'expired_in': (access_token_model.expired - now).seconds
    }

    return HttpResponse(json.dumps(results, ensure_ascii=False), content_type=u'application/json')


