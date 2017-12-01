# coding=utf-8
import time
from functools import wraps
from django.conf import settings
from django.utils.importlib import import_module
from django.shortcuts import HttpResponse
from django.utils.cache import patch_vary_headers
from django.utils.http import cookie_date

from exceptions import ApiException
import responses


def login_required(message='Login required'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated():
                return view_func(request, *args, **kwargs)
            return responses.errors_response(
                message=message,
                code='auth.not_authenticated',
                status=401
            )

        return _wrapped_view

    return decorator


def permission_required(perm, message='Access denied'):
    def _check_perms(user):
        if not isinstance(perm, (list, tuple)):
            perms = (perm,)
        else:
            perms = perm
        if user.has_perms(perms):
            return True
        return False

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if _check_perms(request.user):
                return view_func(request, *args, **kwargs)
            return responses.errors_response(
                message=message,
                code='auth.no_have_permission',
                status=403,
                explain={
                    'permissions': unicode(perm)
                }
            )

        return _wrapped_view

    return decorator


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
                'status': 'ok',
                'response': data
            }

        except ApiException as e:
            vars = {
                'status': 'error',
                'error': e.message
            }
        return process_response(args[0], responses.response(vars))

    return wrapper


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
            response.set_cookie(
                settings.SESSION_COOKIE_NAME,
                request.session.session_key, max_age=max_age,
                expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                path=settings.SESSION_COOKIE_PATH,
                secure=settings.SESSION_COOKIE_SECURE or None,
                httponly=settings.SESSION_COOKIE_HTTPONLY or None)
    return response
