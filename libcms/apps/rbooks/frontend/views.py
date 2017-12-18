# -*- coding: utf-8 -*-
import os
import json
import cStringIO
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import translation
from django.contrib.auth.decorators import login_required
from django.utils.translation import to_locale, get_language
from django.shortcuts import HttpResponse, Http404
from django.views.decorators.cache import never_cache
from ssearch.models import  Record, Ebook
from ..models import Bookmarc, in_internal_ip
from forms import BookmarcForm
from libcms.libs.common.xslt_transformers import xslt_bib_draw_transformer


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
        initial = {'gen_id': gen_id, 'book_id': book}

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
    protocol = 'http'
    if request.is_secure():
        protocol = 'https'
    token1 = request.GET.get('token1')
#     xml = """\
# <Document Version="1.0">\
# <Source File="source.xml" URL="%s://%s/dl/%s/draw/?part=Part0.zip&amp;book=%s&amp;version=1285566137"/>\
# <FileURL>http://%s/dl/%s/draw/?part={part}&amp;book=%s</FileURL>\
# <Token1>%s</Token1>\
# <Permissions><AllowCopyToClipboard>true</AllowCopyToClipboard><AllowPrint>true</AllowPrint></Permissions>\
# </Document>""" % (protocol, request.META['HTTP_HOST'],book, book, request.META['HTTP_HOST'], book, book, token1)

    xml = """\
<Document Version="1.0">\
<Source File="source.xml" URL="{protocol}://{host}/dl/{book}/draw/?part=Part0.zip&amp;book={book}&amp;version=1285566137"/>\
<FileURL>{protocol}://{host}/dl/{book}/draw/?part={{part}}&amp;book={book}</FileURL>\
<Token1>{token}</Token1>\
<Permissions><AllowCopyToClipboard>true</AllowCopyToClipboard><AllowPrint>true</AllowPrint></Permissions>\
</Document>""".format(protocol=protocol, host=request.META['HTTP_HOST'],book=book, token=token1)
    zip_file_content = cStringIO.StringIO()

    zip_file = ZipFile(zip_file_content, 'w')
    zip_file.writestr('doc.xml', xml)
    zip_file.close()

    response = HttpResponse(content_type="application/zip")
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

    response = HttpResponse(content_type="application/zip")
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





@login_required
def bookmarcs(request):
    #print list(Bookmarc.objects.raw("SELECT id, gen_id FROM rbooks_bookmarc WHERE user_id=%s GROUP BY gen_id ORDER BY add_date DESC", params=[request.user.id]))
    bookmarcs = Bookmarc.objects.values('id', 'gen_id').filter(user=request.user).order_by('-add_date')
    gen_ids = {}
    for bookmarc in bookmarcs:
        gen_ids[bookmarc.gen_id] = {'bookmarc': bookmarc}


    for record in Record.objects.using('records').filter(gen_id__in=gen_ids.keys()):
        doc_tree = etree.XML(record.content)
        doc_tree = xslt_bib_draw_transformer(doc_tree)
        gen_ids[record.gen_id]['record']= record
        gen_ids[record.gen_id]['bib'] = etree.tostring(doc_tree).replace(u'<b/>', u' '),

    for record in Ebook.objects.using('records').filter(gen_id__in=gen_ids):
        doc_tree = etree.XML(record.content)
        doc_tree = xslt_bib_draw_transformer(doc_tree)
        gen_ids[record.gen_id]['record'] = record
        gen_ids[record.gen_id]['bib'] = etree.tostring(doc_tree).replace(u'<b/>', u' '),

    records = []
    for bookmarc in bookmarcs:
        records.append(gen_ids[bookmarc.gen_id])

    return render(request, 'rbooks/frontend/bookmarcs.html', {
        'records': records
    })

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