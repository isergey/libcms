# -*- coding: utf-8 -*-
import json
from django.conf import settings
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language

from common.pagination import get_page
from participants import decorators, org_utils
from ..models import Poll, PollContent, PollImage, PollImageContent
from forms import PollForm, PollContentForm, PollImageForm, PollImageContentForm


@login_required
@decorators.must_be_org_user
def index(request, library_code, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    if not request.user.has_module_perms('participant_photopolls'):
        return HttpResponseForbidden()
    return redirect('participant_photopolls:administration:polls_list', library_code=library_code)


@login_required
@decorators.must_be_org_user
def polls_list(request, library_code, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    if not request.user.has_module_perms('participant_photopolls'):
        return HttpResponseForbidden()
    polls_page = get_page(request, Poll.objects.filter(library=library).order_by('-create_date'), 10)

    poll_contents = list(PollContent.objects.filter(poll__in=list(polls_page.object_list), lang=get_language()[:2]))

    t_dict = {}
    for poll in polls_page.object_list:
        t_dict[poll.id] = {'poll': poll}

    for poll_content in poll_contents:
        t_dict[poll_content.poll_id]['poll'].poll_content = poll_content

    return render(request, 'participant_photopolls/administration/polls_list.html', {
        'library': library,
        'polls_list': polls_page.object_list,
        'polls_page': polls_page,
        })

@login_required
@decorators.must_be_org_user
def poll_detail(request, library_code, id, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    if not request.user.has_module_perms('participant_photopolls'):
        return HttpResponseForbidden()
    poll = get_object_or_404(Poll, id=id)
    images = PollImage.objects.filter(poll=poll)
    return render(request, 'participant_photopolls/administration/poll_detail.html', {
        'library': library,
        'poll': poll,
        'images': images
        })

@login_required
# @permission_required_or_403('participant_photopolls.add_poll')
@transaction.atomic()
@decorators.must_be_org_user
def create_poll(request, library_code, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    if request.method == 'POST':
        poll_form = PollForm(request.POST,request.FILES, prefix='poll_form')

        poll_content_forms = []
        for lang in settings.LANGUAGES:
            poll_content_forms.append({
                'form':PollContentForm(request.POST,prefix='poll_content' + lang[0]),
                'lang':lang[0]
            })
        if poll_form.is_valid():
            valid = False
            for poll_content_form in poll_content_forms:
                valid = poll_content_form['form'].is_valid()
                if not valid:
                    break

            if valid:
                poll = poll_form.save(commit=False)
                poll.library = library
                poll.save()
                for poll_content_form in poll_content_forms:
                    poll_content = poll_content_form['form'].save(commit=False)
                    poll_content.lang = poll_content_form['lang']
                    poll_content.poll = poll
                    poll_content.save()
                poll_form.save_m2m()
                return redirect('participant_photopolls:administration:polls_list', library_code=library_code)
    else:
        poll_form = PollForm(prefix="poll_form")
        poll_content_forms = []
        for lang in settings.LANGUAGES:
            poll_content_forms.append({
                'form': PollContentForm(prefix='poll_content' + lang[0]),
                'lang': lang[0]
            })

    return render(request, 'participant_photopolls/administration/create_poll.html', {
        'library': library,
        'poll_form': poll_form,
        'poll_content_forms': poll_content_forms,
    })

@login_required
# @permission_required_or_403('participant_photopolls.change_poll')
@transaction.atomic()
@decorators.must_be_org_user
def edit_poll(request, library_code, id, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    poll = get_object_or_404(Poll, id=id)
    poll_contents = PollContent.objects.filter(poll=poll)
    poll_contents_langs = {}

    for lang in settings.LANGUAGES:
        poll_contents_langs[lang] = None

    for poll_content in poll_contents:
        poll_contents_langs[poll_content.lang] = poll_content

    if request.method == 'POST':
        poll_form = PollForm(request.POST, request.FILES, prefix='poll_form', instance=poll)
        poll_content_forms = []
        if poll_form.is_valid():
            poll_form.save()
            poll_content_forms = []
            for lang in settings.LANGUAGES:
                if lang in poll_contents_langs:
                    lang = lang[0]
                    if lang in poll_contents_langs:
                        poll_content_forms.append({
                            'form':PollContentForm(request.POST,prefix='poll_content_' + lang, instance=poll_contents_langs[lang]),
                            'lang':lang
                        })
                    else:
                        poll_content_forms.append({
                            'form':PollContentForm(request.POST,prefix='poll_content_' + lang),
                            'lang':lang
                        })

            valid = False
            for poll_content_form in poll_content_forms:
                valid = poll_content_form['form'].is_valid()
                if not valid:
                    break

            if valid:
                for poll_content_form in poll_content_forms:
                    poll_content = poll_content_form['form'].save(commit=False)
                    poll_content.poll = poll
                    poll_content.lang = poll_content_form['lang']
                    poll_content.save()
                return redirect('participant_photopolls:administration:polls_list', library_code=library_code)
    else:
        poll_form = PollForm(prefix="poll_form", instance=poll)
        poll_content_forms = []
        for lang in settings.LANGUAGES:
            lang = lang[0]
            if lang in poll_contents_langs:
                poll_content_forms.append({
                    'form':PollContentForm(prefix='poll_content_' + lang, instance=poll_contents_langs[lang]),
                    'lang':lang
                })
            else:
                poll_content_forms.append({
                    'form':PollContentForm(prefix='poll_content_' + lang),
                    'lang':lang
                })

    return render(request, 'participant_photopolls/administration/edit_poll.html', {
        'poll': poll,
        'library': library,
        'poll_form': poll_form,
        'poll_content_forms': poll_content_forms,
        'content_type': 'participant_photopolls_' + str(library.id),
        'content_id': unicode(poll.id)
    })


@login_required
# @permission_required_or_403('participant_photopolls.delete_poll')
@transaction.atomic()
@decorators.must_be_org_user
def delete_poll(request, id, library_code, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    poll = get_object_or_404(Poll, id=id, library=library)
    poll.delete()
    return redirect('participant_photopolls:administration:polls_list', library_code=library_code)




@login_required
# @permission_required_or_403('participant_photopoll.add_poll')
@transaction.atomic()
@decorators.must_be_org_user
def create_poll_image(request, library_code, id, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    poll = get_object_or_404(Poll, id=id, library=library)
    if request.method == 'POST':
        poll_image_form = PollImageForm(request.POST,request.FILES, prefix='poll_image_form')

        poll_image_content_forms = []
        for lang in settings.LANGUAGES:
            poll_image_content_forms.append({
                'form':PollImageContentForm(request.POST,prefix='poll_image_content' + lang[0]),
                'lang':lang[0]
            })
        if poll_image_form.is_valid():
            valid = False
            for poll_image_content_form in poll_image_content_forms:
                valid = poll_image_content_form['form'].is_valid()
                if not valid:
                    break

            if valid:
                poll_image = poll_image_form.save(commit=False)
                poll_image.poll = poll
                poll_image.save()
                for poll_image_content_form in poll_image_content_forms:
                    poll_image_content = poll_image_content_form['form'].save(commit=False)
                    poll_image_content.lang = poll_image_content_form['lang']
                    poll_image_content.poll_image = poll_image
                    poll_image_content.save()
                poll_image_form.save_m2m()
                return redirect('participant_photopolls:administration:poll_detail', library_code=library_code, id=id)
    else:
        poll_image_form = PollImageForm(prefix="poll_image_form")
        poll_image_content_forms = []
        for lang in settings.LANGUAGES:
            poll_image_content_forms.append({
                'form': PollImageContentForm(prefix='poll_image_content' + lang[0]),
                'lang': lang[0]
            })

    return render(request, 'participant_photopolls/administration/create_poll_image.html', {
        'library': library,
        'poll': poll,
        'poll_image_form': poll_image_form,
        'poll_image_content_forms': poll_image_content_forms,
    })

@login_required
# @permission_required_or_403('participant_photopoll.change_poll')
@transaction.atomic()
@decorators.must_be_org_user
def edit_poll_image(request, library_code, id, image_id, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    poll = get_object_or_404(Poll, id=id, library=library)
    poll_image = get_object_or_404(PollImage, poll=poll, id=image_id)
    poll_image_contents = PollImageContent.objects.filter(poll_image=poll_image)
    poll_image_contents_langs = {}

    for lang in settings.LANGUAGES:
        poll_image_contents_langs[lang] = None

    for poll_image_content in poll_image_contents:
        poll_image_contents_langs[poll_image_content.lang] = poll_image_content

    if request.method == 'POST':
        poll_image_form = PollImageForm(request.POST, request.FILES, prefix='poll_image_form', instance=poll_image)
        poll_image_content_forms = []
        if poll_image_form.is_valid():
            poll_image_form.save()
            poll_image_content_forms = []
            for lang in settings.LANGUAGES:
                if lang in poll_image_contents_langs:
                    lang = lang[0]
                    if lang in poll_image_contents_langs:
                        poll_image_content_forms.append({
                            'form':PollImageContentForm(request.POST,prefix='poll_image_content_' + lang, instance=poll_image_contents_langs[lang]),
                            'lang':lang
                        })
                    else:
                        poll_image_content_forms.append({
                            'form':PollImageContentForm(request.POST,prefix='poll_image_content_' + lang),
                            'lang':lang
                        })

            valid = False
            for poll_image_content_form in poll_image_content_forms:
                valid = poll_image_content_form['form'].is_valid()
                if not valid:
                    break

            if valid:
                for poll_image_content_form in poll_image_content_forms:
                    poll_image_content = poll_image_content_form['form'].save(commit=False)
                    poll_image_content.poll_image = poll_image
                    poll_image_content.lang = poll_image_content_form['lang']
                    poll_image_content.save()
                return redirect('participant_photopolls:administration:poll_detail', library_code=library_code, id=id)
    else:
        poll_image_form = PollImageForm(prefix="poll_image_form", instance=poll_image)
        poll_image_content_forms = []
        for lang in settings.LANGUAGES:
            lang = lang[0]
            if lang in poll_image_contents_langs:
                poll_image_content_forms.append({
                    'form':PollImageContentForm(prefix='poll_image_content_' + lang, instance=poll_image_contents_langs[lang]),
                    'lang':lang
                })
            else:
                poll_image_content_forms.append({
                    'form':PollImageContentForm(prefix='poll_image_content_' + lang),
                    'lang':lang
                })

    return render(request, 'participant_photopolls/administration/edit_poll_image.html', {
        'poll_image': poll_image,
        'poll': poll,
        'library': library,
        'poll_image_form': poll_image_form,
        'poll_image_content_forms': poll_image_content_forms,
        'content_type': 'participant_photopoll_images_' + str(library.id),
        'content_id': unicode(poll_image.id)
    })


@login_required
# @permission_required_or_403('participant_photopoll.change_poll')
@transaction.atomic()
@decorators.must_be_org_user
def delete_poll_image(request, library_code, id, image_id, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    poll = get_object_or_404(Poll, id=id, library=library)
    poll_image = get_object_or_404(PollImage, poll=poll, id=image_id)
    poll_image.delete()
    return redirect('participant_photopolls:administration:poll_detail', library_code=library_code, id=id)