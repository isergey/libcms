# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language

from common.pagination import get_page
from participant_site import decorators
from ..models import Event, EventContent
from forms import EventForm, EventContentForm


@login_required
@permission_required_or_403('participant_events.add_event')
@decorators.must_be_manager
def index(request, library_code, library):
    if not request.user.has_module_perms('participant_events'):
        return HttpResponseForbidden()
    return redirect('participant_events:administration:events_list', library_code=library_code)


@login_required
@decorators.must_be_manager
def events_list(request, library_code, library):
    if not request.user.has_module_perms('participant_events'):
        return HttpResponseForbidden()
    events_page = get_page(request, Event.objects.filter(library=library).order_by('-create_date'), 10)

    event_contents = list(EventContent.objects.filter(event__in=list(events_page.object_list), lang=get_language()[:2]))

    t_dict = {}
    for event in events_page.object_list:
        t_dict[event.id] = {'event': event}

    for event_content in event_contents:
        t_dict[event_content.event_id]['event'].event_content = event_content

    return render(request, 'participant_events/administration/events_list.html', {
        'library': library,
        'events_list': events_page.object_list,
        'events_page': events_page,
        })



@login_required
@permission_required_or_403('events.add_event')
@transaction.atomic()
@decorators.must_be_manager
def create_event(request, library_code, library):
    if request.method == 'POST':
        event_form = EventForm(request.POST,request.FILES, prefix='event_form')

        event_content_forms = []
        for lang in settings.LANGUAGES:
            event_content_forms.append({
                'form':EventContentForm(request.POST,prefix='event_content' + lang[0]),
                'lang':lang[0]
            })
        if event_form.is_valid():
            valid = False
            for event_content_form in event_content_forms:
                valid = event_content_form['form'].is_valid()
                print valid
                if not valid:
                    break

            if valid:
                event = event_form.save(commit=False)
                event.library = library
                event.save()
                for event_content_form in event_content_forms:
                    event_content = event_content_form['form'].save(commit=False)
                    event_content.lang = event_content_form['lang']
                    event_content.event = event
                    event_content.save()
                event_form.save_m2m()
                return redirect('participant_events:administration:events_list', library_code=library_code)
    else:
        event_form = EventForm(prefix="event_form")
        event_content_forms = []
        for lang in settings.LANGUAGES:
            event_content_forms.append({
                'form': EventContentForm(prefix='event_content' + lang[0]),
                'lang': lang[0]
            })

    return render(request, 'participant_events/administration/create_event.html', {
        'library': library,
        'event_form': event_form,
        'event_content_forms': event_content_forms,
    })

@login_required
@permission_required_or_403('participant_events.change_event')
@transaction.atomic()
@decorators.must_be_manager
def edit_event(request, id, library_code, library):
    event = get_object_or_404(Event, id=id)
    event_contents = EventContent.objects.filter(event=event)
    event_contents_langs = {}

    for lang in settings.LANGUAGES:
        event_contents_langs[lang] = None

    for event_content in event_contents:
        event_contents_langs[event_content.lang] = event_content

    if request.method == 'POST':
        event_form = EventForm(request.POST, request.FILES, prefix='event_form', instance=event)
        event_content_forms = []
        if event_form.is_valid():
            event_form.save()
            event_content_forms = []
            for lang in settings.LANGUAGES:
                if lang in event_contents_langs:
                    lang = lang[0]
                    if lang in event_contents_langs:
                        event_content_forms.append({
                            'form':EventContentForm(request.POST,prefix='event_content_' + lang, instance=event_contents_langs[lang]),
                            'lang':lang
                        })
                    else:
                        event_content_forms.append({
                            'form':EventContentForm(request.POST,prefix='event_content_' + lang),
                            'lang':lang
                        })

            valid = False
            for event_content_form in event_content_forms:
                valid = event_content_form['form'].is_valid()
                if not valid:
                    break

            if valid:
                for event_content_form in event_content_forms:
                    event_content = event_content_form['form'].save(commit=False)
                    event_content.event = event
                    event_content.lang = event_content_form['lang']
                    event_content.save()
                return redirect('participant_events:administration:events_list', library_code=library_code)
    else:
        event_form = EventForm(prefix="event_form", instance=event)
        event_content_forms = []
        for lang in settings.LANGUAGES:
            lang = lang[0]
            if lang in event_contents_langs:
                event_content_forms.append({
                    'form':EventContentForm(prefix='event_content_' + lang, instance=event_contents_langs[lang]),
                    'lang':lang
                })
            else:
                event_content_forms.append({
                    'form':EventContentForm(prefix='event_content_' + lang),
                    'lang':lang
                })

    return render(request, 'participant_events/administration/edit_event.html', {
        'event': event,
        'library': library,
        'event_form': event_form,
        'event_content_forms': event_content_forms,
        'content_type': 'participant_events_' + str(library.id),
        'content_id': unicode(event.id)
    })


@login_required
@permission_required_or_403('participant_events.delete_event')
@transaction.atomic()
@decorators.must_be_manager
def delete_event(request, id, library_code, library):
    event = get_object_or_404(Event, id=id)
    event.delete()
    return redirect('participant_events:administration:events_list', library_code=library_code)


