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

from ..models import Menu, MenuItem
from forms import MenuForm, MenuItemForm


@login_required
@transaction.atomic()
@decorators.must_be_org_user
def index(request, library_code, managed_libraries=[]):
    # library = org_utils.get_library(library_code, managed_libraries)
    # if not library:
    #     return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')
    #
    # if not request.user.has_module_perms('participant_menu'):
    #     return HttpResponseForbidden(u'У вас нет доступа к разделу')
    # try:
    #     Menu.objects.get(slug='main_menu', library=library)
    # except Menu.DoesNotExist:
    #     for lang in settings.LANGUAGES:
    #         root_item = MenuItem()
    #         root_item.save()
    #         menu = Menu(slug='main_menu', library=library, root_item=root_item, lang=lang[0])
    #         menu.save()

    return redirect('participant_menu:administration:menu_list', library_code=library_code)


@login_required
@transaction.atomic()
# @permission_required_or_403('menu.add_menu')
@decorators.must_be_org_user
def menu_list(request, library_code, managed_libraries=[]):
    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')

    if not request.user.has_module_perms('participant_menu'):
        return HttpResponseForbidden()


    for lang in settings.LANGUAGES:
        try:
            menu = Menu.objects.get(slug='main_menu', library=library, lang=lang[0])
        except Menu.DoesNotExist:
            root_item = MenuItem()
            root_item.save()
            menu = Menu(
                slug='main_menu',
                library=library,
                lang=lang[0],
                root_item=root_item,
                title=u'Главное меню'
            )
            menu.save()

    menu_list = Menu.objects.filter(library=library).order_by('slug', 'lang')

    return render(request, 'participant_menu/administration/menus_list.html', {
        'library': library,
        'menu_list': menu_list,
    })


@login_required
@transaction.atomic()
@decorators.must_be_org_user
def menu_detail(request, library_code, menu_id, managed_libraries=[]):
    if not request.user.has_module_perms('participant_menu'):
        return HttpResponseForbidden()

    library = org_utils.get_library(library_code, managed_libraries)
    if not library:
        return HttpResponseForbidden(u'Вы должны быть сотрудником этой организации')
    menu = get_object_or_404(Menu, id=menu_id)
    nodes = list(menu.root_item.get_descendants())
    return render(request, 'participant_menu/administration/menu_detail.html', {
        'menu': menu,
        'nodes': nodes,
        'library': library
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
        if menu_form.is_valid():
            menu = menu_form.save(commit=False)
            menu.library = library
            root_item = MenuItem()
            root_item.save()
            menu.root_item = root_item
            menu.save()
            return redirect('participant_menu:administration:menu_list', library_code=library_code)
    else:
        menu_form = MenuForm(prefix='menu_form')

    return render(request, 'participant_menu/administration/create_menu.html', {
        'library': library,
        'menu_form': menu_form
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

    if request.method == 'POST':
        menu_form = MenuForm(request.POST, prefix='menu_form', instance=menu)

        if menu_form.is_valid():
            menu = menu_form.save(commit=False)
            menu.save()

            return redirect('participant_menu:administration:menu_list', library_code=library_code)
    else:
        menu_form = MenuForm(prefix='menu_form', instance=menu)

    return render(request, 'participant_menu/administration/edit_menu.html', {
        'library': library,
        'menu_form': menu_form,
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

        if item_form.is_valid():

            item = item_form.save(commit=False)
            item.parent = parent
            item.show = parent.show
            item.save()
            return redirect('participant_menu:administration:menu_detail', menu_id=menu.id, library_code=library_code)
    else:
        item_form = MenuItemForm(prefix="item_form")

    return render(request, 'participant_menu/administration/create_item.html', {
        'library': library,
        'item_form': item_form,
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

    if request.method == 'POST':
        item_form = MenuItemForm(request.POST, prefix='item_form', instance=item)
        if item_form.is_valid():
            item_form.save()
            return redirect('participant_menu:administration:menu_detail', menu_id=menu_id, library_code=library_code)

    else:
        item_form = MenuItemForm(prefix="item_form", instance=item)
    return render(request, 'participant_menu/administration/edit_item.html', {
        'library': library,
        'item': item,
        'item_form': item_form,
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
    return redirect('participant_menu:administration:menu_detail', menu_id=menu_id, library_code=library_code)


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
    return redirect('participant_menu:administration:menu_detail', menu_id=menu_id, library_code=library_code)


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
    return redirect('participant_menu:administration:menu_detail', menu_id=menu_id, library_code=library_code)






