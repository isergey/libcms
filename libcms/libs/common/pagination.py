# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def get_page(request, objects_qs, per_page=20):
    """
    request - объект запроса с параметром
    objects_qs - QuerySet для извлечения объектов
    per_page - количество извлекаемых объектов на страницу
    """
    paginator = Paginator(objects_qs, per_page)
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1

    if page == 0:
        page = 1

    if page > paginator.num_pages:
        page = paginator.num_pages
    try:
        objects = paginator.page(page)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objects = paginator.page(paginator.num_pages)
    return objects