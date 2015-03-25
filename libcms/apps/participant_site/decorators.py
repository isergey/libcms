# coding=utf-8
from django.shortcuts import HttpResponse, get_object_or_404
from participants.models import Library
import models


def must_be_manager(function):
    def wrapper(request, *args, **kwargs):
        library_code = kwargs.get('library_code')
        library = get_object_or_404(Library, code=library_code)
        managers = models.get_managers(request.user, library)
        if not managers:
            return HttpResponse(u'Вы не являетесь менеджером контента этой библиотеки', status=403)
        nkwargs = dict({
            'library': library,
        }, **kwargs)
        return function(request, **nkwargs)

    return wrapper