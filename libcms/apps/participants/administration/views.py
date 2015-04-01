# -*- coding: utf-8 -*-
import json
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import HttpResponseForbidden
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

from common.pagination import get_page
from ..models import Library, LibraryType, District, LibraryContentEditor, UserLibrary, get_role_groups
from . import forms
from .. import decorators

# @permission_required_or_403('accounts.view_users')
@login_required
def check_owning(user, library):
    if user.is_superuser:
        return True
    else:
        if LibraryContentEditor.objects.filter(user=user, library=library).count():
            return True
        else:
            return False


@login_required
def get_cbs(library_node):
    if library_node.parent_id:
        return library_node.get_root()
    else:
        return library_node


@login_required
def index(request):
    return redirect('participants:administration:list')


@login_required
def detail(request, id):
    org = get_object_or_404(Library, id=id)
    branches = Library.objects.filter(parent=org)
    users = UserLibrary.objects.select_related('user').filter(library=org)
    return render(request, 'participants/administration/detail.html', {
        'org': org,
        'branches': branches,
        'users': users
    })


@login_required
@transaction.atomic()
def add_lib_user(request, id):
    org = get_object_or_404(Library, id=id)
    if request.method == 'POST':
        form = forms.UserLibraryForm(request.POST)
        if form.is_valid():
            ul = form.save(commit=False)
            ul.library = org
            ul.save()
            return redirect('participants:administration:detail', id=org.id)
    else:
        form = forms.UserLibraryForm()

    return render(request, 'participants/administration/add_user.html', {
        'org': org,
        'form': form
    })


@login_required
@transaction.atomic()
def remove_lib_user(request, id):
    ul = get_object_or_404(UserLibrary, id=id)
    ul.delete()
    return redirect('participants:administration:detail', id=ul.library_id)


# @permission_required_or_403('participants.add_library')
@login_required
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


# @permission_required_or_403('participants.add_library')
@login_required
@transaction.atomic()
def create(request, parent=None):
    # if parent:
    # if not request.user.has_perm('participants.add_library'):
    # return HttpResponse(u'У Вас нет прав на создание филиалов')
    #
    #     parent = get_object_or_404(Library, id=parent)
    #
    #     # находим цбс для этого узла и пррверяем, не принадлежит ли пользователь к ней
    #     cbs = get_cbs(parent)
    #     if not check_owning(request.user, cbs):
    #         return HttpResponse(u'У Вас нет прав на создание филиалов в этой ЦБС')
    #
    # else:
    #     # тут происходит создание цбс, проверяем глобальное право
    #     if not request.user.has_perm('participants.add_cbs'):
    #         return HttpResponse(u'У Вас нет прав на создание ЦБС')
    parent_org = None
    if parent:
        parent_org = get_object_or_404(Library, id=parent)
    if request.method == 'POST':
        library_form = forms.LibraryForm(request.POST, prefix='library_form')

        if library_form.is_valid():
            library = library_form.save(commit=False)
            if parent_org:
                library.parent = parent_org

            library.save()
            library.types = library_form.cleaned_data['types']
            library_form.save_m2m()
            if parent:
                return redirect('participants:administration:detail', id=parent_org.id)
            else:
                return redirect('participants:administration:list')
    else:
        library_form = forms.LibraryForm(prefix='library_form')

    return render(request, 'participants/administration/create_library.html', {
        'parent_org': parent_org,
        'library_form': library_form,
    })


# @permission_required_or_403('participants.change_library')
@login_required
@transaction.atomic()
def edit(request, id):
    library = get_object_or_404(Library, id=id)
    parent = library.parent
    # if not parent:
    # if not check_owning(request.user, library) or not request.user.has_perm('participants.change_cbs'):
    #         return HttpResponse(u'У Вас нет прав на редактирование этой ЦБС')
    # else:
    #     cbs = get_cbs(parent)
    #     if not check_owning(request.user, cbs) or not request.user.has_perm('participants.change_library'):
    #         return HttpResponse(u'У Вас нет прав на редактирование филиалов в этой ЦБС')

    if request.method == 'POST':
        library_form = forms.LibraryForm(request.POST, prefix='library_form', instance=library)

        if library_form.is_valid():
            library = library_form.save(commit=False)
            library.types = library_form.cleaned_data['types']
            library.save()
            if parent:
                return redirect('participants:administration:detail', id=parent.id)
            else:
                return redirect('participants:administration:list')
    else:
        library_form = forms.LibraryForm(prefix='library_form', instance=library)

    return render(request, 'participants/administration/edit_library.html', {
        'parent': parent,
        'library_form': library_form,
        'library': library
    })


# @permission_required_or_403('participants.delete_library')
@login_required
@transaction.atomic()
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
@login_required
def library_types_list(request):
    if not request.user.has_module_perms('participants'):
        return HttpResponseForbidden()

    library_types_page = get_page(request, LibraryType.objects.all())

    return render(request, 'participants/administration/library_types_list.html', {
        'library_types_page': library_types_page,
    })


@login_required
@permission_required_or_403('participants.add_library_type')
def library_type_create(request):
    if request.method == 'POST':
        library_types_form = forms.LibraryTypeForm(request.POST)

        if library_types_form.is_valid():
            library_types_form.save()
            return redirect('participants:administration:library_types_list')
    else:
        library_types_form = forms.LibraryTypeForm()

    return render(request, 'participants/administration/create_library_type.html', {
        'library_form': library_types_form,
    })


@permission_required_or_403('participants.change_library_type')
@transaction.atomic()
def library_type_edit(request, id):
    library_type = get_object_or_404(LibraryType, id=id)
    if request.method == 'POST':
        library_types_form = forms.LibraryTypeForm(request.POST, instance=library_type)

        if library_types_form.is_valid():
            library_types_form.save()
            return redirect('participants:administration:library_types_list')
    else:
        library_types_form = forms.LibraryTypeForm(instance=library_type)

    return render(request, 'participants/administration/edit_library_type.html', {
        'library_form': library_types_form,
    })


@permission_required_or_403('participants.delete_library_type')
@transaction.atomic()
def library_type_delete(request, id):
    library_type = get_object_or_404(LibraryType, id=id)
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


@login_required
@permission_required_or_403('participants.add_district')
def district_create(request):
    if request.method == 'POST':
        district_form = forms.DistrictForm(request.POST)

        if district_form.is_valid():
            district_form.save()
            return redirect('participants:administration:district_list')
    else:
        district_form = forms.DistrictForm()

    return render(request, 'participants/administration/create_district.html', {
        'district_form': district_form,
    })


@login_required
@permission_required_or_403('participants.change_district')
@transaction.atomic()
def district_edit(request, id):
    district = get_object_or_404(District, id=id)
    if request.method == 'POST':
        district_form = forms.DistrictForm(request.POST, instance=district)

        if district_form.is_valid():
            district_form.save()
            return redirect('participants:administration:district_list')
    else:
        district_form = forms.DistrictForm(instance=district)

    return render(request, 'participants/administration/edit_district.html', {
        'district_form': district_form,
    })


@login_required
@permission_required_or_403('participants.delete_district')
@transaction.atomic()
def district_delete(request, id):
    district = get_object_or_404(District, id=id)
    district.delete()
    return redirect('participants:administration:district_list')


def _get_user_manager_orgs_qs(managed_libraries):
    managed_orgs = []
    for managed_library in managed_libraries:
        managed_orgs.append(managed_library.library)

    if managed_orgs:
        libs_for_qs = []
        for managed_org in managed_orgs:
            libs_for_qs.append(managed_org.id)
            for descendant in managed_org.get_descendants():
                libs_for_qs.append(descendant.id)

        select_libraries_qs = Library.objects.filter(id__in=libs_for_qs)
    else:
        select_libraries_qs = Library.objects.all()
    return select_libraries_qs



@login_required
@transaction.atomic()
@decorators.must_be_org_user
def library_user_list(request, managed_libraries=[]):

    districts = []
    for managed_library in managed_libraries:
        districts.append(managed_library.library.district_id)
    districts_form = forms.get_district_form(districts)(request.GET, prefix='sdf')

    role_form = forms.SelectUserRoleForm(request.GET, prefix='sur')
    position_form = forms.SelectUserPositionForm(request.GET, prefix='spf')
    user_attr_form = forms.UserAttrForm(request.GET, prefix='uaf')

    select_libraries_qs = _get_user_manager_orgs_qs(managed_libraries)

    select_library_form = forms.get_add_user_library_form(select_libraries_qs)(request.GET, prefix='slf')

    q = Q()

    if districts:
        q = q & Q(library__in=select_libraries_qs)

    if districts_form.is_valid():
        district = districts_form.cleaned_data['district']
        if district:
            q = q & Q(library__district=district)

    if select_library_form.is_valid():
        q = q & Q(library=select_library_form.cleaned_data['library'])

    if role_form.is_valid():
        role = role_form.cleaned_data['role']
        if role:
            q = q & Q(user__groups__in=[role])

    if position_form.is_valid():
        position = position_form.cleaned_data['position']
        if position:
            q = q & Q(position=position)

    if user_attr_form.is_valid():
        fio = user_attr_form.cleaned_data['fio']
        login = user_attr_form.cleaned_data['login']
        email = user_attr_form.cleaned_data['email']
        if fio:
            fio_q = Q()
            fio_parts = fio.split()
            for fio_part in fio_parts:
                fio_q = fio_q | Q(user__first_name__icontains=fio_part) \
                        | Q(user__last_name__icontains=fio_part) \
                        | Q(middle_name__icontains=fio_part)
            q = q & fio_q

        if email:
            q = q & Q(user__email__icontains=email)

        if login:
            q = q & Q(user__username__icontains=login)

    library_user_page = get_page(request,
                                 UserLibrary.objects.select_related('user', 'library','position', 'library__district').filter(q),
                                 20)
    return render(request, 'participants/administration/library_user_list.html', {
        'library_user_page': library_user_page,
        'districts_form': districts_form,
        'role_form': role_form,
        'position_form': position_form,
        'user_attr_form': user_attr_form,
        'managed_libraries': managed_libraries
    })



@login_required
@transaction.atomic()
@permission_required_or_403('participants.add_userlibrary')
@decorators.must_be_org_user
def add_library_user(request, managed_libraries=[]):
    districts = []
    for managed_library in managed_libraries:
        districts.append(managed_library.library.district_id)

    select_libraries_qs = _get_user_manager_orgs_qs(managed_libraries)

    select_district_form = forms.get_district_form(districts)(prefix='sdf')
    library = None
    errors = []
    SelectLibraryForm = forms.get_add_user_library_form(select_libraries_qs)
    if request.method == 'POST':
        all_valid = True
        select_library_form = SelectLibraryForm(request.POST, prefix='slf')

        if not select_library_form.is_valid():
            all_valid = False
            errors.append({'message': 'Выберите организацию'})
        else:
            library = select_library_form.cleaned_data['library']

        user_library_form = forms.UserLibraryForm(request.POST, prefix='ulf')
        if not user_library_form.is_valid():
            all_valid = False

        user_form = forms.UserForm(request.POST, prefix='uf')
        if not user_form.is_valid():
            all_valid = False

        user_library_group_form = forms.UserLibraryGroupsFrom(request.POST, prefix='ulgp')
        if not user_library_group_form.is_valid():
            all_valid = False

        if all_valid:
            user = User(
                username=user_form.cleaned_data['email'],
                email=user_form.cleaned_data['email'],
                first_name=user_form.cleaned_data['first_name'],
                last_name=user_form.cleaned_data['last_name'],
                is_active=True
            )

            user.set_password(user_form.cleaned_data['password'])
            user.save()

            users_group = Group.objects.get(name='users')
            users_group.user_set.add(user)

            selected_groups = set(Group.objects.filter(id__in=user_library_group_form.cleaned_data['groups']))
            for selected_group in selected_groups:
                selected_group.user_set.add(user)

            user_library = user_library_form.save(commit=False)
            user_library.user = user
            user_library.library = select_library_form.cleaned_data['library']
            user_library.save()
            user_library_form.save_m2m()
            return redirect('participants:administration:library_user_list')
    else:
        select_library_form = SelectLibraryForm(request.POST, prefix='slf')
        user_library_group_form = forms.UserLibraryGroupsFrom(prefix='ulgp')
        select_district_form = forms.get_district_form(districts)(prefix='sdf')
        user_library_form = forms.UserLibraryForm(prefix='ulf')
        user_form = forms.UserForm(prefix='uf')

    return render(request, 'participants/administration/add_library_user.html', {
        'select_district_form': select_district_form,
        'select_library_form': select_library_form,
        'user_library_form': user_library_form,
        'user_form': user_form,
        'user_library_group_form':user_library_group_form,
        'library': library,
        'errors': errors,
        'managed_libraries': managed_libraries
    })




@login_required
@transaction.atomic()
@permission_required_or_403('participants.change_userlibrary')
@decorators.must_be_org_user
def edit_library_user(request, id, managed_libraries=[]):
    districts = []
    for managed_library in managed_libraries:
        districts.append(managed_library.library.district_id)

    select_libraries_qs = _get_user_manager_orgs_qs(managed_libraries)

    select_district_form = forms.get_district_form(districts)(prefix='sdf')

    library_user = get_object_or_404(UserLibrary, id=id)

    errors = []
    if request.method == 'POST':
        all_valid = True
        select_library_form = forms.get_add_user_library_form(select_libraries_qs)(request.POST, prefix='slf', )

        if not select_library_form.is_valid():
            all_valid = False
            errors.append({'message': 'Выберите организацию'})

        user_library_form = forms.UserLibraryForm(request.POST, prefix='ulf', instance=library_user)
        if not user_library_form.is_valid():
            all_valid = False

        user_form = forms.UserForm(request.POST, prefix='uf', instance=library_user.user)
        if not user_form.is_valid():
            all_valid = False

        user_library_group_form = forms.UserLibraryGroupsFrom(request.POST, prefix='ulgp')
        if not user_library_group_form.is_valid():
            all_valid = False

        if all_valid:
            user = user_form.save(commit=False)
            if user_form.cleaned_data['password']:
                user.set_password(user_form.cleaned_data['password'])
            user.save()

            role_groups = set(get_role_groups())
            selected_groups = set(Group.objects.filter(id__in=user_library_group_form.cleaned_data['groups']))
            remove_groups = role_groups - selected_groups

            for selected_group in selected_groups:
                selected_group.user_set.add(user)

            for remove_group in remove_groups:
                remove_group.user_set.remove(user)

            user_library = user_library_form.save(commit=False)
            user_library.library = select_library_form.cleaned_data['library']
            user_library.save()
            user_library_form.save_m2m()
            return redirect('participants:administration:library_user_list')
    else:
        user_library_group_form = forms.UserLibraryGroupsFrom(prefix='ulgp', initial={
            'groups': [group.id for group in get_role_groups(library_user.user)]
        })
        select_library_form = forms.get_add_user_library_form(select_libraries_qs)(prefix='slf', initial={
            'library': library_user.library
        })
        user_library_form = forms.UserLibraryForm(prefix='ulf', instance=library_user)
        user_form = forms.UserForm(prefix='uf', instance=library_user.user, initial={
            'password': ''
        })

    return render(request, 'participants/administration/edit_library_user.html', {
        'select_district_form': select_district_form,
        'select_library_form': select_library_form,
        'user_library_form': user_library_form,
        'user_library_group_form': user_library_group_form,
        'user_form': user_form,
        'library_user': library_user,
        'managed_libraries': managed_libraries
    })


@login_required
@transaction.atomic()
@decorators.must_be_org_user
def find_library_by_district(request, managed_libraries=[]):

    if not request.user.has_module_perms('participants'):
        return HttpResponseForbidden()

    district_id = request.GET.get('district_id', None)
    parent_id = request.GET.get('parent_id', None)

    if district_id:
        district = get_object_or_404(District, id=district_id)
    else:
        district = None

    libraries = Library.objects.values('id', 'name').filter(district=district, parent=parent_id)
    lib_list = []

    for library in libraries:
        lib_list.append({
            'id': library['id'],
            'name': library['name']
        })

    return HttpResponse(json.dumps(lib_list, ensure_ascii=False), content_type='application/json')


def _get_children(parent):
    nodes = []
    children = parent.get_descendants()
    for child in children:
        children_nodes = []
        if not child.is_leaf_node():
            children_nodes = _get_children(child)
        nodes.append({
            'id': child.id,
            'name': child.name,
            'children': children_nodes
        })
    return nodes


@login_required
@transaction.atomic()
@decorators.must_be_org_user
def load_libs(request, managed_libraries=[]):
    if not request.user.has_module_perms('participants'):
        return HttpResponseForbidden()

    district_id = request.GET.get('district_id', None)


    q = Q(parent=None)
    if managed_libraries:
        lib_ids = []
        for managed_library in managed_libraries:
            lib_ids.append(managed_library.library_id)
        q = q = Q(id__in=lib_ids)


    if district_id:
        district = get_object_or_404(District, id=district_id)
        q = q & Q(district=district)


    libraries = Library.objects.filter(q)
    nodes = []
    for lib in libraries:
        children = []
        if not lib.is_leaf_node():
            children = _get_children(lib)
        nodes.append({
            'id': lib.id,
            'name': lib.name,
            'children': children
        })

    return HttpResponse(json.dumps(nodes, ensure_ascii=False), content_type='application/json')