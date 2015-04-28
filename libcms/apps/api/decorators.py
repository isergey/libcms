# encoding: utf-8
import json
import time
from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.utils.http import cookie_date
from django.utils.importlib import import_module
from django.shortcuts import HttpResponse
from django.http import HttpResponseForbidden
from django.utils.decorators import available_attrs

from exceptions import ApiException
from common import response


def process_request(request):
    engine = import_module(settings.SESSION_ENGINE)
    session_key = request.GET.get('api.sessionid', None)
    if not session_key:
        session_key = request.POST.get('api.sessionid', None)
    if not session_key:
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)

    request.session = engine.SessionStore(session_key)
    return request

def process_response(request, response):
    """
    If request.session was modified, or if the configuration is to save the
    session every time, save the changes and set a session cookie.
    """
    try:
        accessed = request.session.accessed
        modified = request.session.modified
    except AttributeError:
        pass
    else:
        if accessed:
            patch_vary_headers(response, ('Cookie',))
        if modified or settings.SESSION_SAVE_EVERY_REQUEST:
            if request.session.get_expire_at_browser_close():
                max_age = None
                expires = None
            else:
                max_age = request.session.get_expiry_age()
                expires_time = time.time() + max_age
                expires = cookie_date(expires_time)
                # Save the session data and refresh the client cookie.
            request.session.save()
            response.set_cookie(settings.SESSION_COOKIE_NAME,
                request.session.session_key, max_age=max_age,
                expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                path=settings.SESSION_COOKIE_PATH,
                secure=settings.SESSION_COOKIE_SECURE or None,
                httponly=settings.SESSION_COOKIE_HTTPONLY or None)
    return response


def api(func):
    """
    декоратор для обработки вызовов api
    """
    def wrapper(*args, **kwargs):
        args = list(args)
        args[0] = process_request(args[0])

        try:
            data = func(*args, **kwargs)
            if isinstance(data, HttpResponse):
                return data
            vars = {
                'status':'ok',
                'response': data
            }

        except ApiException as e:
            vars = {
                'status':'error',
                'error': e.message
            }
        return process_response(args[0], response(vars))

    return wrapper


try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.


def user_passes_test(test_func):

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)

            return HttpResponseForbidden()
        return _wrapped_view
    return decorator


def login_required_or_403(function=None):

    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated()
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def login_required_ajax(function=None,redirect_field_name=None):
    def _decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse(json.dumps({
                    'status': 'error',
                    'code': 'auth_required',
                    'message': 'You need logged in'
                }), status=401)
        return _wrapped_view

    if function is None:
        return _decorator
    else:
        return _decorator(function)


def permission_required_or_403(perm):
    return user_passes_test(lambda u: u.has_perm(perm))