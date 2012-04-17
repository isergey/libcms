# -*- coding: utf-8 -*-
import simplejson
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, Http404, redirect
from ssearch.models import  Record, Ebook
from ..models import SavedDocument
from forms import SavedDocumentForm

@login_required
def index(request):
    records = []
#    records =  list(Ebook.objects.using('records').filter(gen_id__in=doc_ids))
#    records +=  list(Record.objects.using('records').filter(gen_id__in=doc_ids))
    return HttpResponse(u'Ok')




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
                pass
            if not doc:
                try:
                    doc = Ebook.objects.using('records').get(record_id=form.cleaned_data['gen_id'])
                except Ebook.DoesNotExist:
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
                return HttpResponse(simplejson.dumps(response, ensure_ascii=False))

    else:
        form = SavedDocumentForm()

    return HttpResponse(u'{"status":"ok"}')
