from lxml import etree
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from ..transformers import transformers
from . import forms

@login_required
@user_passes_test(lambda user: user.is_superuser or user.is_staff)
def index(request):
    return render(request, 'transformers_pool/administration/index.html')


@login_required
@user_passes_test(lambda user: user.is_superuser or user.is_staff)
def xslt(request):
    transform_result = ''
    transform_result_pretty = ''
    if request.method == 'POST':
        form = forms.TransformForm(request.POST)
        if form.is_valid():
            tansformer = transformers.get(form.cleaned_data['transformer'])
            record_tree = etree.fromstring(form.cleaned_data['xml'].encode('utf-8'))
            transformed = tansformer(record_tree, abstract='0')
            transform_result = unicode(transformed)
            transform_result_pretty = etree.tounicode(transformed, pretty_print=True)
    else:
        form = forms.TransformForm()
    return render(request, 'transformers_pool/administration/xslt.html', {
        'form': form,
        'transform_result': transform_result,
        'transform_result_pretty': transform_result_pretty
    })