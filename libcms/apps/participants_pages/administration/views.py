# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext as _
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required
from common.pagination import get_page
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.utils.translation import to_locale, get_language

from core.forms import LanguageForm
from participants_pages.models import Page, Content
from forms import PageForm, ContentForm, get_content_form
from participants.models import Library

#@permission_required_or_403('accounts.view_users')
def index(request, library_id):
    return redirect('participants_pages:administration:pages_list', library_id=library_id)


@login_required
@permission_required_or_403('participants_pages.add_page')
def pages_list(request, library_id, parent=None):
    library = get_object_or_404(Library, id=library_id)
    if parent:
        parent = get_object_or_404(Page, id=parent)

    pages_page = get_page(request, Page.objects.filter(parent=parent))
    contents = list(Content.objects.filter(page__in=list(pages_page.object_list), lang=get_language()[:2]))

    pages_dict = {}
    for page in pages_page.object_list:
        pages_dict[page.id] = {'page':page}

    for content in contents:
        pages_dict[content.page_id]['page'].content = content

    pages = [page['page'] for page in pages_dict.values()]


    return render(request, 'participants_pages/administration/pages_list.html', {
        'parent': parent,
        'pages': pages,
        'pages_page': pages_page,
        'library': library
    })

@login_required
@permission_required_or_403('participants_pages.add_page')
def create_page(request, library_id, parent=None):
    library = get_object_or_404(Library, id=library_id)
    if parent:
        parent = get_object_or_404(Page, id=parent)

    if request.method == 'POST':
        page_form = PageForm(request.POST, prefix='page_form')
        if page_form.is_valid():
            page = page_form.save(commit=False)
            if parent:
                page.parent = parent

            if not request.user.has_perm('pages.public_page'):
                page.public = False
            page.library = library
            page.save()
            return redirect('participants_pages:administration:create_page_content', page_id=page.id, library_id=library_id)
    else:
        page_form = PageForm(prefix='page_form')

    return render(request, 'participants_pages/administration/create_page.html', {
        'parent': parent,
        'page_form': page_form,
        'library': library
     })

@login_required
@permission_required_or_403('participants_pages.change_page')
def edit_page(request, library_id, id):
    library = get_object_or_404(Library, id=library_id)
    langs = []
    for lang in settings.LANGUAGES:
        langs.append({
            'code': lang[0],
            'title': _(lang[1])
        })

    page = get_object_or_404(Page, id=id)

    if request.method == 'POST':
        page_form = PageForm(request.POST, prefix='page_form', instance=page)

        if page_form.is_valid():
            page = page_form.save(commit=False)
            if not request.user.has_perm('participants_pages.public_page'):
                page.public = False
            page.save()
            return redirect('participants_pages:administration:pages_list', library_id=library_id)

    else:
        page_form = PageForm(prefix='page_form', instance=page)

    return render(request, 'participants_pages/administration/edit_page.html', {
        'page': page,
        'langs': langs,
        'page_form': page_form,
        'library': library
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
@permission_required_or_403('participants_pages.delete_page')
def delete_page(request, library_id, id):
#    library = get_object_or_404(Library, id=library_id)
    page = get_object_or_404(Page, id=id)
    page.delete()
    return redirect('participants_pages:administration:pages_list', library_id=library_id)

@login_required
@permission_required_or_403('participants_pages.add_page')
def create_page_content(request, library_id, page_id):
    library = get_object_or_404(Library, id=library_id)
    page = get_object_or_404(Page, id=page_id)
    if request.method == 'POST':
        content_form = ContentForm(request.POST, prefix='content_form')

        if content_form.is_valid():
            content = content_form.save(commit=False)
            content.page = page
            content.save()

            save = request.POST.get('save', u'save_edit')
            if save == u'save':
                return redirect('participants_pages:administration:edit_page', id=page_id, library_id=library_id)
            else:
                return redirect('participants_pages:administration:edit_page_content', page_id=page_id, lang=content.lang)
    else:
        content_form = ContentForm(prefix='content_form')
    return render(request, 'participants_pages/administration/create_page_content.html', {
        'page': page,
        'content_form': content_form,
        'library': library
    })

@login_required
@permission_required_or_403('participants_pages.change_page')
def edit_page_content(request, library_id,  page_id, lang):
    library = get_object_or_404(Library, id=library_id)
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
            return redirect('participants_pages:administration:edit_page', id=page_id, library_id=library_id)

    else:
        content_form = ContentForm(prefix='content_form', instance=content)
    return render(request, 'participants_pages/administration/edit_page_content.html', {
        'page': page,
        'content': content,
        'content_form': content_form,
        'library': library

    })






