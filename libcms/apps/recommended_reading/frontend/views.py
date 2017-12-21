from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from common.pagination import get_page
from ..models import Item, ItemAttachment, ITEM_SECTIONS, ITEM_SCHOOL_CLASSES


def index(request, section):
    school_class = request.GET.get('school_class')

    q = Q(section=section, published=True)
    if school_class:
        q &= Q(school_class=int(school_class))
    items_page = get_page(request, Item.objects.filter(q).order_by('-created'))
    current_section = filter(lambda x: x[0] == section, ITEM_SECTIONS)[0]
    return render(request, 'recommended_reading/frontend/index.html', {
        'items_page': items_page,
        'current_section': current_section,
        'school_classes': ITEM_SCHOOL_CLASSES
    })


def detail(request, id):
    item = get_object_or_404(Item, id=id)
    attachments = ItemAttachment.objects.filter(item=item)
    return render(request, 'recommended_reading/frontend/detail.html', {
        'item': item,
        'attachments': attachments,
    })

