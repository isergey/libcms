# -*- coding: utf-8 -*-
from django.core.cache import cache
from django import template
from django.utils.translation import get_language

from ..models import Menu


register = template.Library()
@register.inclusion_tag('participant_menu/tags/drow_menu.html', takes_context=True)
def drow_library_menu(context, library_id, menu_slug):
    lang = get_language()[:2]
    menu = cache.get('menu_' + menu_slug + str(library_id) + lang, None)
    if not menu:
        try:

            menu = Menu.objects.get(slug=menu_slug, library_id=library_id, lang=lang)
            cache.set('menu_' + menu_slug + lang, menu)
        except Menu.DoesNotExist:
            return ({
                'menu': None
            })

    path = context['request'].META['PATH_INFO']

    nodes = cache.get('menu_nodes' + menu_slug + lang, None)
    if not nodes:
        nodes = list(menu.root_item.get_descendants().exclude(show=False))
        cache.set('menu_nodes' + menu_slug + lang, nodes)

    return ({
        'nodes': nodes,
        'menu': menu,
        'path': path
    })

@register.inclusion_tag('participant_menu/tags/drow_menu_default.html', takes_context=True)
def drow_library_menu_default(context, library_id, menu_slug):
    lang = get_language()[:2]
    #menu = Menu.objects.get(slug=menu_slug, library_id=library_id, lang=lang)
    #print menu, 'menu'
    # menu = cache.get('menu_' + menu_slug + str(library_id) +  lang, None)
    # if not menu:
    #     try:
    #         menu = Menu.objects.get(slug=menu_slug, library_id=library_id, lang=lang)
    #         cache.set('menu_' + menu_slug + lang, menu)
    #     except Menu.DoesNotExist:
    #         return ({
    #             'menu': None
    #         })

    path = context['request'].META['PATH_INFO']
    #nodes = list(menu.root_item.get_descendants().exclude(show=False))
    #print nodes
    nodes = cache.get('menu_nodes' + menu_slug + lang, None)
    if not nodes:
        menu = Menu.objects.get(slug=menu_slug, library_id=library_id, lang=lang)
        nodes = list(menu.root_item.get_descendants().exclude(show=False))
        cache.set('menu_nodes' + menu_slug + lang, nodes)

    return ({
        'nodes': nodes,
        # 'menu': menu,
        'path': path
    })
