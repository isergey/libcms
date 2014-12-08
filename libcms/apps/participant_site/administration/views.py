# coding=utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .. import decorators
import forms
from .. import models


@login_required
@decorators.must_be_manager
def index(request, library_code, library):
    return render(request, 'participant_site/administration/backend_base.html', {
        'library': library
    })

@login_required
@decorators.must_be_manager
@transaction.atomic
def edit_info(request, library_code, library):
    try:
        avatar = models.LibraryAvatar.objects.get(library=library)
    except models.LibraryAvatar.DoesNotExist:
        avatar = None


    if request.method == 'POST':
        avatar_from = forms.AvatarForm(request.POST, request.FILES, prefix='avatar_from', instance=avatar)
        library_form = forms.LibraryInfoForm(request.POST, prefix='library_form', instance=library)
        if avatar_from.is_valid() and library_form.is_valid():
            avatar = avatar_from.save(commit=False)
            avatar.library = library
            avatar.save()
            library_form.save()
    else:
        avatar_from = forms.AvatarForm(prefix='avatar_from', instance=avatar)
        library_form = forms.LibraryInfoForm(prefix='library_form', instance=library)
    return render(request, 'participant_site/administration/edit_info.html', {
        'avatar_from': avatar_from,
        'library_form': library_form,
        'library': library
    })

