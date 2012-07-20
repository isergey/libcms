# -*- coding: utf-8 -*-
from django import template
from django.utils.translation import get_language
from ..models import Page, Content

register = template.Library()

@register.inclusion_tag('professionals_pages/tags/professionals_pages_tree.html', takes_context=True)
def professionals_pages_tree(context):
    request =  context['request']
    pages = list(Page.objects.filter(public=True))
    lang=get_language()[:2]
    pages_contents = list(Content.objects.filter(page__in=pages, lang=lang).values('page_id', 'title'))
    pages_dict = {}
    for page in pages:
        pages_dict[page.id] = page

    for page_content in pages_contents:
        pages_dict[page_content['page_id']].title = page_content['title']

    if not pages_contents:
        pages = []
    #

    return {
        'nodes': pages,
        'request': request

    }