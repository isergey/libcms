# -*- encoding: utf-8 -*-
from django.shortcuts import render, get_object_or_404

from ..models import Album, AlbumImage



def index(request):
    albums = Album.objects.filter(public=True)
    return render(request, 'gallery/frontend/albums_list.html', {
        'albums': albums
    })


def album_view(request, id):

    album = get_object_or_404(Album, id=id)
    album_images = AlbumImage.objects.filter(album=album).order_by('order')

    return render(request, 'gallery/frontend/album_view.html', {
        'album': album,
        'album_images': album_images,
    })

