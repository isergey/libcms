# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import translation
from django.utils.translation import get_language
from common.pagination import get_page
from participants.models import Library
from .. import models
import forms

SUBSCRIBE_PER_DAY_LIMIT = 1000


def index(request, library_code):
    library = get_object_or_404(Library, code=library_code)
    events_page = get_page(
        request, models.Event.objects.filter(
            active=True,
            library=library
        ).prefetch_related('age_category', 'event_type').order_by('start_date')
    )

    event_contents = list(
        models.EventContent.objects.filter(
            event__in=list(events_page.object_list),
            lang=get_language()[:2]
        ))

    t_dict = {}
    for event in events_page.object_list:
        t_dict[event.id] = {'event': event}

    for event_content in event_contents:
        t_dict[event_content.event_id]['event'].event_content = event_content

    return render(request, 'participant_events/frontend/list.html', {
        'library': library,
        'events_list': events_page.object_list,
        'events_page': events_page,
    })


def show(request, library_code, id):
    library = get_object_or_404(Library, code=library_code)
    cur_language = translation.get_language()
    event = get_object_or_404(models.Event, id=id, library=library)
    difference = event.end_date - event.start_date
    period = (difference.days, difference.seconds // 3600, (difference.seconds // 60) % 60)
    try:
        content = models.EventContent.objects.get(event=event, lang=cur_language[:2])
    except models.EventContent.DoesNotExist:
        content = None
    notification_form = forms.NotificationForm(initial={
        'email': getattr(request.user, 'email', u'')
    })

    return render(request, 'participant_events/frontend/show.html', {
        'period': period,
        'library': library,
        'event': event,
        'content': content,
        'notification_form': notification_form
    })


@transaction.atomic()
def create_notification(request, library_code, id):
    now = datetime.now()
    today_count = models.EventSubscribe.objects.filter(
        create_date__year=now.year,
        create_date__month=now.month,
        create_date__day=now.day
    ).count()

    if today_count > SUBSCRIBE_PER_DAY_LIMIT:
        return HttpResponse(u'Превышен дневной лимит заявок на напоминания')

    library = get_object_or_404(Library, code=library_code)
    cur_language = translation.get_language()
    event = get_object_or_404(models.Event, id=id, library=library)

    try:
        content = models.EventContent.objects.get(event=event, lang=cur_language[:2])
    except models.EventContent.DoesNotExist:
        content = {}

    if request.method == 'POST':
        notification_form = forms.NotificationForm(request.POST)
        if notification_form.is_valid():
            notification = notification_form.save(commit=False)
            event_count = models.EventNotification.objects.filter(
                email=notification.email,
                items_count=notification.items_count,
                time_item=notification.time_item,
                event=event
            ).count()

            if not event_count:
                notification.event = event
                notification.make_notification_time()
                notification.save()

            return redirect('participant_events:frontend:create_notification_complete', library_code=library_code,
                            id=id)
    else:
        notification_form = forms.NotificationForm(initial={
            'email': getattr(request.user, 'email', u'')
        })

    return render(request, 'participant_events/frontend/create_notification.html', {
        'library': library,
        'event': event,
        'content': content,
        'notification_form': notification_form
    })


def create_notification_complate(request, library_code, id):
    library = get_object_or_404(Library, code=library_code)
    cur_language = translation.get_language()
    event = get_object_or_404(models.Event, id=id, library=library)
    try:
        content = models.EventContent.objects.get(event=event, lang=cur_language[:2])
    except models.EventContent.DoesNotExist:
        content = {}
    return render(request, 'participant_events/frontend/create_notification_complete.html', {
        'library': library,
        'event': event,
        'content': content
    })


@transaction.atomic()
def subscribe(request, library_code):
    now = datetime.now()
    today_count = models.EventSubscribe.objects.filter(
        create_date__year=now.year,
        create_date__month=now.month,
        create_date__day=now.day
    ).count()

    if today_count > SUBSCRIBE_PER_DAY_LIMIT:
        return HttpResponse(u'Превышен дневной лимит подписок')

    library = get_object_or_404(Library, code=library_code)

    if request.method == 'POST':
        form = forms.EventSubscribeForm(request.POST)
        if form.is_valid():
            subscribe = form.save(commit=False)
            try:
                exists_subscribe = models.EventSubscribe.objects.prefetch_related('age_category', 'event_type').get(
                    email=subscribe.email,
                    library=library
                )
                exist_age_categories = exists_subscribe.age_category.all()
                exist_event_types = exists_subscribe.event_type.all()

                for age_category in form.cleaned_data['age_category']:
                    if age_category not in exist_age_categories:
                        exists_subscribe.age_category.add(age_category)

                for event_type in form.cleaned_data['event_type']:
                    if event_type not in exist_event_types:
                        exists_subscribe.event_type.add(event_type)

            except models.EventSubscribe.DoesNotExist:
                subscribe.library = library
                if request.user.is_authenticated():
                    subscribe.user = request.user
                subscribe.save()
                form.save_m2m()
            return redirect('participant_events:frontend:subscribe_complate', library_code=library_code)
    else:
        form = forms.EventSubscribeForm(initial={
            'email': getattr(request.user, 'email', u'')
        })
    return render(request, 'participant_events/frontend/subscribe.html', {
        'library': library,
        'form': form
    })


def subscribe_complate(request, library_code):
    library = get_object_or_404(Library, code=library_code)
    return render(request, 'participant_events/frontend/subscribe_complate.html', {
        'library': library
    })


def filer_by_date(request, library_code, day='', month='', year=''):
    library = get_object_or_404(Library, code=library_code)

    events_page = get_page(request, models.Event.objects.filter(
        library=library,
        active=True,
        start_date__year=year,
        start_date__month=month,
        start_date__day=day
    ).prefetch_related('age_category', 'event_type').order_by('-create_date'))

    event_contents = list(
        models.EventContent.objects.filter(event__in=list(events_page.object_list), lang=get_language()[:2]))

    t_dict = {}
    for event in events_page.object_list:
        t_dict[event.id] = {'event': event}

    for event_content in event_contents:
        t_dict[event_content.event_id]['event'].event_content = event_content

    date = datetime(
        year=int(year),
        month=int(month),
        day=int(day)
    )
    return render(request, 'participant_events/frontend/list.html', {
        'library': library,
        'events_list': events_page.object_list,
        'events_page': events_page,
        'date': date
    })


def make_icalendar(request, library_code, id):
    library = get_object_or_404(Library, code=library_code)
    cur_language = translation.get_language()
    event = get_object_or_404(models.Event, id=id, library=library)
    try:
        content = models.EventContent.objects.get(event=event, lang=cur_language[:2])
    except models.EventContent.DoesNotExist:
        content = None

    return render(request, 'participant_events/frontend/ical.html', {
        'event': event,
        'content': content
    }, content_type='text/calendar')


@login_required
def favorit_events(request, library_code):
    fav_events_page = get_page(request, models.FavoriteEvent.objects.filter(user=request.user))
    events = []
    for fav_event in fav_events_page.object_list:
        events.append(fav_event.event_id)

    events = models.Event.objects.filter(id__in=events)
    event_contents = list(models.EventContent.objects.filter(event__in=list(events), lang=get_language()[:2]))

    t_dict = {}
    for event in events:
        t_dict[event.id] = {'event': event}

    for event_content in event_contents:
        t_dict[event_content.event_id]['event'].event_content = event_content

    return render(request, 'participant_events/frontend/favorites_list.html', {
        'events_list': events,
        'events_page': fav_events_page,
    })


@login_required
def add_to_favorits(request, library_code, id):
    event = get_object_or_404(models.Event, id=id, library__code=library_code)
    try:
        favorite_event = models.FavoriteEvent.objects.get(user=request.user, event=event)
    except models.FavoriteEvent.DoesNotExist:
        models.FavoriteEvent(user=request.user, event=event).save()
    return redirect('participant_events:frontend:favorit_events')


@login_required
def favorite_show(request, library_code, id):
    cur_language = translation.get_language()
    event = get_object_or_404(models.Event, id=id)
    try:
        content = models.EventContent.objects.get(event=event, lang=cur_language[:2])
    except models.EventContent.DoesNotExist:
        content = None

    return render(request, 'participant_events/frontend/favorite_show.html', {
        'event': event,
        'content': content
    })
