from django import template
import datetime
from ..models import Poll, Choice


register = template.Library()

@register.inclusion_tag('polls/tags/tags_polls_form.html', takes_context=True)
def poll_form(context):
    now = datetime.datetime.now()
    polls = Poll.objects.filter(published=True, start_poll_date__lte=now, end_poll_date__gt=now).order_by('-id')[:1]
    poll = None
    choices = []
    if len(polls):
        poll = polls[0]
        choices = Choice.objects.filter(poll=poll).order_by('-sort')
    return {
        'poll': poll,
        'choices': choices,
        'STATIC_URL': context.get('STATIC_URL', None)
    }