# -*- coding: utf-8 -*-
from datetime import datetime
from django.conf import settings
from django import template
from ..models import Banner

register = template.Library()
@register.inclusion_tag('participant_banners/tags/show_banners.html')
def show_banners(library_id=None):
    now = datetime.now()
    banners = list(Banner.objects.filter(start_date__lte=now, end_date__gte=now, global_banner=True, active=True))

    if library_id:
        library_banners = list(Banner.objects.filter(start_date__lte=now, end_date__gte=now, active=True, libraries__id=library_id))
        banners += library_banners

    return ({
        'banners': banners,
        'MEDIA_URL': settings.MEDIA_URL
    })

