# -*- coding: utf-8 -*-
from django.core.cache import cache
from django import template
from django.utils import translation
from django.utils.translation import to_locale, get_language
from menu.models import Menu, MenuItemTitle

register = template.Library()
@register.inclusion_tag('menu/tags/drow_menu.html', takes_context=True)
def drow_menu(context, menu_slug):
    lang=get_language()[:2]
    menu = cache.get('menu_' + menu_slug + lang, None)
    if not menu:
        try:
            menu = Menu.objects.get(slug=menu_slug)
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


    item_titles = cache.get('menu_item_titles' + menu_slug + lang, None)
    if not item_titles:
        item_titles = list(MenuItemTitle.objects.filter(item__in=nodes, lang=lang))
        cache.set('menu_item_titles' + menu_slug + lang, item_titles)

    nd = {}
    for node in nodes:
        nd[node.id] = node

    for item_title in item_titles:
        nd[item_title.item_id].item_title = item_title

    if not item_titles:
        nodes = []
    return ({
        'nodes': nodes,
        'menu': menu,
        'path': path
    })

@register.inclusion_tag('menu/tags/drow_menu_default.html', takes_context=True)
def drow_menu_default(context, menu_slug):
    lang=get_language()[:2]
    menu = cache.get('menu_' + menu_slug + lang, None)
    if not menu:
        try:
            menu = Menu.objects.get(slug=menu_slug)
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


    item_titles = cache.get('menu_item_titles' + menu_slug + lang, None)
    if not item_titles:
        item_titles = list(MenuItemTitle.objects.filter(item__in=nodes, lang=lang))
        cache.set('menu_item_titles' + menu_slug + lang, item_titles)

    nd = {}
    for node in nodes:
        nd[node.id] = node

    for item_title in item_titles:
        nd[item_title.item_id].item_title = item_title

    if not item_titles:
        nodes = []
    return ({
        'nodes': nodes,
        'menu': menu,
        'path': path
    })
