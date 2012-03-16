# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import transaction
from django.utils.translation import ugettext as _
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required
from common.pagination import get_page
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.utils.translation import to_locale, get_language

from core.forms import LanguageForm
from menu.models import Menu, MenuTitle, MenuItem, MenuItemTitle
from forms import MenuForm,MenuTitleForm,  MenuItemForm, MenuItemTitleForm



#@permission_required_or_403('accounts.view_users')
def index(request):
    return redirect('menu:administration:menu_list')
    #return render(request, 'menus/administration/index.html')




@login_required
@permission_required_or_403('menu.add_menu')
def menu_list(request):
    menus_page = get_page(request, Menu.objects.all())
    menu_titles = list(MenuTitle.objects.filter(menu__in=list(menus_page.object_list), lang=get_language()[:2]))

    menus_dict = {}
    for menu in menus_page.object_list:
        menus_dict[menu.id] = {'menu':menu}

    for menu_title in menu_titles:
        menus_dict[menu_title.menu_id]['menu'].menu_title = menu_title

    menus = [menu['menu'] for menu in menus_dict.values()]


    return render(request, 'menu/administration/menus_list.html', {
        'menus': menus,
        'menus_page': menus_page,
    })




@login_required
@permission_required_or_403('menu.add_menu')
@transaction.commit_on_success
def create_menu(request):

    if request.method == 'POST':

        menu_form = MenuForm(request.POST, prefix='menu_form')
        menu_title_forms = []

        for lang in settings.LANGUAGES:
            menu_title_forms.append({
                'form':MenuTitleForm(
                    request.POST,
                    prefix="menu_title_" + lang[0]
                ),
                'lang': lang
            })

        if menu_form.is_valid():
            menu = menu_form.save(commit=False)
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

            return redirect('menu:administration:menu_list')
    else:
        menu_title_forms = []
        for lang in settings.LANGUAGES:
            menu_title_forms.append({
                'form':MenuTitleForm(
                    initial={
                        'lang':lang[0]
                    },
                    prefix="menu_title_" + lang[0]
                ),
                'lang':lang
            })
        menu_form = MenuForm(prefix='menu_form')

    return render(request, 'menu/administration/create_menu.html', {
        'menu_form': menu_form,
        'menu_title_forms': menu_title_forms
     })




@login_required
@permission_required_or_403('menu.change_menu')
@transaction.commit_on_success
def edit_menu(request, id):

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
                    'form':MenuTitleForm(
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
                    if lang in  menu_item_titles_langs:
                        if menu_item_titles_langs[lang].title != menu_title_form['form'].cleaned_data['title']:
                            menu_item_titles_langs[lang].title = menu_title_form['form'].cleaned_data['title']
                            menu_item_titles_langs[lang].save()
                    else:
                        MenuTitle(
                            lang=lang,
                            title=menu_title_form['form'].cleaned_data['title'],
                            menu=menu
                        ).save()

            return redirect('menu:administration:menu_list')
    else:
        menu_title_forms = []
        menus_title_langs = []

        for lang in settings.LANGUAGES:
            for menu_item_title in menu_item_titles:
                if menu_item_title.lang == lang[0]:
                    menus_title_langs.append(lang[0])
                    menu_title_forms.append({
                        'form':MenuTitleForm(
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
                if lang[0] not in  menus_title_langs:
                    new_langs.append(lang[0])

        for lang in new_langs:
            menu_title_forms.append({
                'form':MenuTitleForm(
                    initial={
                        'lang':lang
                    },
                    prefix="menu_title_" + lang
                ),
                'lang':lang
            })

        menu_form = MenuForm(prefix='menu_form', instance=menu)


    return render(request, 'menu/administration/edit_menu.html', {
        'menu_form': menu_form,
        'menu_title_forms': menu_title_forms
    })


@login_required
@permission_required_or_403('menu.delete_menu')
@transaction.commit_on_success
def delete_menu(request, id):
    menu = get_object_or_404(Menu, id=id)
    menu.delete()
    return redirect('menu:administration:menus_list')





def item_list(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    nodes = list(menu.root_item.get_descendants())
    item_titles = MenuItemTitle.objects.filter(item__in=nodes, lang='ru')
    nd = {}
    for node in nodes:
        nd[node.id] = node

    for item_title in item_titles:
        nd[item_title.item_id].title = item_title

    return render(request, 'menu/administration/item_list.html', {
        'nodes': nodes
    })



@transaction.commit_on_success
def create_item(request, menu_id, parent=None):
    menu = get_object_or_404(Menu, id=menu_id)
    root_item = menu.root_item

    if request.method == 'POST':
        item_form = MenuItemForm(request.POST,prefix='item_form')

        menu_item_title_forms = []
        for lang in settings.LANGUAGES:
            menu_item_title_forms.append({
                'form':MenuItemTitleForm(request.POST,prefix='menu_item_title_' + lang[0]),
                'lang':lang[0]
            })

        if item_form.is_valid():

            item = item_form.save()


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
    else:
        item_form = MenuItemForm(prefix="item_form")
        menu_item_title_forms = []
        for lang in settings.LANGUAGES:
            menu_item_title_forms.append({
                'form':MenuItemTitleForm(prefix='menu_item_title_' + lang[0]),
                'lang':lang[0]
            })

    return render(request, 'menu/administration/create_item.html', {
        'item_form': item_form,
        'menu_item_title_forms': menu_item_title_forms
    })



@transaction.commit_on_success
def item_edit(request, id, menu_id=None):
    item = get_object_or_404(MenuItem, id=id)
    item_titles = MenuItemTitle.objects.filter(item=item)

    item_titles_langs = {}
    for lang in settings.LANGUAGES:
        item_titles_langs[lang] = None


    for item_title in item_titles:
        item_titles_langs[item_title.lang] = item_title


    if request.method == 'POST':
        item_form = MenuItemForm(prefix='item_form', instance=item)
        menu_item_title_forms = []
        for lang in settings.LANGUAGES:
            if lang in item_titles_langs:
                lang = lang[0]
                menu_item_title_forms.append({
                    'form':MenuItemTitleForm(request.POST,prefix='menu_item_title_' + lang, instance=item_titles_langs[lang]),
                    'lang':lang
                })

        valid = False
        for menu_item_title_form in menu_item_title_forms:
            valid = menu_item_title_form['form'].is_valid()
            if not valid:
                break


        if valid:
            for menu_item_title_form in menu_item_title_forms:
                menu_item_title = menu_item_title_form['form'].save(commit=False)
                menu_item_title.save()
#                menu_item_title.lang = menu_item_title_form['lang']


    else:
        item_form = MenuItemForm(prefix="item_form", instance=item)
        menu_item_title_forms = []
        for lang in settings.LANGUAGES:
            lang = lang[0]
            menu_item_title_forms.append({
                'form':MenuItemTitleForm(prefix='menu_item_title_' + lang, instance=item_titles_langs[lang]),
                'lang':lang
            })

    return render(request, 'menu/administration/create_item.html', {
        'item_form': item_form,
        'menu_item_title_forms': menu_item_title_forms
    })



#@login_required
#@permission_required_or_403('menus.public_menu')
#def toggle_menu_public(request, id):
#    menu = get_object_or_404(Menu, id=id)
#    if menu.public:
#        menu.public = False
#    else:
#        menu.public = True
#    menu.save()
#    return redirect('menus:administration:menus_list')







#
#
#@login_required
#@permission_required_or_403('menus.add_menu')
#def create_menu_menu_title(request, menu_id):
#    menu = get_object_or_404(Menu, id=menu_id)
#    if request.method == 'POST':
#        menu_title_form = MenuTitleForm(request.POST, prefix='menu_title_form')
#
#        if menu_title_form.is_valid():
#            menu_title = menu_title_form.save(commit=False)
#            menu_title.menu = menu
#            menu_title.save()
#
#            save = request.POST.get('save', u'save_edit')
#            if save == u'save':
#                return redirect('menus:administration:edit_menu', id=menu_id)
#            else:
#                return redirect('menus:administration:edit_menu_menu_title', menu_id=menu_id, lang=menu_title.lang)
#    else:
#        menu_title_form = MenuTitleForm(prefix='menu_title_form')
#    return render(request, 'menus/administration/create_menu_menu_title.html', {
#        'menu': menu,
#        'menu_title_form': menu_title_form,
#    })
#
#@login_required
#@permission_required_or_403('menus.change_menu')
#def edit_menu_menu_title(request, menu_id, lang):
#    lang_form = LanguageForm({'lang': lang})
#    if not lang_form.is_valid():
#        return HttpResponse(_(u'Language is not registered in system.') + _(u" Language code: ") + lang)
#
#    menu = get_object_or_404(Menu, id=menu_id)
#
#    try:
#        menu_title = MenuTitle.objects.get(menu=menu_id, lang=lang)
#    except MenuTitle.DoesNotExist:
#        menu_title = MenuTitle(menu=menu, lang=lang)
#
#    MenuTitleForm = get_page_title_form(('menu', 'lang'))
#
#    if request.method == 'POST':
#        menu_title_form = MenuTitleForm(request.POST, prefix='menu_title_form', instance=menu_title)
#
#        if menu_title_form.is_valid():
#            menu_title = menu_title_form.save(commit=False)
#            menu_title.menu = menu
#            menu_title.save()
#
#        save = request.POST.get('save', u'save_edit')
#        if save == u'save':
#            return redirect('menus:administration:edit_menu', id=menu_id)
#
#    else:
#        menu_title_form = MenuTitleForm(prefix='menu_title_form', instance=menu_title)
#    return render(request, 'menus/administration/edit_menu_menu_title.html', {
#        'menu_title': menu_title,
#        'menu_title_form': menu_title_form,
#    })
#
#




