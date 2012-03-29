# -*- coding: utf-8 -*-
import simplejson
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.utils import translation
from django.utils.translation import get_language
from common.pagination import get_page
from participants.models import Library, District

def make_library_dict(library):
    return {
        'code': library.code,
        'name': library.name,
        'postal_address': getattr(library, 'postal_address', u"не указан"),
        'phone': getattr(library, 'phone', u"не указан"),
        'plans': getattr(library, 'plans', u"не указано"),
        'http_service': getattr(library, 'http_service', u"не указан"),
        'latitude': library.latitude,
        'longitude': library.longitude,
        }


def index(request):
    cbs_list = Library.objects.filter(parent=None).order_by('weight')
    return render(request, 'participants/frontend/cbs_list.html',{
        'cbs_list': cbs_list
    })


def branches(request, id):
    library = get_object_or_404(Library, id=id)
    libraries = Library.objects.filter(parent=library).order_by('weight')

    js_orgs = []
    for org in libraries:
        js_orgs.append(make_library_dict(org))

    js_orgs = simplejson.dumps(js_orgs, encoding='utf-8', ensure_ascii=False)

    return render(request, 'participants/frontend/branch_list.html',{
        'library': library,
        'libraries': libraries,
        'js_orgs': js_orgs
    })


def detail(request, id):
    library = get_object_or_404(Library, id=id)
    js_orgs = []
    js_orgs.append(make_library_dict(library))

    js_orgs = simplejson.dumps(js_orgs, encoding='utf-8', ensure_ascii=False)

    return render(request, 'participants/frontend/detail.html',{
        'library': library,
        'js_orgs': js_orgs
    })
