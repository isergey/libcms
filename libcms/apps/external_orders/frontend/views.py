# coding=utf-8
from lxml import etree
from django.shortcuts import HttpResponse, get_object_or_404, Http404, render

from participants.models import Library
from ssearch.rusmarc_template import beautify
from ssearch.models import get_records
from ssearch.frontend.views import xslt_bib_draw_transformer

from . import forms

def index(request):
    return HttpResponse(u'Ok')


def order(request, org_code, record_gen_id):
    library = get_object_or_404(Library, code=org_code)
    records = get_bib_records([record_gen_id])
    if not records:
        raise Http404(u'Запись не найдена')

    if request.method == 'POST':
        form = forms.OrderForm(request.POST)
    else:
        form = forms.OrderForm()

    return render(request, 'external_orders/frontend/order.html', {
        'form': form,
        'library': library,
        'record': records[0]
    })


def get_bib_records(gen_ids):
    records = get_records(gen_ids)
    bib_records = []
    for record in records:
        doc_tree = etree.XML(record.content)
        bib_tree = xslt_bib_draw_transformer(doc_tree)
        bib_dump = etree.tostring(bib_tree, encoding='utf-8')
        bib_records.append({
            'record': record,
            'card': beautify(bib_dump.replace('<b/>', '')),
        })

    return bib_records