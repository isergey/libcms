from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.db.transaction import atomic
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from common.pagination import get_page
from . import forms
from ..models import Item, ItemAttachment, ITEM_SECTIONS


@login_required
@atomic
def index(request):
    if not request.user.has_module_perms('recommended_reading'):
        return HttpResponseForbidden()
    return redirect('recommended_reading:administration:items')


@login_required
@atomic
@permission_required('recommended_reading.change_item')
def items(request):
    section = request.GET.get('section')
    q = Q()
    if section:
        q &= Q(section=section)
    items_page = get_page(request, Item.objects.filter(q).order_by('-created'))
    return render(request, 'recommended_reading/administration/items.html', {
        'items_page': items_page,
        'sections': ITEM_SECTIONS,
        'current_section': section,
    })


@login_required
@atomic
@permission_required('recommended_reading.change_item')
def detail(request, id):
    item = get_object_or_404(Item, id=id)
    attachments = ItemAttachment.objects.filter(item=item)
    return render(request, 'recommended_reading/administration/detail.html', {
        'item': item,
        'attachments': attachments,
    })


@login_required
@atomic
@permission_required('recommended_reading.add_item')
def create_item(request):
    if request.method == 'POST':
        item_form = forms.ItemForm(request.POST, request.FILES, prefix='item_form')
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.save()
            return redirect('recommended_reading:administration:detail', id=item.id)
    else:
        item_form = forms.ItemForm(prefix='item_form')

    return render(request, 'recommended_reading/administration/item_form.html', {
        'item_form': item_form,
    })


@login_required
@atomic
@permission_required('recommended_reading.change_item')
def change_item(request, id):
    item = get_object_or_404(Item, id=id)
    if request.method == 'POST':
        item_form = forms.ItemForm(request.POST, request.FILES, prefix='item_form', instance=item)
        if item_form.is_valid():
            item.save()
            return redirect('recommended_reading:administration:detail', id=item.id)
    else:
        item_form = forms.ItemForm(prefix='item_form', instance=item)

    return render(request, 'recommended_reading/administration/item_form.html', {
        'item_form': item_form,
        'item': item,
    })


@login_required
@atomic
@permission_required('recommended_reading.delete_item')
def delete_item(request, id):
    item = get_object_or_404(Item, id=id)
    item.delete()
    return redirect('recommended_reading:administration:items')


@login_required
@atomic
@permission_required('recommended_reading.add_itemattachment')
def upload_attachment(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        attachment_form = forms.AttachmentForm(request.POST, request.FILES, prefix='attachment_form')
        if attachment_form.is_valid():
            attachment = attachment_form.save(commit=False)
            attachment.item = item
            attachment.save()
            return redirect('recommended_reading:administration:detail', id=item.id)
    else:
        attachment_form = forms.AttachmentForm(prefix='attachment_form')

    return render(request, 'recommended_reading/administration/attachment_form.html', {
        'attachment_form': attachment_form,
        'item': item,
    })


@login_required
@atomic
@permission_required('recommended_reading.delete_item')
def delete_attachment(request, item_id, id):
    attachment = get_object_or_404(ItemAttachment, id=id, item_id=item_id)
    attachment.delete()
    return redirect('recommended_reading:administration:detail', id=attachment.item_id)