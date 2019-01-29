# -*- coding: utf-8 -*-
from django import template
from django.utils import translation
from django.utils.translation import to_locale, get_language
from pages.models import Page, Content

register = template.Library()


@register.filter
def get_cur_lang_content(page):
    cur_language = translation.get_language()
    try:
        content = Content.objects.get(page=page, lang=cur_language[:2])
    except Content.DoesNotExist:
        content = None
    return content


@register.inclusion_tag('pages/templatetags/render_page_content.html')
def render_page_content(slug):
    cur_language = translation.get_language()
    try:
        content = Content.objects.get(page__url_path=slug, lang=cur_language[:2], page__public=True).content
    except Content.DoesNotExist:
        content = ''
    return {
        'content': content
    }
