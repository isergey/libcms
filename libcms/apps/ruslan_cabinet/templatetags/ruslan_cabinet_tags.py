from datetime import datetime
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def to_datetime(value, format):
    if not value:
        return ''
    try:
        return datetime.strptime(value, format)
    except Exception as e:
        return ''


