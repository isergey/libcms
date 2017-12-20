from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.db.transaction import atomic
from django.shortcuts import render, get_object_or_404

from common.pagination import get_page
from ..models import Item, ItemAttachment, ITEM_SECTIONS


def index(request, section):
    q = Q(section=section, published=True)
    items_page = get_page(request, Item.objects.filter(q).order_by('-created'))
    current_section = filter(lambda x: x[0] == section, ITEM_SECTIONS)[0]
    return render(request, 'recommended_reading/frontend/index.html', {
        'items_page': items_page,
        'current_section': current_section,
    })


@login_required
@atomic
@permission_required('recommended_reading.change_item')
def detail(request, id):
    item = get_object_or_404(Item, id=id)
    attachments = ItemAttachment.objects.filter(item=item)
    return render(request, 'recommended_reading/frontend/detail.html', {
        'item': item,
        'attachments': attachments,
    })

