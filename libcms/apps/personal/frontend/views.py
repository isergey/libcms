# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from sso_ruslan import models as ruslan_models
from participants.models import Library


@login_required
def index(request):
    # try:
    #     lib_reader = LibReader.objects.get(user=request.user)
    # except LibReader.DoesNotExist:
    #     lib_reader = None
    org_id = request.session.get('org_id')
    current_library = None
    if org_id:
        try:
            current_library = Library.objects.get(id=org_id)
        except Library.DoesNotExist:
            pass

    ruslan_user = ruslan_models.get_ruslan_user(request)
    return render(request, 'personal/frontend/index.html', {
        'ruslan_user': ruslan_user,
        'current_library': current_library
    })
