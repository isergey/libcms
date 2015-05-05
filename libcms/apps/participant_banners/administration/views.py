# coding=utf-8
from datetime import datetime
from django.conf import settings
from django.shortcuts import HttpResponse, render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required
from django.db import transaction
from common.pagination import get_page

from participants import decorators, org_utils

from .. import models
import forms

@login_required
@decorators.must_be_org_user
def index(request, library_code, lang='ru', managed_libraries=[]):
    now = datetime.now()
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    if not request.user.has_module_perms('participant_banners'):
        return HttpResponseForbidden(u'У вас нет прав для доступа к разделу')

    banners_page = get_page(request, models.Banner.objects.filter(library_creator=library.id, lang=lang))

    return render(request, 'participant_banners/administration/index.html', {
        'banners_page': banners_page,
        'library': library,
        'languages': settings.LANGUAGES,
        'current_lang': lang,
        'now': now
    })

@login_required
@permission_required_or_403('participant_banners.add_banner')
@decorators.must_be_org_user
@transaction.atomic()
def create(request, library_code, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    if request.method == 'POST':
        banner_form = forms.BannerForm(request.POST, request.FILES)
        if banner_form.is_valid():
            banner = banner_form.save(commit=False)
            banner.library_creator = library
            banner.save()
            banner.libraries.add(library)
            return redirect('participant_banners:administration:index', library_code=library_code, lang=banner.lang)
    else:
        banner_form = forms.BannerForm()
    return render(request, 'participant_banners/administration/create_banner.html', {
        'library': library,
        'banner_form': banner_form
    })


@login_required
@permission_required_or_403('participant_banners.change_banner')
@decorators.must_be_org_user
@transaction.atomic()
def edit(request, library_code, id, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    banner = get_object_or_404(models.Banner, id=id, library_creator=library.id)
    if request.method == 'POST':
        banner_form = forms.BannerForm(request.POST, request.FILES, instance=banner)
        if banner_form.is_valid():
            banner = banner_form.save(commit=False)
            banner.save()
            return redirect('participant_banners:administration:index', library_code=library_code, lang=banner.lang)
    else:
        banner_form = forms.BannerForm(instance=banner)

    return render(request, 'participant_banners/administration/edit_banner.html', {
        'library': library,
        'banner': banner,
        'banner_form': banner_form
    })


@login_required
@permission_required_or_403('participant_banners.delete_banner')
@decorators.must_be_org_user
@transaction.atomic()
def delete(request, library_code, id, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    banner = get_object_or_404(models.Banner, id=id, library_creator=library.id)
    banner.delete()
    return redirect('participant_banners:administration:index', library_code=library_code, lang=banner.lang)


@login_required
@permission_required_or_403('participant_banners.change_banner')
@decorators.must_be_org_user
@transaction.atomic()
def toggle_active(request, library_code, id, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    banner = get_object_or_404(models.Banner, id=id, library_creator=library.id)
    banner.active = not banner.active
    banner.save()
    return redirect('participant_banners:administration:index', library_code=library_code, lang=banner.lang)


@login_required
@permission_required_or_403('participant_banners.bind_to_descendants')
@decorators.must_be_org_user
@transaction.atomic()
def bind_to_children_orgs(request, library_code, id, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    banner = get_object_or_404(models.Banner, id=id, library_creator=library.id)

    for descedant in library.get_descendants():
        banner.libraries.add(descedant)
    banner.in_descendants = True
    banner.save()
    return redirect('participant_banners:administration:index', library_code=library_code, lang=banner.lang)


@login_required
@permission_required_or_403('participant_banners.bind_to_descendants')
@decorators.must_be_org_user
@transaction.atomic()
def unbind_to_children_orgs(request, library_code, id, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    banner = get_object_or_404(models.Banner, id=id, library_creator=library.id)

    for descedant in library.get_descendants():
        banner.libraries.remove(descedant)
    banner.in_descendants = False
    banner.save()
    return redirect('participant_banners:administration:index', library_code=library_code, lang=banner.lang)