# -*- coding: utf-8 -*-
import json
from django.shortcuts import resolve_url
from django.core.cache import cache
from django.core import serializers

json_serializer = serializers.get_serializer("json")()
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
    return render(request, 'participants/frontend/cbs_list.html', {
        'cbs_list': cbs_list,
        'js_orgs': js_orgs
    })


def branches(request, code=None):
    if request.method == "POST":
        code = request.POST.get('code', None)
    library = None
    if code:
        library = get_object_or_404(Library, code=code)
    libraries = Library.objects.filter(parent=library).order_by('weight')

    js_orgs = []
    for org in libraries:
        js_orgs.append(make_library_dict(org))

    js_orgs = json.dumps(js_orgs, encoding='utf-8', ensure_ascii=False)

    if request.is_ajax():
        return HttpResponse(js_orgs)

    return render(request, 'participants/frontend/branch_list.html', {
        'library': library,
        'libraries': libraries,
        'js_orgs': js_orgs
    })


def detail(request, code):
    library = get_object_or_404(Library, code=code)
    js_orgs = []
    js_orgs.append(make_library_dict(library))

    js_orgs = json.dumps(js_orgs, encoding='utf-8', ensure_ascii=False)

    return render(request, 'participants/frontend/detail.html', {
        'library': library,
        'js_orgs': js_orgs
    })


def geosearch(request):
    return render(request, 'participants/frontend/geosearch.html')


def geo_nearest(request):
    page = int(request.GET.get('page', 1))
    lat = float(request.GET.get('lat', 0))
    lon = float(request.GET.get('lon', 0))
    fields = ('id', 'code', 'name', 'latitude', 'longitude', 'postal_address')
    cache_key = 'geo_libs'
    cached_libraies = cache.get(cache_key)

    if not cached_libraies:
        libraries = list(Library.objects.all().exclude(parent=None).values(*fields))
        cached_libraies = json.dumps(libraries).encode('zlib')
        cache.set(cache_key, cached_libraies, timeout=60)

    libraries = json.loads(cached_libraies.decode('zlib'))

    # print len(json.dumps(libraries, ensure_ascii=False).encode('utf-8').encode('zlib'))
    geo_libraries = []
    for library in libraries:
        latitude = library.get('latitude', 0)
        longitude = library.get('longitude', 0)
        if not latitude or not longitude:
            continue
        geo_libraries.append({
            'library': library,
            'distance': geodistance(lat, lon, longitude, latitude),
            'href': resolve_url('participants:frontend:detail', code=library.get('code'))
        })

    geo_libraries = sorted(geo_libraries, key=lambda item: item.get('distance'))

    per_page = 10
    # objects_page = get_page(request, geo_libraries, per_page)
    offset = (page - 1) * per_page

    result = {
        'page': page,
        'per_page': per_page,
        'count': len(geo_libraries),
        'object_list': geo_libraries[offset:per_page],

    }
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')
    #
    # return render(request, 'participants/frontend/nearest_results.html', {
    #     'objects': objects_page.paginator.object_list[offset::per_page]
    # })


from math import radians, sqrt, sin, cos, atan2


def geodistance(lat1, lon1, lat2, lon2):
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon1 - lon2

    EARTH_R = 6372.8

    y = sqrt(
        (cos(lat2) * sin(dlon)) ** 2
        + (cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)) ** 2
    )
    x = sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(dlon)
    c = atan2(y, x)
    return EARTH_R * c

    #print geocalc(60.038349, 30.405864, 55.779945, 49.116242)