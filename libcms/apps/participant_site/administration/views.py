# coding=utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from  ..import decorators


@login_required
@decorators.must_be_manager
def index(request, library_code, library):
    return render(request, 'participant_site/administration/backend_base.html', {
        'library': library
    })




