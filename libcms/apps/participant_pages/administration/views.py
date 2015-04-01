# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import transaction
from django.utils.translation import ugettext as _
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from guardian.decorators import permission_required_or_403
from django.http import HttpResponseForbidden
from guardian.shortcuts import remove_perm, assign, get_groups_with_perms
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import Group

from common.pagination import get_page
from core.forms import LanguageForm, get_groups_form
from participants import decorators, org_utils

from ..models import Page, Content
from forms import ContentForm, get_content_form, get_page_form

VIEW_PAGE_PERMISSION = 'view_page'
@login_required
@decorators.must_be_org_user
def index(request, library_code, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    return redirect('participant_pages:administration:pages_list', library_code=library_code)


@login_required
@permission_required_or_403('participant_pages.add_page')
@transaction.atomic()
@decorators.must_be_org_user
def pages_list(request, library_code, parent=None, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    if parent:
        parent = get_object_or_404(Page, id=parent, library=library)

    pages_page = get_page(request, Page.objects.filter(parent=parent, library=library))
    pages_page.object_list = list(pages_page.object_list)
    contents = list(Content.objects.filter(page__in=pages_page.object_list, lang=get_language()[:2]))

    pages_dict = {}
    for page in pages_page.object_list:
        pages_dict[page.id] = {'page': page}

    for content in contents:
        pages_dict[content.page_id]['page'].content = content

    # pages = [page['page'] for page in pages_dict.values()]


    return render(request, 'participant_pages/administration/pages_list.html', {
        'library': library,
        'parent': parent,
        'pages': pages_page.object_list,
        'pages_page': pages_page,
    })


@login_required
@permission_required_or_403('participant_pages.add_page')
@transaction.atomic()
@decorators.must_be_org_user
def create_page(request, library_code, parent=None, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    if parent:
        parent = get_object_or_404(Page, id=parent, library=library)

    PageForm = get_page_form(library, parent)
    if request.method == 'POST':
        page_form = PageForm(request.POST, prefix='page_form')

        if page_form.is_valid():
            page = page_form.save(commit=False)
            if parent:
                page.parent = parent

            if not request.user.has_perm('participant_pages.public_page'):
                page.public = False
            page.library = library
            page.save()
            if parent:
                # наследование прав от родителя
                copy_perms_for_groups(parent, page)
            else:
                try:
                    users_group = Group.objects.get(name='users')
                    assign_permission([users_group], [page], VIEW_PAGE_PERMISSION)
                except Group.DoesNotExist:
                    pass
            return redirect('participant_pages:administration:create_page_content', library_code=library_code,
                            page_id=page.id)
    else:
        page_form = PageForm(prefix='page_form')

    return render(request, 'participant_pages/administration/create_page.html', {
        'library': library,
        'parent': parent,
        'page_form': page_form,
    })


@login_required
@permission_required_or_403('participant_pages.change_page')
@transaction.atomic()
@decorators.must_be_org_user
def edit_page(request, library_code, id, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    langs = []
    for lang in settings.LANGUAGES:
        langs.append({
            'code': lang[0],
            'title': _(lang[1])
        })

    page = get_object_or_404(Page, id=id)
    PageForm = get_page_form(page.parent_id)
    if request.method == 'POST':
        page_form = PageForm(request.POST, prefix='page_form', instance=page)

        if page_form.is_valid():
            page = page_form.save(commit=False)
            if not request.user.has_perm('participant_pages.public_page'):
                page.public = False
            page.save()
            if page.parent_id:
                return redirect('participant_pages:administration:pages_list', library_code=library_code,
                                parent=page.parent_id)
            return redirect('participant_pages:administration:pages_list', library_code=library_code)

    else:
        page_form = PageForm(prefix='page_form', instance=page)

    return render(request, 'participant_pages/administration/edit_page.html', {
        'library': library,
        'page': page,
        'langs': langs,
        'page_form': page_form
    })


@login_required
@permission_required_or_403('participant_pages.delete_page')
@transaction.atomic()
@decorators.must_be_org_user
def delete_page(request, library_code, id, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    page = get_object_or_404(Page, id=id)
    page.delete()
    if page.parent_id:
        return redirect('participant_pages:administration:pages_list', library_code=library_code, parent=page.parent_id)
    return redirect('participant_pages:administration:pages_list', library_code=library_code)


@login_required
@permission_required_or_403('participant_pages.add_page')
@transaction.atomic()
@decorators.must_be_org_user
def create_page_content(request, library_code, page_id, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    page = get_object_or_404(Page, id=page_id)
    if request.method == 'POST':
        content_form = ContentForm(request.POST, prefix='content_form')

        if content_form.is_valid():
            content = content_form.save(commit=False)
            content.page = page
            content.save()

            save = request.POST.get('save', u'save_edit')
            if save == u'save':
                return redirect('participant_pages:administration:edit_page', library_code=library_code, id=page_id)
            else:
                return redirect('participant_pages:administration:edit_page_content', library_code=library_code,
                                page_id=page_id, lang=content.lang)
    else:
        content_form = ContentForm(prefix='content_form')
    return render(request, 'participant_pages/administration/create_page_content.html', {
        'library': library,
        'page': page,
        'content_form': content_form,
        'content_type': 'participant_pages',
        'content_id': str(library.id) + '_' + page.url_path.replace('/', '_')
    })


@login_required
@permission_required_or_403('participant_pages.change_page')
@transaction.atomic()
@decorators.must_be_org_user
def edit_page_content(request, library_code, page_id, lang, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    lang_form = LanguageForm({'lang': lang})
    if not lang_form.is_valid():
        return HttpResponse(_(u'Language is not registered in system.') + _(u" Language code: ") + lang)

    page = get_object_or_404(Page, id=page_id)

    try:
        content = Content.objects.get(page=page_id, lang=lang)
    except Content.DoesNotExist:
        content = Content(page=page, lang=lang)

    ContentForm = get_content_form(('page', 'lang'))

    if request.method == 'POST':
        content_form = ContentForm(request.POST, prefix='content_form', instance=content)

        if content_form.is_valid():
            content = content_form.save(commit=False)
            content.page = page
            content.save()

        save = request.POST.get('save', u'save_edit')
        if save == u'save':
            return redirect('participant_pages:administration:edit_page', library_code=library_code, id=page_id)

    else:
        content_form = ContentForm(prefix='content_form', instance=content)
    return render(request, 'participant_pages/administration/edit_page_content.html', {
        'library': library,
        'page': page,
        'content': content,
        'content_form': content_form,
        'content_type': 'participant_pages',
        'content_id': str(library.id) + '_' + page.url_path.replace('/', '_')
    })


@permission_required_or_403('participant_pages.change_page')
@transaction.atomic()
@decorators.must_be_org_user
def page_permissions(request, library_code, id, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    obj = get_object_or_404(Page, id=id)

    GroupsForm = get_groups_form(Group.objects.all(), initial=list(get_groups_with_perms(obj)))
    groups_form = GroupsForm()

    return render(request, 'participant_pages/administration/permissions.html', {
        'library': library,
        'page': obj,
        'groups_form': groups_form,
    })


@login_required
@transaction.atomic()
@decorators.must_be_org_user
def assign_page_permissions(request, library_code, id, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    obj = get_object_or_404(Page, id=id)

    if request.method == 'POST':
        GroupsForm = get_groups_form(Group.objects.all())
        groups_form = GroupsForm(request.POST)
        if groups_form.is_valid():
            assign_permission(groups_form.cleaned_data['groups'], [obj], VIEW_PAGE_PERMISSION)
            assign_permission(groups_form.cleaned_data['groups'], obj.get_descendants(), VIEW_PAGE_PERMISSION)
    return HttpResponse(u'{"status":"ok"}')


def assign_permission(new_groups, objects, perm):
    groups = Group.objects.all()
    for obj in objects:
        for group in groups:
            remove_perm(perm, group, obj)
        for new_group in new_groups:
            assign(perm, new_group, obj)


def copy_perms_for_groups(obj, new_obj):
    group_and_perms = get_groups_with_perms(obj, True)
    for gp in group_and_perms:
        for perm in group_and_perms[gp]:
            assign(perm, gp, new_obj)


@permission_required_or_403('participant_pages.change_page')
@transaction.atomic()
@decorators.must_be_org_user
def page_up(request, library_code, id, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    page = get_object_or_404(Page, id=id)
    page.up()
    if page.parent_id:
        return redirect('participant_pages:administration:pages_list', library_code=library_code, parent=page.parent_id)
    else:
        return redirect('participant_pages:administration:pages_list', library_code=library_code)


@permission_required_or_403('participant_pages.change_page')
@transaction.atomic()
@decorators.must_be_org_user
def page_down(request, library_code, id, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    page = get_object_or_404(Page, id=id)
    page.down()
    if page.parent_id:
        return redirect('participant_pages:administration:pages_list', library_code=library_code, parent=page.parent_id)
    else:
        return redirect('participant_pages:administration:pages_list', library_code=library_code)


@permission_required_or_403('participant_pages.change_page')
@transaction.atomic()
@decorators.must_be_org_user
def page_to_first(request, library_code, id, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    page = get_object_or_404(Page, id=id)
    page.to_first_child()
    if page.parent_id:
        return redirect('participant_pages:administration:pages_list', library_code=library_code, parent=page.parent_id)
    else:
        return redirect('participant_pages:administration:pages_list', library_code=library_code)


@permission_required_or_403('participant_pages.change_page')
@transaction.atomic()
@decorators.must_be_org_user
def page_to_last(request, library_code, id, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    page = get_object_or_404(Page, id=id)
    page.to_last_child()
    if page.parent_id:
        return redirect('participant_pages:administration:pages_list', library_code=library_code, parent=page.parent_id)
    else:
        return redirect('participant_pages:administration:pages_list', library_code=library_code, )