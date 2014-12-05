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