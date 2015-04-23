# -*- coding: utf-8 -*-
import urllib
from django.shortcuts import HttpResponse, redirect
from django.contrib.auth.decorators import login_required

from . import forms
from .. import models


def index(request):
    return HttpResponse(u'Ok')

@login_required
def authorize(request):
    authorize_from = forms.AuthorizeParamsFrom(request.GET)

    if not authorize_from.is_valid():
        return HttpResponse(u'Некорректные параметры %s' % authorize_from.errors)

    try:
        models.Application.objects.get(user=request.user, client_id=authorize_from.cleaned_data['client_id'])
    except models.Application.DoesNotExist:
        return HttpResponse(u'Client id not found', status=401)

    code = models.generate_uuid()
    params = {
        'code': models.generate_uuid()
    }

    if authorize_from.cleaned_data['state']:
        params['state'] = authorize_from.cleaned_data['state']

    return redirect(u'%s?%s' % (authorize_from.cleaned_data['redirect_uri'], urllib.urlencode(params)))