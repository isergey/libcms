# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import HttpResponseForbidden
from guardian.decorators import permission_required_or_403
from common.pagination import get_page
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.utils.translation import to_locale, get_language

from ..models import Library, LibraryType, District, LibraryContentEditor
from forms import LibraryForm, LibraryTypeForm, DistrictForm
#@permission_required_or_403('accounts.view_users')

def check_owning(user, library):
    print user, library
    if user.is_superuser:
        return True
    else:
        if LibraryContentEditor.objects.filter(user=user, library=library).count():
            return True
        else:
            return False

def get_cbs(library_node):
    if library_node.parent_id:
        return library_node.get_root()
    else:
        return library_node

def index(request):
    return redirect('participants:administration:list')



#@permission_required_or_403('participants.add_library')
def list(request, parent=None):
    if not request.user.has_module_perms('participants'):
        return HttpResponseForbidden()

    if parent:
        parent = get_object_or_404(Library, id=parent)
        libraries_page = get_page(request, Library.objects.filter(parent=parent))
    else:
        if not request.user.is_superuser:
            cbses = []
            library_content_editors = LibraryContentEditor.objects.filter(user=request.user)
            for lce in library_content_editors:
                cbses.append(lce.library_id)
            libraries_page = get_page(request, Library.objects.filter(id__in=cbses))
        else:
            libraries_page = get_page(request, Library.objects.filter(parent=None))


    return render(request, 'participants/administration/libraries_list.html', {
        'parent': parent,
        'libraries_page': libraries_page,
        })


#@permission_required_or_403('participants.add_library')
@transaction.commit_on_success
def create(request, parent=None):
    if parent:
        if not request.user.has_perm('participants.add_library'):
            return HttpResponse(u'У Вас нет прав на создание филиалов')

        parent = get_object_or_404(Library, id=parent)

        # находим цбс для этого узла и пррверяем, не принадлежит ли пользователь к ней
        cbs = get_cbs(parent)
        if not check_owning(request.user, cbs):
            return HttpResponse(u'У Вас нет прав на создание филиалов в этой ЦБС')

    else:
        # тут происходит создание цбс, проверяем глобальное право
        if not request.user.has_perm('participants.add_cbs'):
            return HttpResponse(u'У Вас нет прав на создание ЦБС')

    if request.method == 'POST':
        library_form = LibraryForm(request.POST, prefix='library_form')

        if library_form.is_valid():
            library = library_form.save(commit=False)
            if parent:
                library.parent = parent

            library.save()
            library.types = library_form.cleaned_data['types']
            if parent:
                return redirect('participants:administration:list', parent=parent.id)
            else:
                return redirect('participants:administration:list')
    else:
        library_form = LibraryForm(prefix='library_form')

    return render(request, 'participants/administration/create_library.html', {
        'parent': parent,
        'library_form': library_form,
        })

#@permission_required_or_403('participants.change_library')
@transaction.commit_on_success
def edit(request, id):
    library =  get_object_or_404(Library, id=id)
    parent = library.parent
    if not parent:
        if not check_owning(request.user, library) or not request.user.has_perm('participants.change_cbs'):
            return HttpResponse(u'У Вас нет прав на редактирование этой ЦБС')
    else:
        cbs = get_cbs(parent)
        if not check_owning(request.user, cbs) or not request.user.has_perm('participants.change_library'):
            return HttpResponse(u'У Вас нет прав на редактирование филиалов в этой ЦБС')

    if request.method == 'POST':
        library_form = LibraryForm(request.POST, prefix='library_form', instance=library)

        if library_form.is_valid():
            library = library_form.save(commit=False)
            library.types = library_form.cleaned_data['types']
            library.save()
            if parent:
                return redirect('participants:administration:list', parent=parent.id)
            else:
                return redirect('participants:administration:list')
    else:
        library_form = LibraryForm(prefix='library_form', instance=library)

    return render(request, 'participants/administration/edit_library.html', {
        'parent': parent,
        'library_form': library_form,
        })



#@permission_required_or_403('participants.delete_library')
@transaction.commit_on_success
def delete(request, id):
    library = get_object_or_404(Library, id=id)
    parent = library.parent
    if not parent:
        if not check_owning(request.user, library) or not request.user.has_perm('participants.delete_cbs'):
            return HttpResponse(u'У Вас нет прав на удаление этой ЦБС')
    else:
        cbs = get_cbs(parent)
        if not check_owning(request.user, cbs) or not request.user.has_perm('participants.delete_library'):
            return HttpResponse(u'У Вас нет прав на удаление филиалов в этой ЦБС')

    library.delete()
    if parent:
        return redirect('participants:administration:list', parent=parent.id)
    else:
        return redirect('participants:administration:list')



#@permission_required_or_403('participants.add_library_type')
def library_types_list(request):
    if not request.user.has_module_perms('participants'):
        return HttpResponseForbidden()

    library_types_page = get_page(request, LibraryType.objects.all())

    return render(request, 'participants/administration/library_types_list.html', {
        'library_types_page': library_types_page,
        })



@permission_required_or_403('participants.add_library_type')
def library_type_create(request):

    if request.method == 'POST':
        library_types_form = LibraryTypeForm(request.POST)

        if library_types_form.is_valid():
            library_types_form.save()
            return redirect('participants:administration:library_types_list')
    else:
        library_types_form = LibraryTypeForm()

    return render(request, 'participants/administration/create_library_type.html', {
        'library_form': library_types_form,
        })


@permission_required_or_403('participants.change_library_type')
@transaction.commit_on_success
def library_type_edit(request, id):
    library_type =  get_object_or_404(LibraryType, id=id)
    if request.method == 'POST':
        library_types_form = LibraryTypeForm(request.POST, instance=library_type)

        if library_types_form.is_valid():
            library_types_form.save()
            return redirect('participants:administration:library_types_list')
    else:
        library_types_form = LibraryTypeForm(instance=library_type)

    return render(request, 'participants/administration/edit_library_type.html', {
        'library_form': library_types_form,
        })


@permission_required_or_403('participants.delete_library_type')
@transaction.commit_on_success
def library_type_delete(request, id):
    library_type =  get_object_or_404(LibraryType, id=id)
    library_type.delete()
    return redirect('participants:administration:library_types_list')


#@permission_required_or_403('participants.add_district')
def district_list(request):
    if not request.user.has_module_perms('participants'):
        return HttpResponseForbidden()
    districts_page = get_page(request, District.objects.all())

    return render(request, 'participants/administration/district_list.html', {
        'districts_page': districts_page,
        })


@permission_required_or_403('participants.add_district')
def district_create(request):

    if request.method == 'POST':
        district_form = DistrictForm(request.POST)

        if district_form.is_valid():
            district_form.save()
            return redirect('participants:administration:district_list')
    else:
        district_form = DistrictForm()

    return render(request, 'participants/administration/create_district.html', {
        'district_form': district_form,
        })


@permission_required_or_403('participants.change_district')
@transaction.commit_on_success
def district_edit(request, id):
    district =  get_object_or_404(District, id=id)
    if request.method == 'POST':
        district_form = DistrictForm(request.POST, instance=district)

        if district_form.is_valid():
            district_form.save()
            return redirect('participants:administration:district_list')
    else:
        district_form = DistrictForm(instance=district)

    return render(request, 'participants/administration/edit_district.html', {
        'district_form': district_form,
        })


@permission_required_or_403('participants.delete_district')
@transaction.commit_on_success
def district_delete(request, id):
    district =  get_object_or_404(District, id=id)
    district.delete()
    return redirect('participants:administration:district_list')