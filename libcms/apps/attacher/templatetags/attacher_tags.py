# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django import template

from ..frontend.views import get_dir_for_object, get_media_url_for_file, get_sign_delete_path
register = template.Library()
@register.inclusion_tag('attacher/tags/attach_list.html')
def attach_list(content_type, content_id):

    files = []
    if content_type and content_id:
        attaches_dir_path = get_dir_for_object(content_type, content_id)
        if os.path.isdir(attaches_dir_path):
            for file_name in os.listdir(attaches_dir_path):
                files.append({
                    'url': get_media_url_for_file(content_type, content_id, file_name),
                    'title': u'_'.join(file_name.split('_')[1:]), # remove prefix unique id in file name
                    'sign_delete_path': get_sign_delete_path(file_name),
                    'path': file_name
                })
    return ({
        'files': files,
        'content_type': content_type,
        'content_id': content_id,
        'STATIC_URL': settings.STATIC_URL
    })

