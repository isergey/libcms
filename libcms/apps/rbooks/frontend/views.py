# -*- coding: utf-8 -*-
import os
import json
import cStringIO
from zipfile import ZipFile, ZIP_DEFLATED
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import translation
from django.utils.translation import to_locale, get_language
from django.shortcuts import HttpResponse, Http404
from django.views.decorators.cache import never_cache
from ssearch.models import  Record, Ebook
from ..models import Bookmarc, in_internal_ip
from forms import BookmarcForm
class AccessDenied(Exception): pass

# def add_to_bookmarc(request):
#     if not request.user.is_authenticated():
#         return HttpResponse(u'Вы должны быть войти на портал', status=401)
#     if request.method == 'POST':


@never_cache
def show(request, book):
    try:
        book_path = get_book_path(book, request.META.get('REMOTE_ADDR', '0.0.0.0'))
    except AccessDenied as e:
        return HttpResponse(e.message + u' Ваш ip адрес: ' + request.META.get('REMOTE_ADDR', '0.0.0.0'))
    if not book_path:
        raise Http404(u'Книга не найдена')

    cur_language = translation.get_language()
    locale_titles = {
        'ru': 'ru_RU',
        'en': 'en_US',
        'tt': 'tt_RU'
    }

    locale_chain = locale_titles.get(cur_language, 'en_US')
    gen_id = request.GET.get('gen_id', None)
    initial = None
    if gen_id:
        initial={'gen_id': gen_id}
    bookmarc_form = BookmarcForm(initial)
    return render(request, 'rbooks/frontend/show.html', {
        'file_name': book,
        'locale_chain': locale_chain,
        'bookmarc_form': bookmarc_form
    })
@never_cache
def book(request, book):
    try:
        book_path = get_book_path(book, request.META.get('REMOTE_ADDR', '0.0.0.0'))
    except AccessDenied as e:
        return HttpResponse(e.message + u' Ваш ip адрес: ' + request.META.get('REMOTE_ADDR', '0.0.0.0'))
    if not book_path:
        raise Http404(u'Книга не найдена')
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
    part = request.GET.get('part')

    try:
        book_path = get_book_path(book, request.META.get('REMOTE_ADDR', '0.0.0.0'))
    except AccessDenied as e:
        return HttpResponse(e.message)


    if not book_path:
        raise Http404(u'Книга не найдена')
    zf = ZipFile(book_path)

    response = HttpResponse(mimetype="application/zip")
    response["Content-Disposition"] = "attachment; filename=%s" % part
    response.write(zf.read(part))

    return response



def add_page_bookmarc(request):
    if not request.user.is_authenticated():
        return HttpResponse(u'Вы должны быть войти на портал', status=401)
    if request.method == 'POST':
        form = BookmarcForm(request.POST)
        if form.is_valid():
            if Bookmarc.objects.filter(user=request.user, gen_id=form.cleaned_data['gen_id']):
                return HttpResponse(u'{"status":"ok"}')
            doc = None
            try:
                doc = Record.objects.using('records').get(gen_id=form.cleaned_data['gen_id'])
            except Record.DoesNotExist:
                pass
            if not doc:
                try:
                    doc = Ebook.objects.using('records').get(gen_id=form.cleaned_data['gen_id'])
                except Ebook.DoesNotExist:
                    raise Http404(u'Record not founded')

            saved_bookmarc = form.save(commit=False)
            saved_bookmarc.user = request.user
            saved_bookmarc.gen_id = doc.gen_id
            saved_bookmarc.save()
            if request.is_ajax():
                return HttpResponse(u'{"status":"ok"}')
        else:
            if request.is_ajax():
                response = {
                    'status': 'error',
                    'errors': form.errors
                }
                return HttpResponse(json.dumps(response, ensure_ascii=False))



    return HttpResponse(u'{"status":"ok"}')


def get_book_path(book, remote_addr):
    internal_ip = cache.get('internal_ip' + remote_addr, None)
    if internal_ip == None:
        internal_ip = in_internal_ip(remote_addr)
        cache.set('internal_ip' + remote_addr, internal_ip)

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
        raise AccessDenied(u'Просмотр с вашего ip ареса запрещен.')



    if not book_path:
        return None

    return book_path