# -*- coding: utf-8 -*-
from lxml import etree
import json
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, Http404, redirect, get_object_or_404
from ssearch.models import Record, Ebook
from ..models import SavedDocument, List
from forms import SavedDocumentForm, ListForm
from libcms.libs.common.xslt_transformers import xslt_bib_draw_transformer


@login_required
def index(request):
    q = Q(user=request.user)
    list_id = request.GET.get('list', '')
    list = None
    if list_id:
        try:
            list = List.objects.get(id=list_id)
            q &= Q(list=list)
        except List.DoesNotExist:
            pass
    saved_docs = SavedDocument.objects.filter(q)
    lists = List.objects.filter(user=request.user)

    gen_ids = {}
    for saved_doc in saved_docs:
        gen_ids[saved_doc.gen_id] = {'saved_doc': saved_doc}

    for record in Record.objects.using('records').filter(gen_id__in=gen_ids.keys()):
        doc_tree = etree.XML(record.content)
        doc_tree = xslt_bib_draw_transformer(doc_tree)
        gen_ids[record.gen_id]['record'] = record
        gen_ids[record.gen_id]['bib'] = etree.tostring(doc_tree).replace(u'<b/>', u' '),

    records = []
    for saved_doc in saved_docs:
        records.append(gen_ids[saved_doc.gen_id])

    return render(request, 'mydocs/frontend/index.html', {
        'records': records,
        'lists': lists,
        'list': list,
    })


def save(request):
    if not request.user.is_authenticated():
        return HttpResponse(u'Вы должны быть войти на портал', status=401)
    if request.method == 'POST':
        form = SavedDocumentForm(request.POST)
        if form.is_valid():
            if SavedDocument.objects.filter(user=request.user, gen_id=form.cleaned_data['gen_id']):
                return HttpResponse(u'{"status":"ok"}')
            doc = None
            try:
                doc = Record.objects.using('records').get(gen_id=form.cleaned_data['gen_id'])
            except Record.DoesNotExist:
                raise Http404(u'Record not founded')

            saved_document = form.save(commit=False)
            saved_document.user = request.user
            saved_document.gen_id = doc.gen_id
            saved_document.save()
            if request.is_ajax():
                return HttpResponse(u'{"status":"ok"}')
        else:
            if request.is_ajax():
                response = {
                    'status': 'error',
                    'errors': form.errors
                }
                return HttpResponse(json.dumps(response, ensure_ascii=False))

    else:
        form = SavedDocumentForm()

    return HttpResponse(u'{"status":"ok"}')


@login_required
def delete(request, id):
    get_object_or_404(SavedDocument, id=id, user=request.user).delete()
    if request.is_ajax():
        return HttpResponse(u'{"status":"ok"}')
    return redirect('mydocs:frontend:index')


@login_required
def create_list(request):
    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            list = form.save(commit=False)
            list.user = request.user
            list.save()
            return redirect('mydocs:frontend:index')
    else:
        form = ListForm()

    return render(request, 'mydocs/frontend/list_form.html', {
        'form': form,
    })


@login_required
def change_list(request, id):
    list = get_object_or_404(List, id=id, user=request.user)
    if request.method == 'POST':
        form = ListForm(request.POST, instance=list)
        if form.is_valid():
            form.save()
            return redirect('mydocs:frontend:index')
    else:
        form = ListForm(instance=list)
    return render(request, 'mydocs/frontend/list_form.html', {
        'form': form,
        'list': list,
    })


@login_required
def delete_list(request, id):
    list = get_object_or_404(List, id=id, user=request.user)
    list.delete()
    return redirect('mydocs:frontend:index')
