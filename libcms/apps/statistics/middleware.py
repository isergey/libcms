import uuid
import hashlib
import datetime

from django.conf import settings

from localeurl import utils
from .models import log_page_view, PageView

IGNORED_PATHES = [settings.STATIC_URL, settings.MEDIA_URL]
URL_TIMEOUT = 10


class SetSessionCookies(object):
    def process_request(self, request):
        pass

    def process_response(self, request, response):
        if not request.COOKIES.get('_sc', None):
            response.set_cookie('_sc', uuid.uuid4().hex)
        return response


class RequestLog(object):
    def process_response(self, request, response):
        session = request.COOKIES.get('_sc', None)

        if not session:
            session = uuid.uuid4().hex
            response.set_cookie('_sc', session, max_age=60 * 60 * 24 * 365)
        if request.is_ajax():
            return response

        path_parts = utils.strip_path(request.META.get('PATH_INFO', '').lower())
        if len(path_parts) > 1:
            path = path_parts[1]
        else:
            path = path_parts[0]
        ignore = False
        for ignore_path in IGNORED_PATHES:
            if path.startswith(ignore_path):
                ignore = True
        query = request.META.get('QUERY_STRING', '').lower()

        url_hash = hashlib.md5((path + query).encode('utf-8')).hexdigest()

        before = (datetime.datetime.now() - datetime.timedelta(minutes=URL_TIMEOUT))
        if PageView.objects.filter(datetime__gt=before, session=session, url_hash=url_hash).exists():
            ignore = True

        if session and not ignore:
            log_page_view(path=path, query=query, url_hash=url_hash, session=session)

        return response


