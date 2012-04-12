# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required

from participants.models import Library
from ..models import LibReader
from forms import LibReaderForm

@login_required
def index(request):
    return render(request, 'urt/frontend/index.html')

@login_required
def link(request):
    cbses = Library.objects.filter(parent=None)
    if request.method == 'POST':
        form = LibReaderForm(request.POST)
    else:
        form = LibReaderForm()
    return render(request, 'urt/frontend/link.html', {
        'form': form,
        'cbses': cbses
    })