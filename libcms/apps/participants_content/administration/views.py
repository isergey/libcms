# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext as _
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required
from common.pagination import get_page
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.utils.translation import to_locale, get_language

#@permission_required_or_403('accounts.view_users')
@login_required
def index(request, library_id):
    return HttpResponse(u'Library content')






