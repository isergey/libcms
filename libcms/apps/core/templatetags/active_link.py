# -*- ecoding: utf-8 -*-

from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import SafeUnicode
register = template.Library()

@register.simple_tag(takes_context=True)
def active(context, urls):

    if type(urls) == unicode:
        if context['request'].path == urls:
            return "active"
        else:
            return ""

    if context['request'].path in ( reverse(url) for url in urls.split() ):
        return "active"
    return ""


@register.simple_tag(takes_context=True)
def active_path(context, urls):
    """
    Если адрес ссылки начинается с адреса запроса
    """
    if type(urls) == unicode:
        if context['request'].path.startswith(urls):
            return "header-link_active"
        else:
            return ""

    for url in urls.split():
        if context['request'].path.startswith(reverse(url)):
            return "header-link_active"
    return ""