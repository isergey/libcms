# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language

from common.pagination import get_page

from participants import decorators, org_utils

from ..models import Menu, MenuTitle, MenuItem, MenuItemTitle
from forms import MenuForm, MenuTitleForm, MenuItemForm, MenuItemTitleForm


@login_required
@transaction.atomic()
@decorators.must_be_org_user
def index(request, library_code, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    if not request.user.has_module_perms('participant_menu'):
        return HttpResponseForbidden(u'У вас нет доступа к разделу')
    try:
        Menu.objects.get(slug='main_menu', library=library)
    except Menu.DoesNotExist:
        root_item = MenuItem()
        root_item.save()
        menu = Menu(slug='main_menu', library=library, root_item=root_item)
        menu.save()
        for lang in settings.LANGUAGES:
            MenuTitle(menu=menu, lang=lang[0], title='Main menu').save()

    return redirect('participant_menu:administration:menu_list', library_code=library_code)


@login_required
# @permission_required_or_403('menu.add_menu')
@decorators.must_be_org_user
def menu_list(request, library_code, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    if not request.user.has_module_perms('participant_menu'):
        return HttpResponseForbidden()
    menus_page = get_page(request, Menu.objects.filter(library=library))
    menu_titles = list(MenuTitle.objects.filter(menu__in=list(menus_page.object_list), lang=get_language()[:2]))

    menus_dict = {}
    for menu in menus_page.object_list:
        menus_dict[menu.id] = {'menu': menu}

    for menu_title in menu_titles:
        menus_dict[menu_title.menu_id]['menu'].menu_title = menu_title

    menus = [menu['menu'] for menu in menus_dict.values()]

    return render(request, 'participant_menu/administration/menus_list.html', {
        'library': library,
        'menus': menus,
        'menus_page': menus_page,
    })


@login_required
@permission_required_or_403('participant_menu.add_menu')
@transaction.atomic()
@decorators.must_be_org_user
def create_menu(request, library_code, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    if request.method == 'POST':

        menu_form = MenuForm(request.POST, prefix='menu_form')
        menu_title_forms = []

        for lang in settings.LANGUAGES:
            menu_title_forms.append({
                'form': MenuTitleForm(
                    request.POST,
                    prefix="menu_title_" + lang[0]
                ),
                'lang': lang
            })

        if menu_form.is_valid():
            menu = menu_form.save(commit=False)
            menu.library = library
            valid = False
            for menu_title_form in menu_title_forms:
                valid = menu_title_form['form'].is_valid()
                if not valid: break

            if valid:
                root_item = MenuItem()
                root_item.save()
                menu.root_item = root_item
                menu.save()

                for menu_title_form in menu_title_forms:
                    MenuTitle(
                        lang=menu_title_form['lang'][0],
                        title=menu_title_form['form'].cleaned_data['title'],
                        menu=menu
                    ).save()

            return redirect('participant_menu:administration:menu_list', library_code=library_code)
    else:
        menu_title_forms = []
        for lang in settings.LANGUAGES:
            menu_title_forms.append({
                'form': MenuTitleForm(
                    initial={
                        'lang': lang[0]
                    },
                    prefix="menu_title_" + lang[0]
                ),
                'lang': lang
            })
        menu_form = MenuForm(prefix='menu_form')

    return render(request, 'participant_menu/administration/create_menu.html', {
        'library': library,
        'menu_form': menu_form,
        'menu_title_forms': menu_title_forms
    })


@login_required
@permission_required_or_403('participant_menu.change_menu')
@transaction.atomic
@decorators.must_be_org_user
def edit_menu(request, id, library_code, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    menu = get_object_or_404(Menu, id=id)
    menu_item_titles = MenuTitle.objects.filter(menu=menu)
    menu_item_titles_langs = {}
    for menu_item_title in menu_item_titles:
        menu_item_titles_langs[menu_item_title.lang] = menu_item_title

    if request.method == 'POST':
        menu_form = MenuForm(request.POST, prefix='menu_form', instance=menu)

        menu_title_forms = []

        if menu_form.is_valid():
            menu = menu_form.save(commit=False)

            for lang in settings.LANGUAGES:
                menu_title_forms.append({
                    'form': MenuTitleForm(
                        request.POST,
                        prefix="menu_title_" + lang[0]
                    ),
                    'lang': lang
                })

            valid = False
            for menu_title_form in menu_title_forms:
                valid = menu_title_form['form'].is_valid()
                if not valid:
                    break
            if valid:
                menu.save()

                for menu_title_form in menu_title_forms:
                    lang = menu_title_form['form'].cleaned_data['lang']
                    if lang in menu_item_titles_langs:
                        if menu_item_titles_langs[lang].title != menu_title_form['form'].cleaned_data['title']:
                            menu_item_titles_langs[lang].title = menu_title_form['form'].cleaned_data['title']
                            menu_item_titles_langs[lang].save()
                    else:
                        MenuTitle(
                            lang=lang,
                            title=menu_title_form['form'].cleaned_data['title'],
                            menu=menu
                        ).save()

            return redirect('participant_menu:administration:menu_list', library_code=library_code)
    else:
        menu_title_forms = []
        menus_title_langs = []

        for lang in settings.LANGUAGES:
            for menu_item_title in menu_item_titles:
                if menu_item_title.lang == lang[0]:
                    menus_title_langs.append(lang[0])
                    menu_title_forms.append({
                        'form': MenuTitleForm(
                            initial={
                                'lang': menu_item_title.lang,
                                'title': menu_item_title.title,
                            },
                            prefix="menu_title_" + menu_item_title.lang
                        ),
                        'lang': menu_item_title.lang
                    })
        new_langs = []
        if len(settings.LANGUAGES) != len(menus_title_langs):
            for lang in settings.LANGUAGES:
                if lang[0] not in menus_title_langs:
                    new_langs.append(lang[0])

        for lang in new_langs:
            menu_title_forms.append({
                'form': MenuTitleForm(
                    initial={
                        'lang': lang
                    },
                    prefix="menu_title_" + lang
                ),
                'lang': lang
            })

        menu_form = MenuForm(prefix='menu_form', instance=menu)

    return render(request, 'participant_menu/administration/edit_menu.html', {
        'library': library,
        'menu_form': menu_form,
        'menu_title_forms': menu_title_forms
    })


@login_required
@permission_required_or_403('participant_menu.delete_menu')
@transaction.atomic
@decorators.must_be_org_user
def delete_menu(request, id, library_code, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    menu = get_object_or_404(Menu, id=id)
    menu.delete()
    return redirect('participant_menu:administration:menus_list', library_code=library_code)


@login_required
# @permission_required_or_403('menu.create_menu')
@decorators.must_be_org_user
def item_list(request, menu_id, library_code, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    menu = get_object_or_404(Menu, id=menu_id)
    nodes = list(menu.root_item.get_descendants())
    lang = get_language()[:2]
    item_titles = MenuItemTitle.objects.filter(item__in=nodes, lang=lang)
    nd = {}
    for node in nodes:
        nd[node.id] = node

    for item_title in item_titles:
        nd[item_title.item_id].t_title = item_title

    return render(request, 'participant_menu/administration/item_list.html', {
        'library': library,
        'nodes': nodes,
        'menu': menu
    })


@login_required
@permission_required_or_403('participant_menu.add_menuitem')
@transaction.atomic
@decorators.must_be_org_user
def create_item(request, menu_id, library_code, parent=None, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    menu = get_object_or_404(Menu, id=menu_id)

    if not parent:
        parent = menu.root_item
    else:
        parent = get_object_or_404(MenuItem, id=parent)

    if request.method == 'POST':
        item_form = MenuItemForm(request.POST, prefix='item_form')

        menu_item_title_forms = []
        for lang in settings.LANGUAGES:
            menu_item_title_forms.append({
                'form': MenuItemTitleForm(request.POST, prefix='menu_item_title_' + lang[0]),
                'lang': lang[0]
            })

        if item_form.is_valid():

            item = item_form.save(commit=False)
            item.parent = parent
            item.show = parent.show
            item.save()

            valid = False
            for menu_item_title_form in menu_item_title_forms:
                valid = menu_item_title_form['form'].is_valid()
                if not valid:
                    break

            if valid:
                for menu_item_title_form in menu_item_title_forms:
                    menu_item_title = menu_item_title_form['form'].save(commit=False)
                    menu_item_title.lang = menu_item_title_form['lang']
                    menu_item_title.item = item
                    menu_item_title.save()
                return redirect('participant_menu:administration:item_list', menu_id=menu.id, library_code=library_code)
    else:
        item_form = MenuItemForm(prefix="item_form")
        menu_item_title_forms = []
        for lang in settings.LANGUAGES:
            menu_item_title_forms.append({
                'form': MenuItemTitleForm(initial={'url': u'/' + lang[0] + u'/#'}, prefix='menu_item_title_' + lang[0]),
                'lang': lang[0]
            })

    return render(request, 'participant_menu/administration/create_item.html', {
        'library': library,
        'item_form': item_form,
        'menu_item_title_forms': menu_item_title_forms,
        'menu': menu
    })


@login_required
@permission_required_or_403('participant_menu.change_menuitem')
@transaction.atomic()
@decorators.must_be_org_user
def item_edit(request, id, library_code, menu_id=None, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    menu = get_object_or_404(Menu, id=menu_id)
    item = get_object_or_404(MenuItem, id=id)
    item_titles = MenuItemTitle.objects.filter(item=item)

    item_titles_langs = {}
    for lang in settings.LANGUAGES:
        item_titles_langs[lang] = None

    for item_title in item_titles:
        item_titles_langs[item_title.lang] = item_title

    if request.method == 'POST':
        item_form = MenuItemForm(request.POST, prefix='item_form', instance=item)
        menu_item_title_forms = []
        for lang in settings.LANGUAGES:
            if lang in item_titles_langs:
                lang = lang[0]
                if lang in item_titles_langs:
                    menu_item_title_forms.append({
                        'form': MenuItemTitleForm(request.POST, prefix='menu_item_title_' + lang,
                                                  instance=item_titles_langs[lang]),
                        'lang': lang
                    })
                else:
                    menu_item_title_forms.append({
                        'form': MenuItemTitleForm(request.POST, prefix='menu_item_title_' + lang),
                        'lang': lang
                    })

        valid = False
        for menu_item_title_form in menu_item_title_forms:
            valid = menu_item_title_form['form'].is_valid()
            if not valid:
                break

        if not item_form.is_valid():
            valid = False

        if valid:
            item = item_form.save()
            for menu_item_title_form in menu_item_title_forms:
                menu_item_title = menu_item_title_form['form'].save(commit=False)
                menu_item_title.item = item
                menu_item_title.lang = menu_item_title_form['lang']
                menu_item_title.save()

            if not item.is_leaf_node():
                ditems = item.get_descendants()
                for ditem in ditems:
                    ditem.show = item.show
                    ditem.save()

            return redirect('participant_menu:administration:item_list', menu_id=menu_id, library_code=library_code)


    else:
        item_form = MenuItemForm(prefix="item_form", instance=item)
        menu_item_title_forms = []
        for lang in settings.LANGUAGES:
            lang = lang[0]
            if lang in item_titles_langs:
                menu_item_title_forms.append({
                    'form': MenuItemTitleForm(prefix='menu_item_title_' + lang, instance=item_titles_langs[lang]),
                    'lang': lang
                })
            else:
                menu_item_title_forms.append({
                    'form': MenuItemTitleForm(prefix='menu_item_title_' + lang),
                    'lang': lang
                })

    return render(request, 'participant_menu/administration/edit_item.html', {
        'library': library,
        'item': item,
        'item_form': item_form,
        'menu_item_title_forms': menu_item_title_forms,
        'menu': menu
    })


@login_required
@permission_required_or_403('participant_menu.delete_menuitem')
@transaction.atomic
@decorators.must_be_org_user
def item_delete(request, menu_id, id, library_code, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    item = get_object_or_404(MenuItem, id=id)
    item.delete()
    return redirect('participant_menu:administration:item_list', menu_id=menu_id, library_code=library_code)


@login_required
@permission_required_or_403('participant_menu.change_menu')
@transaction.atomic
@decorators.must_be_org_user
def item_up(request, menu_id, id, library_code, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    item = get_object_or_404(MenuItem, id=id)
    item.up()
    return redirect('participant_menu:administration:item_list', menu_id=menu_id, library_code=library_code)


@login_required
@permission_required_or_403('participant_menu.change_menu')
@transaction.atomic
@decorators.must_be_org_user
def item_down(request, menu_id, id, library_code, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    item = get_object_or_404(MenuItem, id=id)
    item.down()
    return redirect('participant_menu:administration:item_list', menu_id=menu_id, library_code=library_code)






