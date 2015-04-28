# coding=utf-8
from importlib import import_module
from datetime import datetime
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.exceptions import ImproperlyConfigured
from django.contrib import auth
from . import models


class OauthSessionMiddleware(object):
    #TODO: сделать сессию переиспользуемой

    def __init__(self):
        self.header = "HTTP_AUTHORIZATION"
        self.session_middleware = SessionMiddleware()
        engine = import_module(settings.SESSION_ENGINE)
        self.SessionStore = engine.SessionStore

    def process_request(self, request):
        try:
            auth_header = request.META[self.header]
        except KeyError:
            return self.session_middleware.process_request(request)

        token = ''
        if auth_header.startswith('token'):
            auth_header_parts = auth_header.split()
            if len(auth_header_parts) < 2:
                return
            token = auth_header_parts[1]

        if not token:
            return self.session_middleware.process_request(request)

        request.session = self.SessionStore(session_key=token)

    def process_response(self, request, response):
        authorization = request.META.get('HTTP_AUTHORIZATION', None)
        if authorization:
            response['Authorization'] = authorization
        else:
            return self.session_middleware.process_response(request, response)

        try:
            modified = request.session.modified
            if modified or settings.SESSION_SAVE_EVERY_REQUEST:
                if response.status_code != 500:
                    request.session.save()
        except AttributeError:
            pass

        return response


class OauthUserMiddleware(object):

    def process_request(self, request):
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The oauth user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")

        try:
            auth_header = request.META['HTTP_AUTHORIZATION']
        except KeyError:
            return

        token = ''
        if auth_header.startswith('token'):
            auth_header_parts = auth_header.split()
            if len(auth_header_parts) < 2:
                return
            token = auth_header_parts[1]

        if not token:
            return

        if request.user.is_authenticated():
            return
        now = datetime.now()
        models.AccessToken.objects.filter(token=token, expired__lt=now).delete()
        try:
            token_model = models.AccessToken.objects.select_related('auth_user').get(token=token, expired__gte=now)
        except models.AccessToken.DoesNotExist:
            return

        user = auth.authenticate(oauth_user=token_model.auth_user.username)

        if user:
            request.user = user
            auth.login(request, user)


