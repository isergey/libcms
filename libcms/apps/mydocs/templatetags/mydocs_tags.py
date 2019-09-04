# -*- coding: utf-8 -*-
from django import template
from mydocs.frontend.forms import get_saved_document_form
from ..models import SavedDocument

register = template.Library()


@register.inclusion_tag('mydocs/tags/drow_save_doc.html')
def drow_save_doc(user, gen_id):
    already_saved = False
    if user.id and SavedDocument.objects.filter(gen_id=str(gen_id), user=user).count():
        already_saved = True
    form = get_saved_document_form(user)(initial={
        'gen_id': gen_id
    })
    return {
        'form': form,
        'already_saved': already_saved,
        'gen_id': gen_id,
        'user': user
    }
