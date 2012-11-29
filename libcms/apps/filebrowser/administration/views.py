# -*- coding: utf-8 -*-
import sys
import os
import datetime
import shutil
from django.conf import settings
from django.utils.translation import ugettext as _
from django.http import HttpResponseForbidden
from django.shortcuts import HttpResponse, Http404, HttpResponseRedirect, render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from guardian.decorators import permission_required_or_403
from forms import UploadFileForm, CreateDirectory

FILE_NAME_ENCODING = 'utf-8'

mtypes = {
    'gif': 'image',
    'jpg': 'image',
    'png': 'image',
    'pdf': 'pdf',
    'doc': 'doc',
    'xls': 'xsl',
}


def chek_or_create_dir(path):
    if not os.path.isdir(path):
        try:
            os.makedirs(path, 0755)
        except Exception as e:
            return False

    return True


def get_mtype(file_name):
    file_name_ext = file_name.split('.')

    if len(file_name_ext) > 1 and file_name_ext[1] in mtypes:
        return mtypes[file_name_ext[1]]

    return 'file'


def get_file_map(path, show_path_url, show_path):
    file_name = os.path.basename(path)
    item_map = {}

    item_map['type'] = 'file'
    item_map['mtype'] = get_mtype(file_name)
    item_map['name'] = file_name

    file_stat = os.stat(path)
    size = file_stat.st_size / 1024
    if size < 1:
        item_map['size'] = {
            'bytes': file_stat.st_size,
            'title': u'bytes'
        }
    else:
        item_map['size'] = {
            'bytes': size,
            'title': u'Kbytes'
        }

    item_map['create_time'] = datetime.datetime.fromtimestamp(file_stat.st_ctime)
    item_map['url'] = show_path_url.rstrip('/') + '/' + file_name
    item_map['work_url'] = show_path + '/' + file_name
    return item_map


def get_dir_map(path, show_path):
    dir_name = os.path.basename(path)
    item_map = {}

    item_map['type'] = 'dir'
    item_map['mtype'] = 'dir'
    item_map['name'] = dir_name

    dir_stat = os.stat(path)

    item_map['size'] = {
        'bytes': 0,
        'title': u'bytes'
    }

    item_map['create_time'] = datetime.datetime.fromtimestamp(dir_stat.st_ctime)
    item_map['url'] = show_path + '/' + dir_name + '/'
    return item_map


def handle_uploaded_file(f, path):
    destination = open(path + '/' + f.name.encode(FILE_NAME_ENCODING), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


@login_required
def index(request):
    if not request.user.has_module_perms('filebrowser'):
        return HttpResponseForbidden()

    base_uplod_path = settings.FILEBROWSER['upload_dir']

    show_path = u'' # root of upload path
    show_path_url = settings.FILEBROWSER['upload_dir_url']


    path = request.GET.get('path', u'/').strip('/')
    if '..' in path or '/.' in path:
        raise Http404(u"Path not founded")

    show_path =  path.encode(FILE_NAME_ENCODING)

    show_path_url += show_path

    if not chek_or_create_dir(base_uplod_path):
        return HttpResponse(u"Catalog '%s' can't be created" % show_path)

    if not os.path.isdir(base_uplod_path + show_path):
        raise Http404(u"Path not founded")

    dir_items = os.listdir(base_uplod_path + show_path)

    dir_map = []
    for dir_item in dir_items:
        path_to_dir_item = base_uplod_path + show_path + '/' + dir_item
        if os.path.isfile(path_to_dir_item):
            dir_map.append(get_file_map(path_to_dir_item, show_path_url, show_path))

        elif os.path.isdir(path_to_dir_item):
            dir_map.append(get_dir_map(path_to_dir_item, show_path))

        # не выводим элемент
        else:
            continue

    breadcrumbs = []
    path_dirs = show_path.strip('/').split('/')
    breadcrumbs.append({
        'title': '/',
        'url': '/',
        })
    for i, path_dir in enumerate(path_dirs):
        breadcrumbs.append({
            'title': path_dir,
            'url': '/' + '/'.join(path_dirs[:i + 1]),
            })

    upload_form = UploadFileForm(initial={'path': show_path})
    dir_form = CreateDirectory(initial={'path': show_path}, prefix='dir_form')

    dir_map = sorted(dir_map, key=lambda x: x['create_time'], cmp=lambda x, y: cmp(x, y), reverse=True)
    dir_map = sorted(dir_map, key=lambda x: x['type'], cmp=lambda x, y: cmp(x.lower(), y.lower()))

    return render(request, 'filebrowser/administration/list.html', {
        'dir_map': dir_map,
        'breadcrumbs': breadcrumbs,
        'upload_form': upload_form,
        'dir_form': dir_form,
        'active_module': 'filebrowser'
    })


@login_required
@permission_required_or_403('filebrowser.delete_file')
def delete(request):

    base_uplod_path = settings.FILEBROWSER['upload_dir']

    current_dir = '/'
    if 'path' in request.GET:
        path = request.GET['path'].strip('/')
        if '..' in path or '/.' in path:
            raise Http404(u"Path not founded")

        delete_path = '%s' % path.encode(FILE_NAME_ENCODING)
        current_dir = os.path.split(delete_path)[0]

        delete_path = base_uplod_path + delete_path
        print delete_path
        if os.path.isfile(delete_path):
            os.remove(delete_path)
        if os.path.isdir(delete_path):
            shutil.rmtree(delete_path)
    return HttpResponseRedirect(reverse('filebrowser:administration:index') + '?path=' + current_dir.decode(FILE_NAME_ENCODING))



@login_required
@permission_required_or_403('filebrowser.add_file')
def upload(request):

    path = u'/'
    base_uplod_path = settings.FILEBROWSER['upload_dir']
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            path = form.cleaned_data['path'].encode(FILE_NAME_ENCODING)
            upload_path = base_uplod_path + path
            file_name = request.FILES['file'].name
            if os.path.isfile(upload_path + '/' + file_name.encode(FILE_NAME_ENCODING)):
                return HttpResponse(_(u'File with this name already exist. Please, delete old file or rename uploadable file.'))
            elif  os.path.isdir(upload_path + '/' + file_name.encode(FILE_NAME_ENCODING)):
                return HttpResponse(_(u'Directory with this name already exist. Please, delete old directory or rename uploadable file.'))

            if not os.path.isdir(upload_path):
                raise Http404(u"Path not founded")

            handle_uploaded_file(f=request.FILES['file'], path=upload_path)

    return HttpResponseRedirect(reverse('filebrowser:administration:index') + '?path=' + path.decode(FILE_NAME_ENCODING))



@login_required
@permission_required_or_403('filebrowser.add_file')
def create_directory(request):

    path = u'/'
    base_uplod_path = settings.FILEBROWSER['upload_dir']

    if request.method == 'POST':
        dir_form = CreateDirectory(request.POST, prefix='dir_form')
        if dir_form.is_valid():
            path = dir_form.cleaned_data['path'].encode(FILE_NAME_ENCODING)
            upload_path = base_uplod_path + path
            dir_name = dir_form.cleaned_data['name'].encode(FILE_NAME_ENCODING)
            if os.path.isfile(upload_path + '/' +dir_name):
                return HttpResponse(_(u'File with this name already exist. Please, delete old file or rename creatable directory.'))
            elif  os.path.isdir(upload_path + '/' + dir_name):
                return HttpResponse(_(u'Directory with this name already exist. Please, delete old directory or or rename creatable directory.'))

            if not os.path.isdir(upload_path):
                raise Http404(_(u"Path not founded"))
            upload_path = upload_path.rstrip('/')
            os.mkdir(upload_path + '/' + dir_name, 0755)

    return HttpResponseRedirect(reverse('filebrowser:administration:index') + '?path=' + path.decode(FILE_NAME_ENCODING))


