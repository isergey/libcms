# encoding: utf-8
from django.contrib.auth import authenticate
from decorators import api
from django.contrib.auth import login


@api
def auth(request):

    username = request.GET.get('username', None)
    password = request.GET.get('password', None)

    if username and password:
        user_cache = authenticate(username=username, password=password)
        if user_cache is None:
            return {}
        elif not user_cache.is_active:
            return {}


        login(request, user_cache)
        return {'api.sessionid':request.session.session_key}
    return {}
