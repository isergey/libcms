# -*- coding: utf-8 -*-
from django import template
from django.utils import translation
from django.utils.translation import to_locale, get_language
from ..models import Page, Content

register = template.Library()

@register.filter
def get_cur_lang_content(page):
    cur_language = translation.get_language()
    try:
        content = Content.objects.get(page=page, lang=cur_language[:2])
    except Content.DoesNotExist:
        content = None
    return content


register = template.Library()
@register.inclusion_tag('participants_pages/tags/drow_page_tree.html', takes_context=True)
def drow_page_tree(context, library_id):
    request =  context['request']
    pages = list(Page.objects.filter(library=library_id))
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
        'library_id': library_id,
        'request': request

    }


