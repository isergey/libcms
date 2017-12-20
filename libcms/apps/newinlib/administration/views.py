# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import get_language, gettext
from guardian.decorators import permission_required_or_403

from common.pagination import get_page
from forms import ItemForm, ItemContentForm
from ..models import Item, ItemContent

LANGUAGES = (
    ('ru', gettext('Russian')),
#    ('en', gettext('English')),
#    ('tt', gettext('Tatar')),
)
#LANGUAGES = settings.LANGUAGES

@login_required
def index(request):
    if not request.user.has_module_perms('newinlib'):
        return HttpResponseForbidden()
    return redirect('newinlib:administration:items_list')


@login_required
@permission_required_or_403('newinlib.add_item')
def items_list(request):

    items_page = get_page(request, Item.objects.all().order_by('-create_date'))
    items_contents = list(ItemContent.objects.filter(item__in=list(items_page.object_list), lang=get_language()[:2]))

    t_dict = {}
    for item in items_page.object_list:
        t_dict[item.id] = {'item': item}

    for item_content in items_contents:
        t_dict[item_content.item_id]['item'].item_content = item_content

    return render(request, 'newinlib/administration/items_list.html', {
        'items_list': items_page.object_list,
        'items_page': items_page,
        })



@login_required
@permission_required_or_403('newinlib.add_item')
@transaction.atomic
def create_item(request):

    if request.method == 'POST':
        item_form = ItemForm(request.POST,prefix='item_form')

        item_content_forms = []
        for lang in LANGUAGES:
            item_content_forms.append({
                'form':ItemContentForm(request.POST,prefix='item_content' + lang[0]),
                'lang':lang[0]
            })

        if item_form.is_valid():



            valid = False
            for item_content_form in item_content_forms:
                valid = item_content_form['form'].is_valid()
                if not valid:
                    break

            if valid:
                item = item_form.save(commit=False)
                if 'item_form_avatar' in request.FILES:
                    avatar_img_name = handle_uploaded_file(request.FILES['item_form_avatar'])
                    item.avatar_img_name = avatar_img_name
                item.save()
                for item_content_form in item_content_forms:
                    item_content = item_content_form['form'].save(commit=False)
                    item_content.lang = item_content_form['lang']
                    item_content.item = item
                    item_content.save()
                return redirect('newinlib:administration:items_list')
    else:
        item_form = ItemForm(prefix="item_form")
        item_content_forms = []
        for lang in LANGUAGES:
            item_content_forms.append({
                'form':ItemContentForm(prefix='item_content' + lang[0]),
                'lang':lang[0]
            })

    return render(request, 'newinlib/administration/create_item.html', {
        'item_form': item_form,
        'item_content_forms': item_content_forms,
        })

@login_required
@permission_required_or_403('newinlib.change_item')
@transaction.atomic
def edit_item(request, id):
    item = get_object_or_404(Item, id=id)
    items_contents = ItemContent.objects.filter(item=item)
    item_contents_langs = {}

    for lang in LANGUAGES:
        item_contents_langs[lang] = None

    for item_content in items_contents:
        item_contents_langs[item_content.lang] = item_content

    if request.method == 'POST':
        item_form = ItemForm(request.POST,prefix='item_form', instance=item)

        if item_form.is_valid():
            item = item_form.save(commit=False)
            if 'item_form_avatar' in request.FILES:
                if item.avatar_img_name:
                    handle_uploaded_file(request.FILES['item_form_avatar'], item.avatar_img_name)
                else:
                    avatar_img_name = handle_uploaded_file(request.FILES['item_form_avatar'])
                    item.avatar_img_name = avatar_img_name
            item.save()
            item_content_forms = []
            for lang in LANGUAGES:
                lang = lang[0]
                if lang in item_contents_langs:
                    item_content_forms.append({
                        'form':ItemContentForm(request.POST,prefix='item_content_' + lang, instance=item_contents_langs[lang]),
                        'lang':lang
                    })
                else:
                    item_content_forms.append({
                        'form':ItemContentForm(request.POST, prefix='item_content_' + lang),
                        'lang':lang
                    })


            valid = False
            for item_content_form in item_content_forms:
                valid = item_content_form['form'].is_valid()
                if not valid:
                    break

            if valid:
                for item_content_form in item_content_forms:
                    item_content = item_content_form['form'].save(commit=False)
                    item_content.item = item
                    item_content.lang = item_content_form['lang']
                    item_content.save()
                return redirect('newinlib:administration:items_list')
    else:
        item_form = ItemForm(prefix="item_form", instance=item)
        item_content_forms = []
        for lang in LANGUAGES:
            lang = lang[0]
            if lang in item_contents_langs:
                item_content_forms.append({
                    'form':ItemContentForm(prefix='item_content_' + lang, instance=item_contents_langs[lang]),
                    'lang':lang
                })
            else:
                item_content_forms.append({
                    'form':ItemContentForm(prefix='item_content_' + lang),
                    'lang':lang
                })

    return render(request, 'newinlib/administration/edit_item.html', {
        'item_form': item_form,
        'item_content_forms': item_content_forms,
        })


@login_required
@permission_required_or_403('newinlib.delete_item')
@transaction.atomic
def delete_item(request, id):
    item = get_object_or_404(Item, id=id)
    item.delete()
    delete_avatar(item.avatar_img_name)
    return redirect('newinlib:administration:items_list')




import os
from PIL import Image
import uuid
from datetime import datetime

def get_im_crop(image, ratio, ):
    image_width = image.size[0]
    image_hight = image.size[1]
    image_ratio = float(image_width) / image_hight

    box = [0, 0, 0, 0]
    if image_ratio <= 1:
        new_hight = int(image_width / ratio)
        vert_offset = int((image_hight - new_hight) / 2)
        box[0] = 0
        box[1] = vert_offset
        box[2] = image_width
        box[3] = vert_offset + new_hight
    else:
        new_width = image_hight * ratio
        if new_width > image_width:
            new_width = image_width
            new_hight = int(new_width / ratio)
            vert_offset = int((image_hight - new_hight) / 2)
            box[0] = 0
            box[1] = vert_offset
            box[2] = new_width
            box[3] = vert_offset + new_hight
        else:
            gor_offset = int((image_width - new_width) / 2)
            box[0] = gor_offset
            box[1] = 0
            box[2] = int(gor_offset + new_width)
            box[3] = image_hight

    return image.crop(tuple(box))


def handle_uploaded_file(f, old_name=None):

    upload_dir = settings.MEDIA_ROOT + 'uploads/newinlib/itemavatars/'
    now = datetime.now()
    ratio = 0.67
    dirs = [
        upload_dir,
        upload_dir  + str(now.year) + str(now.month).zfill(2) + '/',
        upload_dir  + 'big/' +str(now.year) + str(now.month).zfill(2) + '/',
        ]
    for dir in dirs:
        if not os.path.isdir(dir):
            os.makedirs(dir, 0744)

    if old_name:
        name = old_name
    else:
        name =  str(now.year) + str(now.month).zfill(2) + '/' + uuid.uuid4().hex + '.jpg'

    path = upload_dir + name
    big_image_path = upload_dir + 'big/' + name

    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    im = Image.open(path).convert('RGB')
    im = get_im_crop(im, ratio)

    final_hight = 450
    final_width = int((ratio * final_hight))
    im = im.resize((final_width, final_hight), Image.ANTIALIAS)
    im.save(big_image_path, "JPEG",  quality=95)

    final_hight = 175
    final_width = int((ratio * final_hight))
    im = im.resize((final_width, final_hight), Image.ANTIALIAS)
    im.save(path, "JPEG",  quality=95)

    return name



def delete_avatar(name):
    upload_dir = settings.MEDIA_ROOT + 'uploads/newinlib/itemavatars/'
    if os.path.isfile(upload_dir + name):
        os.remove(upload_dir + name)
    if os.path.isfile(upload_dir + 'big/' + name):
        os.remove(upload_dir + 'big/' + name)