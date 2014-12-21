# -*- coding: utf-8 -*-
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import translation
from django.utils.translation import get_language
from common.pagination import get_page
from django.db.models import Q
from participant_events.models import Event, EventContent
import forms


def index(request, day='', month='', year=''):
    filter_form = forms.EventsFilterForm(request.GET, prefix='filter')
    q = Q(active=True)

    if filter_form.is_valid():
        library = filter_form.cleaned_data['library']
        event_type = filter_form.cleaned_data['event_type']
        age_category = filter_form.cleaned_data['age_category']

        if library:
            q = q & Q(library=library)

        if event_type:
            q_type = Q(event_type='')
            for item in event_type:
                q = q & Q(event_type__in=event_type)

        if age_category:
            q = q & Q(age_category__in=age_category)
    date_filtered = None
    if year and month and day:
        q = q & Q(start_date__year=year, start_date__month=month, start_date__day=day)
        date_filtered = datetime(year=int(year), month=int(month), day=int(day))
    #print unicode(q)
    events_page = get_page(
        request, Event.objects.select_related('library').prefetch_related('age_category', 'event_type').filter(q).distinct()
    )
    events = list(events_page.object_list)
    event_contents = list(
        EventContent.objects.filter(
            event__in=events,
            lang=get_language()[:2]
        ))

    t_dict = {}
    for event in events:
        t_dict[event.id] = {'event': event}

    for event_content in event_contents:
        t_dict[event_content.event_id]['event'].event_content = event_content

    return render(request, 'events/frontend/list.html', {
        'events_list': events,
        'events_page': events_page,
        'filter_form': filter_form,
        'date_filtered': date_filtered
        })


def filer_by_date(request, day='', month='', year=''):
    events_page = get_page(request, Event.objects.filter(active=True, start_date__year=year, start_date__month=month, start_date__day=day).order_by('-create_date'))
    event_contents = list(EventContent.objects.filter(event__in=list(events_page.object_list), lang=get_language()[:2]))

    t_dict = {}
    for event in events_page.object_list:
        t_dict[event.id] = {'event': event}

    for event_content in event_contents:
        t_dict[event_content.event_id]['event'].event_content = event_content
    return render(request, 'events/frontend/list.html', {
        'events_list': events_page.object_list,
        'events_page': events_page,

        })

def show(request, id):
    cur_language = translation.get_language()
    event = get_object_or_404(Event, id=id)
    try:
        content = EventContent.objects.get(event=event, lang=cur_language[:2])
    except EventContent.DoesNotExist:
        content = None

    return render(request, 'events/frontend/show.html', {
        'event': event,
        'content': content
    })
