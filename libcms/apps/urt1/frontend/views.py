# -*- coding: utf-8 -*-
from pyaz import *
from django.db import transaction
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required

from participants.models import Library
from ..models import LibReader
from forms import LibReaderForm, LibReaderAuthForm

@login_required
def index(request):
    try:
        lib_reader = LibReader.objects.get(user=request.user)
    except LibReader.DoesNotExist:
        lib_reader = None
    return render(request, 'urt/frontend/index.html', {
        'lib_reader': lib_reader
    })

@login_required
@transaction.atomic()
def link(request):
    errors = []

    if request.method == 'POST':
        form = LibReaderForm(request.POST)
        if form.is_valid():
            LibReader(user=request.user, reader_id=form.cleaned_data['reader_id']).save()
            return redirect('urt:frontend:index')
            # library =  form.cleaned_data['library']
            # if not library.z_service:
            #     errors.append(u'Выбранная ЦБС не имеет возможности учавствовать в связывании.')
            # else:
            #     zopt = ZOptions()
            #     zopt.set_user(form.cleaned_data['lib_login'])
            #     zopt.set_password(form.cleaned_data['lib_password'])
            #     zcon = ZConnection(zopt)
            #     try:
            #         zcon.connect(library.z_service, '0')
            #         # если исключение не вылетело, то подключение и авторизация прошла успешно
            #         # можно считать, что связь удалась
            #         libuser = form.save(commit=False)
            #         libuser.user = request.user
            #
            #         if not LibReader.objects.filter(library=library, user=request.user).count():
            #             libuser.save()
            #         return redirect('urt:frontend:index')
            #     except ZConnectionException as e:
            #         if e.message.startswith('Init rejected:'):
            #             errors.append(u'Пользователь с таким идентификатором и паролем не найден. Проверьте правильность вводимых данных.')
            #         elif message.startswith('Connect failed:'):
            #             errors.append(u'Сервер ЦБС не доступен.')
            #         elif e.message.startswith('Timeout:'):
            #             errors.append(u'Сервер ЦБС не отвечает.')
            #         else:
            #             raise e

    else:
        form = LibReaderForm()


    return render(request, 'urt/frontend/link.html', {
        'form': form,
        'errors': errors,
    })

@login_required
def edit_link(request, id):
    link = get_object_or_404(LibReader, id=id)
    errors = []

    if request.method == 'POST':
        form = LibReaderForm(request.POST, instance=link)
        if form.is_valid():
            library =  form.cleaned_data['library']
            if not library.z_service:
                errors.append(u'Выбранная ЦБС не имеет возможности учавствовать в связывании.')
            else:
                zopt = ZOptions()
                zopt.set_user(form.cleaned_data['lib_login'])
                zopt.set_password(form.cleaned_data['lib_password'])
                zcon = ZConnection(zopt)
                try:
                    zcon.connect(library.z_service, '0')
                    # если исключение не вылетело, то подключение и авторизация прошла успешно
                    # можно считать, что связь удалась
                    form.save()
                    return redirect('urt:frontend:index')
                except ZConnectionException as e:
                    if e.message.startswith('Init rejected:'):
                        errors.append(u'Пользователь с таким идентификатором и паролем не найден. Проверьте правильность вводимых данных.')
                    elif message.startswith('Connect failed:'):
                        errors.append(u'Сервер ЦБС не доступен.')
                    elif e.message.startswith('Timeout:'):
                        errors.append(u'Сервер ЦБС не отвечает.')
                    else:
                        raise e

    else:
        form = LibReaderForm(instance=link)

    return render(request, 'urt/frontend/edit_link.html', {
        'form': form,
        'errors': errors
    })
@login_required
def auth(request, id):

    errors = []
    # проверка на существование связи
    if LibReader.objects.filter(library_id=id, user=request.user).count():
        return redirect('urt:frontend:index')
    library = get_object_or_404(Library, id=id)

    if not library.z_service:
        return HttpResponse(u'Отсутвуют параметры сервера авторизации. Если Вы увидели это сообщение, пожалуйста, свяжитесь с администратором портала.')


    back = request.GET.get('back', None)
    if request.method == 'POST':
        form = LibReaderAuthForm(request.POST)
        if form.is_valid():
            zopt = ZOptions()
            zopt.set_user(form.cleaned_data['lib_login'])
            zopt.set_password(form.cleaned_data['lib_password'])
            zcon = ZConnection(zopt)
            try:
                zcon.connect(library.z_service, '0')
                # если исключение не вылетело, то подключение и авторизация прошла успешно
                # можно считать, что связь удалась
                libuser = form.save(commit=False)
                libuser.user = request.user
                libuser.library = library
                libuser.save()
                if back:
                    return redirect(back)
                else:
                    return redirect('urt:frontend:index')
            except ZConnectionException as e:
                if e.message.startswith('Init rejected:'):
                    errors.append(u'Пользователь с таким идентификатором и паролем не найден. Проверьте правильность вводимых данных.')
                elif message.startswith('Connect failed:'):
                    errors.append(u'Сервер ЦБС не доступен.')
                elif e.message.startswith('Timeout:'):
                    errors.append(u'Сервер ЦБС не отвечает.')
                else:
                    raise e
    else:
        form = LibReaderAuthForm()
    return render(request, 'urt/frontend/auth.html', {
        'form': form,
        'library': library,
        'errors': errors,

    })