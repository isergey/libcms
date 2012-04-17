# -*- coding: utf-8 -*-
from django import template
register = template.Library()
from mydocs.frontend.forms import SavedDocumentForm
from ..models import SavedDocument

@register.inclusion_tag('mydocs/tags/drow_save_doc.html')
def drow_save_doc(user, gen_id):
    already_saved = False
    if SavedDocument.objects.filter(gen_id=gen_id, user=user).count():
        already_saved = True

    form = SavedDocumentForm(initial={
        'gen_id': gen_id
    })
    return {
        'form': form,
        'already_saved': already_saved,
    }