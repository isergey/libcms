# -*- coding: utf-8 -*-
from django.conf import settings
from datetime import date, datetime
import calendar
from django import template
from django.core.cache import cache
from django.utils.translation import get_language
from django.db.models import Q
from ..models import Event, EventContent
from ..frontend.forms import CalendarFilterForm, get_current_month_choice, get_current_year_choice

register = template.Library()


@register.inclusion_tag('participant_events/tags/events_calendar.html', takes_context=True)
def participant_events_calendar(context, library, y=0, m=0):
    request = context['request']

    if request.method == 'POST':
        form = CalendarFilterForm(request.POST)
        if form.is_valid():
            y = int(form.cleaned_data['year'])
            m = int(form.cleaned_data['month'])
    else:
        form = CalendarFilterForm(
            initial={
                'month': get_current_month_choice(),
                'year': get_current_year_choice()
            }
        )
    today = date.today()
    year = today.year
    month = today.month

    if y: year = y
    if m: month = m
    weeks = calendar.monthcalendar(year, month)
    cache_key = 'participant_events_y_m' + str(year) + str(month) + 'active=1'
    events = cache.get(cache_key, [])
    if not events:
        events = list(
            Event.objects.filter(library=library, start_date__year=year, start_date__month=month, active=True))
        cache.set(cache_key, events)

    events = Event.objects.filter(library=library, start_date__year=year, start_date__month=month, active=True)
    calendar_of_events = []
    for week in weeks:
        week_events = []
        for day in week:
            day_events = {
                'day': 0,
                'today': False,
                'events': [],
            }
            day_events['day'] = day
            if day == today.day and year == today.year and month == today.month: day_events['today'] = True
            for event in events:
                if event.start_date.day == day:
                    day_events['events'].append({
                        'id': event.id,
                        #                        'title': event.title,
                        #                        'teaser': event.teaser
                    })
            week_events.append(day_events)
        calendar_of_events.append(week_events)
    return {
        'calendar': calendar_of_events,
        'month': month,
        'year': year,
        'form': form,
        'library': library
    }


@register.inclusion_tag('participant_events/tags/events_nearest.html')
def participant_events_nearest(library_id, count=5):
    query = Q(
        active=True,
        end_date__gte=datetime.now()
    )
    if library_id:
        query &= Q(library_id=library_id)
    events = list(
        Event.objects
            .select_related('library')
            .filter(query)
            .prefetch_related('age_category', 'event_type')
            .order_by('-start_date')[:count]
    )
    event_contents = list(EventContent.objects.filter(event__in=events, lang=get_language()[:2]))

    t_dict = {}
    for event in events:
        t_dict[event.id] = {'event': event}

    for event_content in event_contents:
        t_dict[event_content.event_id]['event'].event_content = event_content

    groups = []
    group = []
    j = 1
    for i, event in enumerate(events):
        group.append(event)
        if j % 2 == 0:
            groups.append(group)
            group = []
        j += 1
    if group:
        groups.append(group)
    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'events': events,
        'groups': groups
    }
