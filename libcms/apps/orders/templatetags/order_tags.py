# -*- coding: utf-8 -*-
import hashlib
from django import template
register = template.Library()
from participants.models import Library
from zgate.models import ZCatalog
from django.core.cache import cache
from ..frontend.forms import DeliveryOrderForm, CopyOrderForm
@register.simple_tag
def org_by_id(org_id):
    hash_id = hashlib.md5(org_id.encode('utf-8')).hexdigest()
    org_info = cache.get(hash_id, None)
    if org_info:
        return org_info


    org_info = {
        'code':'',
        'name':'',
        'type':''
    }

    try:
        library = Library.objects.get(code=org_id)
        org_info['code'] = library.code
        org_info['name'] = library.name
        if library.is_root_node():
            org_info['type'] = 'library_system'
        else:
            org_info['type'] = 'library'
    except Library.DoesNotExist:
        org_info = {
            'code':org_id,
            'name':org_id,
            'type':None
        }
    cache.set(hash_id, org_info)
    return org_info




@register.inclusion_tag('orders/tags/drow_el_order_menu.html')
def drow_el_order_menu(owners_codes, record_id):
    """
    Тег отрисовки меню для заказа в электронном каталоге держателя
    Необходимо чтобы в системе был зарегистрирован экземпляр АРМ Читателя (zgate.catalog) сo slug в виде сиглы держателя

    owners_codes - список сигл держателей
    record_id - идентификатор записи, которую необходимо заказать
    """


    owners_dict = {}
    empty_codes = [] # Сиглы, которые указаны в записе но не зарегистрированны в системе
    owners = list(Library.objects.filter(code__in=owners_codes).values('id','name','code'))

    for owner in owners:
        owners_dict[owner['code']] = {
            'owner': owner,
            'has_catalog': False
        }

    # ищем zgate для каждого держателя, чтобы можно было сделать зазказ
    zcatalogs = ZCatalog.objects.filter(latin_title__in=owners_dict.keys()).values('latin_title')

    for zcatalog in zcatalogs:
        # в latin_title хранится сигла держателя
        if zcatalog['latin_title'] in owners_dict:
            owners_dict[zcatalog['latin_title']]['has_catalog'] = True


    for owner_code in owners_codes:
        if owner_code not in owners_dict:
            empty_codes.append(owner_code)

    owners = owners_dict.values()
    return {
        'owners': owners,
        'record_id': record_id,
        'empty_codes': empty_codes,
    }


@register.inclusion_tag('orders/tags/drow_mba_order_menu.html')
def drow_mba_order_menu(user, gen_id):
    """
    Тег отрисовки меню для заказа в мба
    """
    delivery_form = DeliveryOrderForm(prefix='delivery', initial={
        'gen_id':gen_id
    })
    copy_form = CopyOrderForm(prefix='copy', initial={
        'gen_id':gen_id
    })

    return {
        'gen_id': gen_id,
        'user': user,
        'delivery_form': delivery_form,
        'copy_form': copy_form,
    }