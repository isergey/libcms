# -*- coding: utf-8 -*-
import json
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, Http404
from django.utils import translation
from django.utils.translation import get_language
from common.pagination import get_page
from ..models import Library, District

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


def index(request):
    cbs_list = Library.objects.filter(parent=None).order_by('weight')
    js_orgs = []
    for org in cbs_list:
        js_orgs.append(make_library_dict(org))

    js_orgs = json.dumps(js_orgs, encoding='utf-8', ensure_ascii=False)
    return render(request, 'participants/frontend/cbs_list.html',{
        'cbs_list': cbs_list,
        'js_orgs': js_orgs
    })


def branches(request, code=None):
    if request.method == "POST":
        code = request.POST.get('code', None)
    library=None
    if code:
        library = get_object_or_404(Library, code=code)
    libraries = Library.objects.filter(parent=library).order_by('weight')

    js_orgs = []
    for org in libraries:
        js_orgs.append(make_library_dict(org))

    js_orgs = json.dumps(js_orgs, encoding='utf-8', ensure_ascii=False)

    if request.is_ajax():
        return HttpResponse(js_orgs)

    return render(request, 'participants/frontend/branch_list.html',{
        'library': library,
        'libraries': libraries,
        'js_orgs': js_orgs
    })


def detail(request, code):
    library = get_object_or_404(Library, code=code)
    js_orgs = []
    js_orgs.append(make_library_dict(library))

    js_orgs = json.dumps(js_orgs, encoding='utf-8', ensure_ascii=False)

    return render(request, 'participants/frontend/detail.html',{
        'library': library,
        'js_orgs': js_orgs
    })
