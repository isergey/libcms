# -*- coding: utf-8 -*-
from django.conf import settings
from django import template
from ..models import LibraryAvatar

MEDIA_URL = settings.MEDIA_URL

register = template.Library()


@register.assignment_tag
def get_library_avatar_src(library_id):
    try:
        library_avatar = LibraryAvatar.objects.get(library_id=library_id)
        print(library_avatar.avatar)
        return unicode(library_avatar.avatar)
    except LibraryAvatar.DoesNotExist:
        return None
