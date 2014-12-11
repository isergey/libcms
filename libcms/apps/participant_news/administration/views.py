# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.utils.translation import get_language
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required
from common.pagination import get_page

from participant_site.decorators import must_be_manager
from ..models import News, NewsImage
from . import forms

@login_required
@permission_required_or_403('participant_news.add_news')
@must_be_manager
def index(request, library_code, library):
    return redirect('participant_news:administration:news_list', library_code=library_code)


@login_required
@permission_required_or_403('news.add_news')
@must_be_manager
def news_list(request, library_code, library):
    news_page = get_page(request, News.objects.filter(library=library).order_by('-order', '-create_date'))
    return render(request, 'participant_news/administration/news_list.html', {
        'library': library,
        'news_list': news_page.object_list,
        'news_page': news_page,
        })



@login_required
@permission_required_or_403('participant_news.add_news')
@transaction.atomic()
@must_be_manager
def create_news(request, library_code, library):

    if request.method == 'POST':
        news_form = forms.NewsForm(request.POST, prefix='news_form')

        if news_form.is_valid():
                news = news_form.save(commit=False)
                if 'news_form_avatar' in request.FILES:
                    avatar_img_name = handle_uploaded_file(request.FILES['news_form_avatar'])
                    news.avatar_img_name = avatar_img_name
                news.library = library
                news.save()
                if 'save_edit' in request.POST:
                    return redirect('participant_news:administration:edit_news', library_code=library_code, id=news.id)
                else:
                    return redirect('participant_news:administration:news_list', library_code=library_code)
    else:
        news_form = forms.NewsForm(prefix="news_form")

    return render(request, 'participant_news/administration/create_news.html', {
        'library': library,
        'news_form': news_form,
        })

@login_required
@permission_required_or_403('participant_news.change_news')
@transaction.atomic()
@must_be_manager
def edit_news(request, library_code, library, id):
    news = get_object_or_404(News, library=library, id=id)
    if request.method == 'POST':
        news_form = forms.NewsForm(request.POST,prefix='news_form', instance=news)

        if news_form.is_valid():
            news = news_form.save(commit=False)
            if 'news_form_avatar' in request.FILES:
                if news.avatar_img_name:
                    handle_uploaded_file(request.FILES['news_form_avatar'], news.avatar_img_name)
                else:
                    avatar_img_name = handle_uploaded_file(request.FILES['news_form_avatar'])
                    news.avatar_img_name = avatar_img_name
            news.save()
            if 'save_edit' in request.POST:
                return redirect('participant_news:administration:edit_news', library_code=library_code, id=news.id)
            else:
                return redirect('participant_news:administration:news_list', library_code=library_code)
    else:
        news_form = forms.NewsForm(prefix="news_form", instance=news)
    return render(request, 'participant_news/administration/edit_news.html', {
        'library': library,
        'news': news,
        'news_form': news_form,
        'content_type': 'participant_news_' + str(library.id),
        'content_id': unicode(news.id)
        })


@login_required
@permission_required_or_403('participant_news.delete_news')
@transaction.atomic()
@must_be_manager
def delete_news(request, library_code, library, id):
    news = get_object_or_404(News, library=library, id=id)
    news.delete()
    delete_avatar(news.avatar_img_name)
    return redirect('participant_news:administration:news_list', library_code=library_code)




@login_required
@permission_required_or_403('participant_news.change_news')
@transaction.atomic()
@must_be_manager
def news_images(request, library_code, library, id):
    news = get_object_or_404(News, library=library, id=id)
    news_images = NewsImage.objects.filter(news=news)
    return render(request, 'participant_news/administration/news_images.html', {
        'news_images': news_images,
        'news': news,
        'library': library
    })


@login_required
@permission_required_or_403('participant_news.change_news')
@transaction.atomic()
@must_be_manager
def create_news_image(request, library_code, library, id):
    news = get_object_or_404(News, library=library, id=id)

    if request.method == 'POST':
        form = forms.NewsImageForm(request.POST, request.FILES)
        if form.is_valid():
            news_image = form.save(commit=False)
            news_image.news = news
            news_image.save()
            return redirect('participant_news:administration:news_images', library_code=library_code, id=id)
    else:
        form = forms.NewsImageForm()

    return render(request, 'participant_news/administration/create_news_image.html', {
        'news': news,
        'library': library,
        'form': form
    })

@login_required
@permission_required_or_403('participant_news.change_news')
@transaction.atomic()
@must_be_manager
def edit_news_image(request, library_code, library, id, image_id):
    news_image = get_object_or_404(NewsImage, news_id=id, id=image_id)

    if request.method == 'POST':
        form = forms.NewsImageForm(request.POST, request.FILES, instance=news_image)
        if form.is_valid():
            form.save()
            return redirect('participant_news:administration:news_images', library_code=library_code, id=news_image.news_id)
    else:
        form = forms.NewsImageForm(instance=news_image)

    return render(request, 'participant_news/administration/edit_news_image.html', {
        'news': news_image.news,
        'news_image': news_image,
        'library': library,
        'form': form
    })

@login_required
@permission_required_or_403('participant_news.change_news')
@transaction.atomic()
@must_be_manager
def delete_news_image(request, library_code, library, id, image_id):
    news_image = get_object_or_404(NewsImage, news_id=id, id=image_id)
    news_image.delete()
    return redirect('participant_news:administration:news_images', library_code=library_code, id=id)


import os
from PIL import Image
import uuid
from datetime import datetime

UPLOAD_DIR =  settings.MEDIA_ROOT + 'uploads/participant_news/newsavatars/'
def handle_uploaded_file(f, old_name=None):
    upload_dir = UPLOAD_DIR
    now = datetime.now()
    dirs = [
        upload_dir,
        upload_dir  + str(now.year) + '/',
        upload_dir  + str(now.year) + '/' + str(now.month) + '/',
        ]
    for dir in dirs:
        if not os.path.isdir(dir):
            os.makedirs(dir, 0755)
    size = 147, 110
    if old_name:
        name = old_name
    else:
        name = str(now.year) + '/' + str(now.month) + '/' + uuid.uuid4().hex + '.jpg'
    path = upload_dir + name
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    im = Image.open(path)
    image_width = im.size[0]
    image_hight = im.size[1]
    image_ratio = float(image_width) / image_hight

    box = [0, 0, 0, 0]
    if image_ratio <= 1:
        new_hight = int(image_width / 1.333)
        vert_offset = int((image_hight - new_hight) / 2)
        box[0] = 0
        box[1] = vert_offset
        box[2] = image_width
        box[3] = vert_offset + new_hight
    else:
        new_width = image_hight * 1.333
        if new_width > image_width:
            new_width = image_width
            new_hight = int(new_width / 1.333)
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

    im = im.crop(tuple(box))

    final_hight = 110
    image_ratio = float(im.size[0]) / im.size[1]
    final_width = int((image_ratio * final_hight))
    im = im.resize((final_width, final_hight), Image.ANTIALIAS)
    im.save(path, "JPEG",  quality=95)
    return name

def delete_avatar(name):
    upload_dir = UPLOAD_DIR
    if os.path.isfile(upload_dir + name):
        os.remove(upload_dir + name)




