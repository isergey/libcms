# -*- coding: utf-8 -*-

import cStringIO
from zipfile import ZipFile, ZIP_DEFLATED
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import translation
from django.utils.translation import to_locale, get_language
from django.shortcuts import HttpResponse, Http404
from django.views.decorators.cache import never_cache
from pages.models import Page, Content


def index(request):
    cur_language = translation.get_language()
    page = get_object_or_404(Page, slug='index')
    try:
        content = Content.objects.get(page=page, lang=cur_language[:2])
    except Content.DoesNotExist:
        content = None

    return render(request, 'pages/frontend/show.html', {
        'page': page,
        'content': content
    })
@never_cache
def show(request):
    book = request.GET.get('book')
    cur_language = translation.get_language()
    print cur_language
#    page = get_object_or_404(Page, slug=slug)
#    try:
#        content = Content.objects.get(page=page, lang=cur_language[:2])
#    except Content.DoesNotExist:
#        content = None

    return render(request, 'rbooks/frontend/show.html', {
        'file_name': book,
    })
@never_cache
def book(request):
    book = request.GET.get('book')
    token1 = request.GET.get('token1')
    xml = """\
<Document Version="1.0">\
<Source File="source.xml" URL="http://%s/ru/rbooks/draw/?part=Part0.zip&amp;book=%s&amp;version=1285566137"/>\
<FileURL>http://%s/ru/rbooks/draw/?part={part}&amp;book=%s</FileURL>\
<Token1>%s</Token1>\
<Permissions><AllowCopyToClipboard>true</AllowCopyToClipboard><AllowPrint>true</AllowPrint></Permissions>\
</Document>""" % (request.META['HTTP_HOST'], book, request.META['HTTP_HOST'], book, token1)

    zip_file_content = cStringIO.StringIO()

    zip_file = ZipFile(zip_file_content, 'w')
    zip_file.writestr('doc.xml', xml)
    zip_file.close()

    response = HttpResponse(mimetype="application/zip")
    response["Content-Disposition"] = "attachment; filename=%s.zip" % book
    zip_file_content.seek(0)
    response.write(zip_file_content.read())

    return response


@never_cache
def draw(request):
    book = request.GET.get('book')
    part = request.GET.get('part')
    try:
        zf = ZipFile('/home/sergey/PycharmProjects/libcms/libcms/apps/rbooks/static/rbooks/books/' + book +'.edoc')
    except Exception:
        raise Http404(u'Book not founded')

    response = HttpResponse(mimetype="application/zip")
    response["Content-Disposition"] = "attachment; filename=%s" % part
    response.write(zf.read(part))

    return response