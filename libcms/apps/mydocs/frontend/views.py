# -*- coding: utf-8 -*-
from lxml import etree
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, Http404, redirect, get_object_or_404
from ssearch.models import  Record, Ebook
from ..models import SavedDocument
from forms import SavedDocumentForm
from common.xslt_transformers import xslt_bib_draw_transformer

@login_required
def index(request):
    saved_docs = SavedDocument.objects.filter(user=request.user)
    gen_ids = {}
    for saved_doc in saved_docs:
        gen_ids[saved_doc.gen_id] = {'saved_doc':saved_doc}


    for record in Record.objects.using('records').filter(gen_id__in=gen_ids.keys()):
        doc_tree = etree.XML(record.content)
        doc_tree = xslt_bib_draw_transformer(doc_tree)
        gen_ids[record.gen_id]['record']=record
        gen_ids[record.gen_id]['bib']=etree.tostring(doc_tree).replace(u'<b/>', u' '),


    records = []
    for saved_doc in saved_docs:
        records.append(gen_ids[saved_doc.gen_id])

    return render(request, 'mydocs/frontend/index.html', {
        'records': records
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
    get_object_or_404(SavedDocument, id=id, user = request.user).delete()
    if request.is_ajax():
        return HttpResponse(u'{"status":"ok"}')
    return redirect('mydocs:frontend:index')