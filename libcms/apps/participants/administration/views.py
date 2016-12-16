# -*- coding: utf-8 -*-
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core import serializers
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q, Count
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, resolve_url
from guardian.decorators import permission_required_or_403

from accounts import models as accounts_models
from common.pagination import get_page
from . import forms
from .. import decorators
from .. import models

SITE_DOMAIN = getattr(settings, 'SITE_DOMAIN', 'http://localhost')


def check_owning(user, library):
    if user.is_superuser:
        return True
    else:
        if models.LibraryContentEditor.objects.filter(user=user, library=library).count():
            return True
        else:
            return False


def get_cbs(library_node):
    if library_node.parent_id:
        return library_node.get_root()
    else:
        return library_node


@login_required
def index(request):
    return redirect('participants:administration:list')


@login_required
@decorators.must_be_org_user
def detail(request, id, managed_libraries=None):
    managed_libraries = managed_libraries or []
    managed_libraries_id = [managed_library.id for managed_library in managed_libraries]
    can_manage = False
    if int(id) in managed_libraries_id:
        can_manage = True

    org = get_object_or_404(models.Library, id=id)
    branches = models.Library.objects.filter(parent=org)
    departments = models.Department.objects.filter(library=org)
    library_users = models.UserLibrary.objects.filter(library=org)
    wifi_points = models.WiFiPoint.objects.filter(library=org)
    int_connections = models.InternetConnection.objects.filter(library=org)
    ora_connections = models.OracleConnection.objects.filter(library=org)
    return render(request, 'participants/administration/detail.html', {
        'org': org,
        'branches': branches,
        'departments': departments,
        'library_users': library_users,
        'wifi_points': wifi_points,
        'int_connections': int_connections,
        'ora_connections': ora_connections,
        'can_manage': can_manage
    })


@login_required
@transaction.atomic()
@permission_required_or_403('participants.add_department')
def get_departments(request):
    library_id = request.GET.get('library_id', '0')
    library = get_object_or_404(models.Library, id=library_id)
    departments = models.Department.objects.filter(library=library)
    data = serializers.serialize("json", departments)
    return HttpResponse(data, content_type=u'application/json')


@login_required
@transaction.atomic()
@permission_required_or_403('participants.change_department')
def department_detail(request, id):
    department = get_object_or_404(models.Department, id=id)
    return render(request, 'participants/administration/department_detail.html', {
        'department': department,
    })


@login_required
@transaction.atomic()
@permission_required_or_403('participants.add_department')
def create_department(request, library_id):
    library = get_object_or_404(models.Library, id=library_id)
    if request.method == 'POST':
        form = forms.DepartamentForm(request.POST)
        form.fields['parent'].queryset = models.Department.objects.filter(library_id=library_id)
        if form.is_valid():
            department = form.save(commit=False)
            department.library = library
            department.save()
            return redirect('participants:administration:detail', id=library_id)
    else:
        form = forms.DepartamentForm()
        form.fields['parent'].queryset = models.Department.objects.filter(library_id=library_id)
    return render(request, 'participants/administration/create_department.html', {
        'form': form,
        'library': library
    })


@login_required
@transaction.atomic()
@permission_required_or_403('participants.change_department')
def edit_department(request, id):
    department = get_object_or_404(models.Department, id=id)
    if request.method == 'POST':
        form = forms.DepartamentForm(request.POST, instance=department)
        form.fields['parent'].queryset = models.Department.objects.filter(library_id=department.library_id)
        if form.is_valid():
            form.save()
            return redirect('participants:administration:detail', id=department.library_id)
    else:
        form = forms.DepartamentForm(instance=department)
        form.fields['parent'].queryset = models.Department.objects.filter(library_id=department.library_id)
    return render(request, 'participants/administration/edit_department.html', {
        'form': form,
        'library': department.library
    })


@login_required
@transaction.atomic()
@permission_required_or_403('participants.delete_department')
def delete_department(request, id):
    department = get_object_or_404(models.Department, id=id)
    department.delete()
    return redirect('participants:administration:detail', id=department.library_id)


# @permission_required_or_403('participants.add_library')
@login_required
def list(request, parent=None):
    if not request.user.has_module_perms('participants'):
        return HttpResponseForbidden()

    if parent:
        parent = get_object_or_404(models.Library, id=parent)
        libraries_page = get_page(request, models.Library.objects.filter(parent=parent))
    else:
        libraries_page = get_page(request, models.Library.objects.filter(parent=None))

    return render(request, 'participants/administration/libraries_list.html', {
        'parent': parent,
        'libraries_page': libraries_page,
    })


@permission_required_or_403('participants.add_library')
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
        parent_org = get_object_or_404(models.Library, id=parent)
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


@permission_required_or_403('participants.change_library')
@login_required
@transaction.atomic()
def edit(request, id):
    library = get_object_or_404(models.Library, id=id)
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


@permission_required_or_403('participants.delete_library')
@login_required
@transaction.atomic()
def delete(request, id):
    library = get_object_or_404(models.Library, id=id)
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


# @permission_required_or_403('participants.add_library_type')
@login_required
def library_types_list(request):
    if not request.user.has_module_perms('participants'):
        return HttpResponseForbidden()

    library_types_page = get_page(request, models.LibraryType.objects.all())

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
    library_type = get_object_or_404(models.LibraryType, id=id)
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
    library_type = get_object_or_404(models.LibraryType, id=id)
    library_type.delete()
    return redirect('participants:administration:library_types_list')


# @permission_required_or_403('participants.add_district')
def district_list(request):
    if not request.user.has_module_perms('participants'):
        return HttpResponseForbidden()
    districts_page = get_page(request, models.District.objects.all())

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
    district = get_object_or_404(models.District, id=id)
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
    district = get_object_or_404(models.District, id=id)
    district.delete()
    return redirect('participants:administration:district_list')


def _get_user_manager_orgs_qs(managed_libraries):
    managed_orgs = []
    for managed_library in managed_libraries:
        managed_orgs.append(managed_library)

    if managed_orgs:
        libs_for_qs = []
        for managed_org in managed_orgs:
            libs_for_qs.append(managed_org.id)
            for descendant in managed_org.get_descendants():
                libs_for_qs.append(descendant.id)

        select_libraries_qs = models.Library.objects.filter(id__in=libs_for_qs)
    else:
        select_libraries_qs = models.Library.objects.all()
    return select_libraries_qs


@login_required
@transaction.atomic()
@decorators.must_be_org_user
def library_user_list(request, managed_libraries=[]):
    districts = []
    for managed_library in managed_libraries:
        districts.append(managed_library.district_id)
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

    library_user_page = get_page(
        request,
        models.UserLibrary.objects.select_related('user', 'library', 'position', 'library__district').filter(q),
        20
    )
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
def add_library_user(request, library_id, managed_libraries=[]):
    managed_libray_ids = [unicode(managed_library.id) for managed_library in managed_libraries]

    if managed_libray_ids and library_id not in managed_libray_ids:
        return HttpResponseForbidden(u'Вы не можете обслуживать эту организацию')

    library = get_object_or_404(models.Library, id=library_id)
    roles_queryset = Group.objects.filter(name__startswith='role_')
    if request.method == 'POST':
        user_form = forms.UserForm(request.POST, prefix='user_form')

        user_library_form = forms.UserLibraryForm(request.POST, prefix='user_library_form')
        user_library_form.fields['department'].queryset = models.Department.objects.filter(library=library)
        user_roles_from = forms.UserLibraryGroupsFrom(request.POST, prefix='user_roles_from')
        user_roles_from.fields['groups'].queryset = roles_queryset

        if user_form.is_valid() and user_library_form.is_valid() and user_roles_from.is_valid():
            user = user_form.save(commit=False)
            user.username = user_form.cleaned_data['email']
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            accounts_models.create_or_update_password(user, user_form.cleaned_data['password'])

            user_library = user_library_form.save(commit=False)
            user_library.user = user
            user_library.library = library
            user_library.save()

            user_roles_from = forms.UserLibraryGroupsFrom(request.POST, prefix='user_roles_from', instance=user)
            user_roles_from.fields['groups'].queryset = roles_queryset
            if user_roles_from.is_valid():
                user_roles_from.save()
            send_user_create_email(user, user_form.cleaned_data['password'])

            return redirect('participants:administration:detail', id=library.id)
    else:
        user_form = forms.UserForm(prefix='user_form')
        user_library_form = forms.UserLibraryForm(prefix='user_library_form')
        user_library_form.fields['department'].queryset = models.Department.objects.filter(library=library)
        user_roles_from = forms.UserLibraryGroupsFrom(prefix='user_roles_from')
        user_roles_from.fields['groups'].queryset = roles_queryset
    return render(request, 'participants/administration/add_library_user.html', {
        'library': library,
        'user_form': user_form,
        'user_library_form': user_library_form,
        'user_roles_from': user_roles_from
    })


@login_required
@transaction.atomic()
@permission_required_or_403('participants.change_userlibrary')
@decorators.must_be_org_user
def edit_library_user(request, id, managed_libraries=[]):
    user_library = get_object_or_404(models.UserLibrary, id=id)
    managed_libray_ids = [managed_library.id for managed_library in managed_libraries]

    if managed_libray_ids and user_library.library_id not in managed_libray_ids:
        return HttpResponseForbidden(u'Вы не можете обслуживать эту организацию')

    library = user_library.library
    if request.method == 'POST':
        user_form = forms.UserForm(request.POST, prefix='user_form', instance=user_library.user)

        user_library_form = forms.UserLibraryForm(request.POST, prefix='user_library_form', instance=user_library)
        user_library_form.fields['department'].queryset = models.Department.objects.filter(library=library)

        user_roles_from = forms.UserLibraryGroupsFrom(request.POST, prefix='user_roles_from',
                                                      instance=user_library.user)
        user_roles_from.fields['groups'].queryset = Group.objects.filter(name__startswith='role_')

        if user_form.is_valid() and user_library_form.is_valid() and user_roles_from.is_valid():
            user = user_form.save(commit=False)
            user.username = user_form.cleaned_data['email']
            if user_form.cleaned_data['password']:
                user.set_password(user_form.cleaned_data['password'])
                accounts_models.create_or_update_password(user, user_form.cleaned_data['password'])
            user.save()

            user_library = user_library_form.save(commit=False)
            user_library.user = user
            user_library.library = library
            user_library.save()

            user_roles_from.save()
            return redirect('participants:administration:detail', id=library.id)
    else:
        user_form = forms.UserForm(initial={'password': ''}, prefix='user_form', instance=user_library.user)
        user_library_form = forms.UserLibraryForm(prefix='user_library_form', instance=user_library)
        user_library_form.fields['department'].queryset = models.Department.objects.filter(library=library)
        user_roles_from = forms.UserLibraryGroupsFrom(prefix='user_roles_from', instance=user_library.user)
        user_roles_from.fields['groups'].queryset = Group.objects.filter(name__startswith='role_')

    return render(request, 'participants/administration/edit_library_user.html', {
        'library': library,
        'user_form': user_form,
        'user_library_form': user_library_form,
        'user_roles_from': user_roles_from
    })


@login_required
@transaction.atomic()
@permission_required_or_403('participants.delete_userlibrary')
@decorators.must_be_org_user
def delete_library_user(request, id, managed_libraries=[]):
    user_library = get_object_or_404(models.UserLibrary, id=id)
    managed_libray_ids = [managed_library.id for managed_library in managed_libraries]

    if managed_libray_ids and user_library.library_id not in managed_libray_ids:
        return HttpResponseForbidden(u'Вы не можете обслуживать эту организацию')

    user_library.user.delete()
    user_library.delete()
    return redirect('participants:administration:detail', id=user_library.library_id)


@login_required
@transaction.atomic()
@decorators.must_be_org_user
def find_library_by_district(request, managed_libraries=[]):
    if not request.user.has_module_perms('participants'):
        return HttpResponseForbidden()

    district_id = request.GET.get('district_id', None)
    parent_id = request.GET.get('parent_id', None)

    if district_id:
        district = get_object_or_404(models.District, id=district_id)
        q = Q(district_id=district_id, parent=parent_id)
    else:
        q = Q(parent=parent_id)

    libraries = models.Library.objects.values('id', 'name').filter(q)
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
            lib_ids.append(managed_library.id)
        q = q = Q(id__in=lib_ids)

    if district_id:
        district = get_object_or_404(models.District, id=district_id)
        q = q & Q(district=district)

    libraries = models.Library.objects.filter(q)
    nodes = []
    for lib in libraries:
        children = []
        # if not lib.is_leaf_node():
        #     children = _get_children(lib)
        nodes.append({
            'id': lib.id,
            'name': lib.name,
            # 'children': children
        })

    return HttpResponse(json.dumps(nodes, ensure_ascii=False), content_type='application/json')


@login_required
@transaction.atomic()
@decorators.must_be_org_user
def managed_districts(request, managed_libraries=[]):
    districts_id = []
    for managed_library in managed_libraries:
        districts_id.append(managed_library.district_id)
    q = Q()
    if districts_id:
        q = Q(id__in=districts_id)
    districts = serializers.serialize("json", models.District.objects.filter(q))
    return HttpResponse(districts, content_type='application/json')


@login_required
@transaction.atomic()
@decorators.must_be_org_user
def library_wifi_list(request, managed_libraries=[]):
    districts = []
    for managed_library in managed_libraries:
        districts.append(managed_library.district_id)
    districts_form = forms.get_district_form(districts)(request.GET, prefix='sdf')

    select_libraries_qs = _get_user_manager_orgs_qs(managed_libraries)

    select_library_form = forms.get_add_user_library_form(select_libraries_qs)(request.GET, prefix='slf')

    wifi_attr_form = forms.WiFiPointAttrForm(request.GET, prefix='waf')

    q = Q()

    if districts:
        q &= Q(library__in=select_libraries_qs)

    if districts_form.is_valid():
        district = districts_form.cleaned_data['district']
        if district:
            q &= Q(library__district=district)

    if select_library_form.is_valid():
        q &= Q(library=select_library_form.cleaned_data['library'])

    if wifi_attr_form.is_valid():
        if wifi_attr_form.cleaned_data['mac']:
            q &= Q(mac__icontains=wifi_attr_form.cleaned_data['mac'])
        if wifi_attr_form.cleaned_data['comments']:
            comment_parts = wifi_attr_form.cleaned_data['comments'].split(' ')
            q_comments = Q()
            for comment_part in comment_parts:
                q_comments &= Q(comments__icontains=comment_part)
            q &= q_comments
        if wifi_attr_form.cleaned_data['status']:
            q &= Q(status=wifi_attr_form.cleaned_data['status'])

    library_wifi_page = get_page(
        request,
        models.WiFiPoint.objects.select_related('library', 'library__district').filter(q),
        20
    )

    total_wifi = models.WiFiPoint.objects.all().count()
    total_enabled_wifi = models.WiFiPoint.objects.filter(status='enabled').count()
    total_disabled_wifi = models.WiFiPoint.objects.filter(status='disabled').count()

    return render(request, 'participants/administration/library_wifi_list.html', {
        'select_library_form': select_library_form,
        'districts_form': districts_form,
        'wifi_attr_form': wifi_attr_form,
        'library_wifi_page': library_wifi_page,
        'total_wifi': total_wifi,
        'total_enabled_wifi': total_enabled_wifi,
        'total_disabled_wifi': total_disabled_wifi,
    })


@login_required
@transaction.atomic()
@permission_required_or_403('participants.add_wifipoint')
@decorators.must_be_org_user
def add_library_wifi(request, library_id, managed_libraries=[]):
    managed_libray_ids = [unicode(managed_library.id) for managed_library in managed_libraries]

    if managed_libray_ids and library_id not in managed_libray_ids:
        return HttpResponseForbidden(u'Вы не можете обслуживать эту организацию')
    library = get_object_or_404(models.Library, id=library_id)

    if request.method == 'POST':
        form = forms.WiFiPointForm(request.POST)
        if form.is_valid():
            wifi_point = form.save(commit=False)
            wifi_point.library = library
            wifi_point.save()
            return redirect('participants:administration:detail', id=library.id)
    else:
        form = forms.WiFiPointForm()
    return render(request, 'participants/administration/wifi_form.html', {
        'form': form,
        'org': library,
    })


@login_required
@transaction.atomic()
@permission_required_or_403('participants.change_wifipoint')
@decorators.must_be_org_user
def edit_library_wifi(request, library_id, id, managed_libraries=[]):
    managed_libray_ids = [unicode(managed_library.id) for managed_library in managed_libraries]
    if managed_libray_ids and library_id not in managed_libray_ids:
        return HttpResponseForbidden(u'Вы не можете обслуживать эту организацию')
    library = get_object_or_404(models.Library, id=library_id)
    wifi_point = get_object_or_404(models.WiFiPoint, id=id, library_id=library_id)
    if request.method == 'POST':
        form = forms.WiFiPointForm(request.POST, instance=wifi_point)
        if form.is_valid():
            wifi_point = form.save(commit=False)
            wifi_point.library = library
            wifi_point.save()
            return redirect('participants:administration:detail', id=library.id)
    else:
        form = forms.WiFiPointForm(instance=wifi_point)
    return render(request, 'participants/administration/wifi_form.html', {
        'form': form,
        'edit': True,
        'org': library,
    })


@login_required
@transaction.atomic()
@permission_required_or_403('participants.delete_wifipoint')
@decorators.must_be_org_user
def delete_library_wifi(request, library_id, id, managed_libraries=[]):
    managed_libray_ids = [unicode(managed_library.id) for managed_library in managed_libraries]
    if managed_libray_ids and library_id not in managed_libray_ids:
        return HttpResponseForbidden(u'Вы не можете обслуживать эту организацию')
    library = get_object_or_404(models.Library, id=library_id)
    wifi_point = get_object_or_404(models.WiFiPoint, id=id, library_id=library_id)
    wifi_point.delete()
    return redirect('participants:administration:detail', id=library.id)


@login_required
@transaction.atomic()
@decorators.must_be_org_user
def library_int_conn_list(request, managed_libraries=[]):
    districts = []
    for managed_library in managed_libraries:
        districts.append(managed_library.district_id)
    districts_form = forms.get_district_form(districts)(request.GET, prefix='sdf')

    select_libraries_qs = _get_user_manager_orgs_qs(managed_libraries)

    select_library_form = forms.get_add_user_library_form(select_libraries_qs)(request.GET, prefix='slf')

    int_conn_attr_form = forms.InternetConnectionAttrForm(request.GET, prefix='icaf')

    q = Q()

    if districts:
        q &= Q(library__in=select_libraries_qs)

    if districts_form.is_valid():
        district = districts_form.cleaned_data['district']
        if district:
            q &= Q(library__district=district)

    if select_library_form.is_valid():
        q &= Q(library=select_library_form.cleaned_data['library'])

    if int_conn_attr_form.is_valid():
        if int_conn_attr_form.cleaned_data['is_exist']:
            q &= Q(is_exist=int_conn_attr_form.cleaned_data['is_exist'])

        if int_conn_attr_form.cleaned_data['connection_type']:
            q &= Q(is_exist=int_conn_attr_form.cleaned_data['connection_type'])

        if int_conn_attr_form.cleaned_data['incoming_speed']:
            incoming_speed_parts = int_conn_attr_form.cleaned_data['incoming_speed'].split('-')
            if len(incoming_speed_parts) == 1:
                q &= Q(incoming_speed=int(incoming_speed_parts[0]))
            if len(incoming_speed_parts) == 2:
                q &= Q(incoming_speed__gte=int(incoming_speed_parts[0]),
                       incoming_speed__lte=int(incoming_speed_parts[1]))

        if int_conn_attr_form.cleaned_data['outbound_speed']:
            outbound_speed_parts = int_conn_attr_form.cleaned_data['outbound_speed'].split('-')
            if len(outbound_speed_parts) == 1:
                q &= Q(outbound_speed=int(outbound_speed_parts[0]))
            if len(outbound_speed_parts) == 2:
                q &= Q(outbound_speed__gte=int(outbound_speed_parts[0]),
                       outbound_speed__lte=int(outbound_speed_parts[1]))

    library_int_conn_page = get_page(
        request,
        models.InternetConnection.objects.select_related('library', 'library__district').filter(q),
        20
    )

    return render(request, 'participants/administration/library_int_conn_list.html', {
        'select_library_form': select_library_form,
        'districts_form': districts_form,
        'int_conn_attr_form': int_conn_attr_form,
        'library_int_conn_page': library_int_conn_page
    })


@login_required
@transaction.atomic()
@permission_required_or_403('participants.add_internetconnection')
@decorators.must_be_org_user
def add_library_int_conn(request, library_id, managed_libraries=[]):
    managed_libray_ids = [unicode(managed_library.id) for managed_library in managed_libraries]

    if managed_libray_ids and library_id not in managed_libray_ids:
        return HttpResponseForbidden(u'Вы не можете обслуживать эту организацию')
    library = get_object_or_404(models.Library, id=library_id)

    if request.method == 'POST':
        form = forms.InternetConnectionForm(request.POST)
        if form.is_valid():
            int_conn_point = form.save(commit=False)
            int_conn_point.library = library
            int_conn_point.save()
            return redirect('participants:administration:detail', id=library.id)
    else:
        form = forms.InternetConnectionForm()
    return render(request, 'participants/administration/int_conn_form.html', {
        'form': form,
        'org': library,
    })


@login_required
@transaction.atomic()
@permission_required_or_403('participants.change_internetconnection')
@decorators.must_be_org_user
def edit_library_int_conn(request, library_id, id, managed_libraries=[]):
    managed_libray_ids = [unicode(managed_library.id) for managed_library in managed_libraries]
    if managed_libray_ids and library_id not in managed_libray_ids:
        return HttpResponseForbidden(u'Вы не можете обслуживать эту организацию')
    library = get_object_or_404(models.Library, id=library_id)
    int_conn_point = get_object_or_404(models.InternetConnection, id=id, library_id=library_id)
    if request.method == 'POST':
        form = forms.InternetConnectionForm(request.POST, instance=int_conn_point)
        if form.is_valid():
            int_conn_point = form.save(commit=False)
            int_conn_point.library = library
            int_conn_point.save()
            return redirect('participants:administration:detail', id=library.id)
    else:
        form = forms.InternetConnectionForm(instance=int_conn_point)
    return render(request, 'participants/administration/int_conn_form.html', {
        'form': form,
        'edit': True,
        'org': library,
    })


@login_required
@transaction.atomic()
@permission_required_or_403('participants.delete_internetconnection')
@decorators.must_be_org_user
def delete_library_int_conn(request, library_id, id, managed_libraries=[]):
    managed_libray_ids = [unicode(managed_library.id) for managed_library in managed_libraries]
    if managed_libray_ids and library_id not in managed_libray_ids:
        return HttpResponseForbidden(u'Вы не можете обслуживать эту организацию')
    library = get_object_or_404(models.Library, id=library_id)
    int_conn_point = get_object_or_404(models.InternetConnection, id=id, library_id=library_id)
    int_conn_point.delete()
    return redirect('participants:administration:detail', id=library.id)



@login_required
@transaction.atomic()
@permission_required_or_403('participants.add_oracleconnection')
@decorators.must_be_org_user
def add_library_ora_conn(request, library_id, managed_libraries=[]):
    managed_libray_ids = [unicode(managed_library.id) for managed_library in managed_libraries]

    if managed_libray_ids and library_id not in managed_libray_ids:
        return HttpResponseForbidden(u'Вы не можете обслуживать эту организацию')
    library = get_object_or_404(models.Library, id=library_id)

    if request.method == 'POST':
        form = forms.OracleConnectionForm(request.POST)
        if form.is_valid():
            ora_conn_point = form.save(commit=False)
            ora_conn_point.library = library
            ora_conn_point.save()
            return redirect('participants:administration:detail', id=library.id)
    else:
        form = forms.OracleConnectionForm()
    return render(request, 'participants/administration/ora_conn_form.html', {
        'form': form,
        'org': library,
    })


@login_required
@transaction.atomic()
@permission_required_or_403('participants.change_oracleconnection')
@decorators.must_be_org_user
def edit_library_ora_conn(request, library_id, id, managed_libraries=[]):
    managed_libray_ids = [unicode(managed_library.id) for managed_library in managed_libraries]
    if managed_libray_ids and library_id not in managed_libray_ids:
        return HttpResponseForbidden(u'Вы не можете обслуживать эту организацию')
    library = get_object_or_404(models.Library, id=library_id)
    ora_conn_point = get_object_or_404(models.OracleConnection, id=id, library_id=library_id)
    old_password = ora_conn_point.password
    if request.method == 'POST':
        form = forms.OracleConnectionForm(request.POST, instance=ora_conn_point)
        if form.is_valid():
            ora_conn = form.save(commit=False)
            ora_conn.library = library
            if not ora_conn.password:
                ora_conn.password = old_password
            ora_conn.save()
            return redirect('participants:administration:detail', id=library.id)
    else:
        form = forms.OracleConnectionForm(instance=ora_conn_point)
    return render(request, 'participants/administration/ora_conn_form.html', {
        'form': form,
        'edit': True,
        'org': library,
    })


@login_required
@transaction.atomic()
@permission_required_or_403('participants.delete_oracleconnection')
@decorators.must_be_org_user
def delete_library_ora_conn(request, library_id, id, managed_libraries=[]):
    managed_libray_ids = [unicode(managed_library.id) for managed_library in managed_libraries]
    if managed_libray_ids and library_id not in managed_libray_ids:
        return HttpResponseForbidden(u'Вы не можете обслуживать эту организацию')
    library = get_object_or_404(models.Library, id=library_id)
    ora_conn_point = get_object_or_404(models.OracleConnection, id=id, library_id=library_id)
    ora_conn_point.delete()
    return redirect('participants:administration:detail', id=library.id)


def send_user_create_email(user, password):
    message = u"\
Уважаемый сотрудник библиотеки! \
\nДоводим до Вашего сведения, что для работы в Государственной информационной системе \
\n\"Национальная электронная библиотека Республики Татарстан\" для вас создана учетная запись. \
\nЛогин: %s \
\nПароль: %s \
\nВход осуществляется на сайте %s" % (
        user.username, password, u'http://' + SITE_DOMAIN + u'/' + resolve_url('accounts:frontend:login')
    )

    send_mail(u'Создана учетная запись сотрудника', message, 'system@' + SITE_DOMAIN,
              [user.email], fail_silently=False)
