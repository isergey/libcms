# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import transaction
from django.utils.translation import ugettext as _
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from guardian.decorators import permission_required_or_403
from guardian.models import GroupObjectPermission

from guardian.forms import GroupObjectPermissionsForm
from guardian.shortcuts import get_perms_for_model, get_perms, remove_perm, assign, get_groups_with_perms
from django.contrib.auth.decorators import login_required
from common.pagination import get_page
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.utils.translation import to_locale, get_language
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from core.forms import LanguageForm, get_permissions_form, get_groups_form
from pages.models import Page, Content
from forms import ContentForm, get_content_form, get_page_form

#@permission_required_or_403('accounts.view_users')
def index(request):
    return redirect('pages:administration:pages_list')
    #return render(request, 'pages/administration/index.html')

@login_required
@permission_required_or_403('pages.add_page')
def pages_list(request, parent=None):
    if parent:
        parent = get_object_or_404(Page, id=parent)

    pages_page = get_page(request, Page.objects.filter(parent=parent))
    pages_page.object_list = list(pages_page.object_list)
    contents = list(Content.objects.filter(page__in=pages_page.object_list, lang=get_language()[:2]))

    pages_dict = {}
    for page in pages_page.object_list:
        pages_dict[page.id] = {'page':page}

    for content in contents:
        pages_dict[content.page_id]['page'].content = content

#    pages = [page['page'] for page in pages_dict.values()]


    return render(request, 'pages/administration/pages_list.html', {
        'parent': parent,
        'pages': pages_page.object_list,
        'pages_page': pages_page,
    })

@login_required
@permission_required_or_403('pages.add_page')
def create_page(request, parent=None):
    if parent:
        parent = get_object_or_404(Page, id=parent)

    PageForm = get_page_form(parent)
    if request.method == 'POST':
        page_form = PageForm(request.POST, prefix='page_form')

        if page_form.is_valid():
            page = page_form.save(commit=False)
            if parent:
                page.parent = parent

            if not request.user.has_perm('pages.public_page'):
                page.public = False

            page.save()
            if parent:
                # наследование прав от родителя
                copy_perms_for_groups(parent, page)

            return redirect('pages:administration:create_page_content', page_id=page.id)
    else:
        page_form = PageForm(prefix='page_form')

    return render(request, 'pages/administration/create_page.html', {
        'parent': parent,
        'page_form': page_form,
     })

@login_required
@permission_required_or_403('pages.change_page')
def edit_page(request, id):
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
            if not request.user.has_perm('pages.public_page'):
                page.public = False
            page.save()
            return redirect('pages:administration:pages_list')

    else:
        page_form = PageForm(prefix='page_form', instance=page)

    return render(request, 'pages/administration/edit_page.html', {
        'page': page,
        'langs': langs,
        'page_form': page_form,
    })

#@login_required
#@permission_required_or_403('pages.public_page')
#def toggle_page_public(request, id):
#    page = get_object_or_404(Page, id=id)
#    if page.public:
#        page.public = False
#    else:
#        page.public = True
#    page.save()
#    return redirect('pages:administration:pages_list')

@login_required
@permission_required_or_403('pages.delete_page')
def delete_page(request, id):
    page = get_object_or_404(Page, id=id)
    page.delete()
    return redirect('pages:administration:pages_list')

@login_required
@permission_required_or_403('pages.add_page')
def create_page_content(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    if request.method == 'POST':
        content_form = ContentForm(request.POST, prefix='content_form')

        if content_form.is_valid():
            content = content_form.save(commit=False)
            content.page = page
            content.save()

            save = request.POST.get('save', u'save_edit')
            if save == u'save':
                return redirect('pages:administration:edit_page', id=page_id)
            else:
                return redirect('pages:administration:edit_page_content', page_id=page_id, lang=content.lang)
    else:
        content_form = ContentForm(prefix='content_form')
    return render(request, 'pages/administration/create_page_content.html', {
        'page': page,
        'content_form': content_form,
    })

@login_required
@permission_required_or_403('pages.change_page')
def edit_page_content(request, page_id, lang):
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
            return redirect('pages:administration:edit_page', id=page_id)

    else:
        content_form = ContentForm(prefix='content_form', instance=content)
    return render(request, 'pages/administration/edit_page_content.html', {
        'page': page,
        'content': content,
        'content_form': content_form,
    })

from guardian.core import ObjectPermissionChecker
@permission_required_or_403('pages.change_page')
def page_permissions(request, id):
    obj = get_object_or_404(Page, id=id)

    GroupsForm = get_groups_form(Group.objects.all(), initial=list(get_groups_with_perms(obj)))
    groups_form = GroupsForm()


    return render(request, 'pages/administration/permissions.html', {
        'page': obj,
        'groups_form': groups_form,
    })



@login_required
@transaction.commit_on_success
def assign_page_permissions(request, id):
    obj = get_object_or_404(Page, id=id)
    perm = 'view_page'


    if request.method == 'POST':
        GroupsForm = get_groups_form(Group.objects.all())
        groups_form = GroupsForm(request.POST)
        if groups_form.is_valid():
            assign_permission(groups_form.cleaned_data['groups'], [obj], perm)
            assign_permission(groups_form.cleaned_data['groups'], obj.get_descendants(), perm)
    return HttpResponse(u'{"status":"ok"}')


def assign_permission(new_groups, objects, perm):
    groups = Group.objects.all()
    for obj in objects:
        for group in groups:
            remove_perm(perm, group, obj)
        for new_group in new_groups:
            assign(perm, new_group, obj)


def copy_perms_for_groups(obj, new_obj):
    group_and_perms =  get_groups_with_perms(obj, True)
    for gp in group_and_perms:
        for perm in group_and_perms[gp]:
            assign(perm, gp, new_obj)



def page_up(request, id):
    page = get_object_or_404(Page, id=id)
    page.up()
    if page.parent_id:
        return redirect('pages:administration:pages_list', parent=page.parent_id)
    else:
        return redirect('pages:administration:pages_list')


def page_down(request, id):
    page = get_object_or_404(Page, id=id)
    page.down()
    if page.parent_id:
        return redirect('pages:administration:pages_list', parent=page.parent_id)
    else:
        return redirect('pages:administration:pages_list')