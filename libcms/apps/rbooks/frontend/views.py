# -*- coding: utf-8 -*-
import os, sys
import cStringIO
from zipfile import ZipFile, ZIP_DEFLATED
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import translation
from django.utils.translation import to_locale, get_language
from django.shortcuts import HttpResponse, Http404
from django.views.decorators.cache import never_cache
from ..models import in_internal_ip


@never_cache
def show(request, book):
#    book = request.GET.get('book')
    cur_language = translation.get_language()
    locale_titles = {
        'ru': 'ru_RU',
        'en': 'en_US',
        'tt': 'tt_RU'
    }

    locale_chain = locale_titles.get(cur_language, 'en_US')
    return render(request, 'rbooks/frontend/show.html', {
        'file_name': book,
        'locale_chain': locale_chain
    })
@never_cache
def book(request, book):

#    book = request.GET.get('book')
    token1 = request.GET.get('token1')
    xml = """\
<Document Version="1.0">\
<Source File="source.xml" URL="http://%s/dl/%s/draw/?part=Part0.zip&amp;book=%s&amp;version=1285566137"/>\
<FileURL>http://%s/dl/%s/draw/?part={part}&amp;book=%s</FileURL>\
<Token1>%s</Token1>\
<Permissions><AllowCopyToClipboard>true</AllowCopyToClipboard><AllowPrint>true</AllowPrint></Permissions>\
</Document>""" % (request.META['HTTP_HOST'],book, book, request.META['HTTP_HOST'], book, book, token1)

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
def draw(request, book):
    REMOTE_ADDR = request.META.get('REMOTE_ADDR', '0.0.0.0')
    internal_ip = cache.get('internal_ip' + REMOTE_ADDR, None)
    if internal_ip == None:
        internal_ip = in_internal_ip(REMOTE_ADDR)
        cache.set('internal_ip' + REMOTE_ADDR, internal_ip)

    part = request.GET.get('part')

    book_path_internet = None
    book_path_internal = None

    book_path = None

    internet_books = (
        settings.RBOOKS.get('dl_path') + book +'.1.edoc',
        settings.RBOOKS.get('dl_path') + book +'.edoc',
        )
    iternal_books = (
        settings.RBOOKS.get('dl_path') + book +'.2.edoc',
    ) + internet_books

    if not internal_ip:
        for internet_book in internet_books:
            if os.path.isfile(internet_book):
                book_path_internet =  internet_book
                break

        if  book_path_internet:
            book_path = book_path_internet
    else:
        for iternal_book in iternal_books:
            if os.path.isfile(iternal_book):
                book_path_internal =  iternal_book
                break

        if book_path_internal:
            book_path = book_path_internal

    if not book_path_internal and not book_path_internet:
        raise Http404(u'Book not founded')



    if not book_path:
        raise Http404(u'Book not founded for your network')

    zf = ZipFile(book_path)

    response = HttpResponse(mimetype="application/zip")
    response["Content-Disposition"] = "attachment; filename=%s" % part
    response.write(zf.read(part))

    return response