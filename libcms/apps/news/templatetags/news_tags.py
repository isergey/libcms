# -*- coding: utf-8 -*-
import calendar
from datetime import date
from django.core.cache import cache
from django import template
from django.utils.translation import get_language
from ..models import News, NewsContent
from ..frontend.forms import CalendarFilterForm, get_current_month_choice, get_current_year_choice
register = template.Library()


@register.inclusion_tag('news/tags/news_feed.html')
def news_feed(count=5):
    news_list = list(News.objects.filter(publicated=True).exclude(type=1).order_by('-create_date')[:count])
    lang=get_language()[:2]
    news_contents = NewsContent.objects.filter(news__in=news_list, lang=lang)
    nd = {}
    for news in news_list:
        nd[news.id] = news

    for news_content in news_contents:
        nd[news_content.news_id].news_content = news_content

    if not news_contents:
        news_list = []
    return ({
        'news_list': news_list,
    })


@register.inclusion_tag('news/tags/news_feed.html')
def other_news(current_id, count=5):
    news_list = list(News.objects.filter(publicated=True).exclude(type=1).order_by('-create_date').exclude(id=current_id)[:count])
    lang=get_language()[:2]
    news_contents = NewsContent.objects.filter(news__in=news_list, lang=lang)
    nd = {}
    for news in news_list:
        nd[news.id] = news

    for news_content in news_contents:
        nd[news_content.news_id].news_content = news_content

    if not news_contents:
        news_list = []
    return ({
        'news_list': news_list,
    })


@register.inclusion_tag('news/tags/news_calendar.html', takes_context=True)
def news_calendar(context, y=0, m=0):
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
    cache_key = 'events_y_m' + str(year) + str(month) + 'active=1'
    events = cache.get(cache_key, [])
    if not events:
        events = list(
            News.objects.filter(create_date__year=year, create_date__month=month, publicated=True))
        cache.set(cache_key, events)

    events = News.objects.filter(create_date__year=year, create_date__month=month, publicated=True)
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
                if event.create_date.day == day:
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
    }