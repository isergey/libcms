# -*- encoding: utf-8 -*-
from PIL import Image
import uuid
import os
from datetime import datetime
from django.db import transaction
from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required
from ..models import Album, AlbumImage
from forms import AlbumForm, AlbumImageForm, AlbumImageEditForm
from django.views.decorators.csrf import csrf_exempt


def index(request):
    if not request.user.has_module_perms('gallery'):
        return HttpResponseForbidden()
    return redirect('gallery:administration:albums_list')


@login_required
def albums_list(request):
    albums = Album.objects.all()
    return render(request, 'gallery/administration/albums_list.html', {
        'albums': albums
    })


@login_required
@permission_required_or_403('gallery.add_album')
def album_create(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            if 'album_form_avatar' in request.FILES:
                avatar_img_name = handle_uploaded_file(request.FILES['album_form_avatar'])
                album.avatar_img_name = avatar_img_name

            if not request.user.has_perm('gallery.public_album'):
                album.public = False
            album.save()
            return redirect('gallery:administration:albums_list')
    else:
        form = AlbumForm()

    return render(request, 'gallery/administration/album_create.html', {
        'form': form
    })


@login_required
@permission_required_or_403('gallery.change_album')
def album_edit(request, id):
    album = get_object_or_404(Album, id=id)
    if request.method == 'POST':
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            album = form.save(commit=False)
            if 'album_form_avatar' in request.FILES:
                if album.avatar_img_name:
                    handle_uploaded_file(request.FILES['album_form_avatar'], album.avatar_img_name)
                else:
                    avatar_img_name = handle_uploaded_file(request.FILES['album_form_avatar'])
                    album.avatar_img_name = avatar_img_name

            if not request.user.has_perm('gallery.public_album'):
                album.public = False
            album.save()
            return redirect('gallery:administration:albums_list')
    else:
        form = AlbumForm(instance=album)

    return render(request, 'gallery/administration/album_edit.html', {
        'form': form
    })


@login_required
@permission_required_or_403('gallery.delete_album')
def album_delete(request, id):
    album = get_object_or_404(Album, id=id)
    album.delete()
    delete_avatar(album.avatar_img_name)
    return redirect('gallery:administration:albums_list')


def album_view(request, id):
    if not request.user.has_module_perms('gallery'):
        return HttpResponseForbidden()

    album = get_object_or_404(Album, id=id)
    album_images = AlbumImage.objects.filter(album=album).order_by('order')

    return render(request, 'gallery/administration/album_view.html', {
        'album': album,
        'album_images': album_images,
    })


@transaction.atomic
@csrf_exempt
def album_upload(request, id):
    if request.user.is_authenticated():
        user = request.user
    elif request.method == 'POST':
        user = user_from_session_key(request.POST.get('sessionid', 0))

    if not user.is_authenticated():
        return HttpResponseForbidden()

    if not user.has_perm('gallery.add_album'):
        return HttpResponseForbidden()

    album = get_object_or_404(Album, id=id)
    if request.method == 'POST':
        form = AlbumImageForm(request.POST, request.FILES)
        if form.is_valid():
            order = AlbumImage.objects.all().count()
            album_image = form.save(commit=False)
            album_image.album = album
            album_image.order = order
            album_image.save()
            return HttpResponse('True')
    else:
        form = AlbumImageForm()
    return render(request, 'gallery/administration/album_upload.html', {
        'album': album,
        'form': form,
    })


@login_required
@permission_required_or_403('gallery.change_album')
@transaction.atomic
def image_edit(request, id):
    album_image = get_object_or_404(AlbumImage, id=id)
    if request.method == 'POST':
        form = AlbumImageEditForm(request.POST, instance=album_image)
        if form.is_valid():
            form.save()
            return redirect('gallery:administration:album_view', id=album_image.album_id)
    else:
        form = AlbumImageEditForm(instance=album_image)

    return render(request, 'gallery/administration/image_edit.html', {
        'form': form,
        'album_image': album_image
    })


@login_required
@permission_required_or_403('gallery.delete_album')
@transaction.atomic
def image_delete(request, id):
    image = get_object_or_404(AlbumImage, id=id)
    image.delete()
    return redirect('gallery:administration:album_view', id=image.album_id)


def image_up(request, id):
    image = get_object_or_404(AlbumImage, id=id)
    image.up()
    return redirect('gallery:administration:album_view', id=image.album_id)


def image_down(request, id):
    image = get_object_or_404(AlbumImage, id=id)
    image.down()
    return redirect('gallery:administration:album_view', id=image.album_id)


def image_to_begin(request, id):
    image = get_object_or_404(AlbumImage, id=id)
    image.to_begin()
    return redirect('gallery:administration:album_view', id=image.album_id)


def image_to_end(request, id):
    image = get_object_or_404(AlbumImage, id=id)
    image.to_end()
    return redirect('gallery:administration:album_view', id=image.album_id)


from django.conf import settings
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, load_backend
from django.contrib.auth.models import AnonymousUser


def user_from_session_key(session_key):
    session_engine = __import__(settings.SESSION_ENGINE, {}, {}, [''])
    session_wrapper = session_engine.SessionStore(session_key)
    session = session_wrapper.load()
    user_id = session.get(SESSION_KEY)
    backend_id = session.get(BACKEND_SESSION_KEY)
    if user_id and backend_id:
        auth_backend = load_backend(backend_id)
        user = auth_backend.get_user(user_id)
        if user:
            return user
    return AnonymousUser()


def handle_uploaded_file(f, old_name=None):
    upload_dir = settings.MEDIA_ROOT + 'uploads/galleryavatars/'
    now = datetime.now()
    dirs = [
        upload_dir,
        upload_dir + str(now.year) + '/',
        upload_dir + str(now.year) + '/' + str(now.month) + '/',
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
    im.save(path, "JPEG", quality=95)
    return name


def delete_avatar(name):
    upload_dir = settings.MEDIA_ROOT + 'uploads/galleryavatars/'
    if os.path.isfile(upload_dir + name):
        os.remove(upload_dir + name)