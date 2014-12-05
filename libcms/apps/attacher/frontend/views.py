# encoding: utf-8
import shutil
import json
import uuid
from datetime import datetime
import os
import hashlib
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, render
from django.views.decorators.csrf import csrf_exempt


ATTACH_PREFIX = 'attaches/'
TMP_PREFIX = 'tmp/'

ATTACH_BASE_PATH = settings.MEDIA_ROOT + ATTACH_PREFIX
ATTACH_TMP_PATH = ATTACH_BASE_PATH + TMP_PREFIX

ATTACH_BASE_URL = settings.MEDIA_URL + ATTACH_PREFIX
ATTACH_TMP_URL = ATTACH_BASE_URL + TMP_PREFIX
@csrf_exempt
@login_required
def index(request):
    if request.method == 'POST':
        content_type = request.GET.get('content_type')
        content_id = request.GET.get('content_id')
        return upload(request, content_type, content_id)
    return render(request, 'attacher/frontend/index.html', {
        'var': 'ewdfwe'
    })

@login_required
def upload(request, content_type, content_id):
    upload_info  = handle_uploaded_file(request.FILES.get('files[]'), content_type, content_id)
    return HttpResponse(json.dumps({
        'title': upload_info[0],
        'url': upload_info[1],
        'delete_path': upload_info[2],
        'sign_delete_path': upload_info[3],
    }))

@login_required
def delete(request):
    path = request.GET.get('path', None)
    sign = request.GET.get('sign', None)
    content_type = request.GET.get('content_type', None)
    content_id = request.GET.get('content_id', None)

    if not path or not sign or not content_type or not content_id:
        return HttpResponse(u'Wrong arguments', status=400)

    if sign != get_sign_delete_path(path):
        return HttpResponse(u'Wrong path', status=403)
    target_file_path = get_dir_for_object(content_type, content_id) + path
    if os.path.isfile(target_file_path):
        os.remove(target_file_path)

    return HttpResponse('Ok')

def handle_uploaded_file(f, content_type, content_id):


    file_name = f.name
    file_name_parts = file_name.split('.')

    ext = u''
    if len(file_name_parts) > 1:
        ext = file_name_parts[-1]
        file_name = u'.'.join(file_name_parts[:-1])
    else:
        file_name =u'.'.join(file_name_parts)

    if len(file_name) > 32:
        file_name = file_name[:32]

    if ext:
        file_name = file_name + u'.' + ext

    file_name = file_name.lower().replace(' ', '_')
    file_name =   uuid.uuid4().hex + u'_' + unicode(file_name)

    target_dir_path = get_dir_for_object(content_type, content_id)

    if not os.path.isdir(target_dir_path):
        os.makedirs(target_dir_path, 0775)

    with open(target_dir_path + file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    media_path = get_media_url_for_file(content_type, content_id, file_name)

    delete_path = u'%s' % (file_name)
    sign_delete_path = get_sign_delete_path(delete_path)
    return (f.name, media_path, delete_path, sign_delete_path)



def get_sign_delete_path(delete_path):
    return  hashlib.md5(unicode(delete_path).encode('utf-8') + settings.SECRET_KEY).hexdigest()



def get_dir_for_object(content_type, content_id):
    content_type = content_type.replace(u'/', u'_')
    content_id = content_id.replace(u'/', u'_')
    return '%s%s/%s/' % (ATTACH_BASE_PATH , content_type, content_id)


def get_media_url_for_file(content_type, content_id, file_name):
    content_type = content_type.replace(u'/', u'_')
    content_id = content_id.replace(u'/', u'_')
    return u'%s%s/%s/%s' %(ATTACH_BASE_URL , content_type, content_id, file_name)



def delete_content_attaches(content_type, content_id):
    content_dir = get_dir_for_object(content_type, content_id)
    if os.path.isdir(content_dir):
        shutil.rmtree(content_dir)