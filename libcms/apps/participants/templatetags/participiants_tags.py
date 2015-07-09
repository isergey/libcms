# -*- coding: utf-8 -*-
import json
from django import template
from .. import models
register = template.Library()


def make_library_dict(library):
    return {
        'id': library.id,
        'code': library.code,
        'name': library.name,
        'postal_address': getattr(library, 'postal_address', u"не указан"),
        'phone': getattr(library, 'phone', u"не указан"),
        'plans': getattr(library, 'plans', u"не указано"),
        'http_service': getattr(library, 'http_service', u"не указан"),
        'latitude': library.latitude,
        'longitude': library.longitude,
        }

@register.inclusion_tag('participants/tags/cbs_list.html')
def cbs_map():
    cbs_list = models.Library.objects.filter(parent=None).order_by('weight')
    js_orgs = []
    for org in cbs_list:
        js_orgs.append(make_library_dict(org))

    js_orgs = json.dumps(js_orgs, encoding='utf-8', ensure_ascii=False)
    return {
        'cbs_list': cbs_list,
        'js_orgs': js_orgs
    }


@register.assignment_tag
def get_user_org(user):
    user_libraies = models.UserLibrary.objects.filter(user=user)[:1]
    if user_libraies:
        return user_libraies[0].library
    else:
        return None


@register.assignment_tag(takes_context=True)
def personal_cabinet_links(context):
    if context.request.user.is_authenticated():
        return models.personal_cabinet_links(context.request)
    return []