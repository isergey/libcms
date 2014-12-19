# -*- coding: utf-8 -*-
from django import template
from ..models import  Album, AlbumImage
register = template.Library()

@register.inclusion_tag('gallery/tags/gallery_slider.html')
def gallery_slider():
    gallery_name = 'newsday'
    album = None
    album_images = []
    try:
        album = Album.objects.get(slug=gallery_name)
        album_images = AlbumImage.objects.filter(album=album)
    except Album.DoesNotExist:
        pass

    return {
        'album': album,
        'album_images': album_images,
        'gallery_name': gallery_name
    }

@register.inclusion_tag('gallery/tags/gallery_carusel.html')
def gallery_carusel():
    album = None
    album_images = []
    try:
        album = Album.objects.get(slug='carousel')
        album_images = AlbumImage.objects.filter(album=album)
    except Album.DoesNotExist:
        pass

    return {
        'album':album,
        'album_images': album_images,
    }