# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import transaction
from django.utils.translation import ugettext as _
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required
from common.pagination import get_page
from django.utils.translation import to_locale, get_language

from core.forms import LanguageForm
from events.models import Event, EventContent
from forms import EventForm, EventContentForm

@login_required
@permission_required_or_403('events.add_event')
def index(request):
    if not request.user.has_module_perms('events'):
        return HttpResponseForbidden()
    return redirect('events:administration:events_list')


@login_required
@permission_required_or_403('events.add_event')
def events_list(request):
    events_page = get_page(request, Event.objects.all().order_by('-create_date'))
    event_contents = list(EventContent.objects.filter(event__in=list(events_page.object_list), lang=get_language()[:2]))

    t_dict = {}
    for event in events_page.object_list:
        t_dict[event.id] = {'event': event}

    for event_content in event_contents:
        t_dict[event_content.event_id]['event'].event_content = event_content

    return render(request, 'events/administration/events_list.html', {
        'events_list': events_page.object_list,
        'events_page': events_page,
        })



@login_required
@permission_required_or_403('events.add_event')
@transaction.commit_on_success
def create_event(request):

    if request.method == 'POST':
        event_form = EventForm(request.POST,prefix='event_form')

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
                event.save()
                for event_content_form in event_content_forms:
                    event_content = event_content_form['form'].save(commit=False)
                    event_content.lang = event_content_form['lang']
                    event_content.event = event
                    event_content.save()
                return redirect('events:administration:events_list')
    else:
        event_form = EventForm(prefix="event_form")
        event_content_forms = []
        for lang in settings.LANGUAGES:
            event_content_forms.append({
                'form':EventContentForm(prefix='event_content' + lang[0]),
                'lang':lang[0]
            })

    return render(request, 'events/administration/create_event.html', {
        'event_form': event_form,
        'event_content_forms': event_content_forms,
    })

@login_required
@permission_required_or_403('events.change_event')
@transaction.commit_on_success
def edit_event(request, id):
    event = get_object_or_404(Event, id=id)
    event_contents = EventContent.objects.filter(event=event)
    event_contents_langs = {}

    for lang in settings.LANGUAGES:
        event_contents_langs[lang] = None

    for event_content in event_contents:
        event_contents_langs[event_content.lang] = event_content

    if request.method == 'POST':
        event_form = EventForm(request.POST,prefix='event_form', instance=event)

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

                return redirect('events:administration:events_list')
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

    return render(request, 'events/administration/edit_event.html', {
        'event_form': event_form,
        'event_content_forms': event_content_forms,
        })


@login_required
@permission_required_or_403('events.delete_event')
@transaction.commit_on_success
def delete_event(request, id):
    event = get_object_or_404(Event, id=id)
    event.delete()
    return redirect('events:administration:events_list')




