import struct
import base64

from django.contrib import auth
from django.contrib.auth import load_backend
from django.contrib.auth.backends import RemoteUserBackend
from django.core.exceptions import ImproperlyConfigured


def get_msg_str(msg,start):
    msg_len, _, msg_off = struct.unpack("<HHH", msg[start:start + 6])
    return msg[msg_off:msg_off + msg_len].replace("\0", '')

def ntlm_auth(auth):
    """Goes through ntlm stages...
    Return user_name, response.
    While response is not none, keep sending it.
    Then use the user.
    """
    username = u''
    domain = u''
    comp = u''


    if auth[:4] == "NTLM":
        msg = base64.b64decode(auth[4:])
        #  print repr(msg)
        ntlm_fmt = "<8sb" #string, length 8, 4 - op
        NLTM_SIG = "NTLMSSP\0"
        signature, op = struct.unpack(ntlm_fmt, msg[:9])
        if signature != NLTM_SIG:
            pass
        else:
            # print signature, op
            # print repr(msg)
            if op == 1:
                out_msg_fmt = ntlm_fmt + "2I4B2Q2H"
                out_msg = struct.pack(out_msg_fmt,
                    NLTM_SIG, #Signature
                    2, #Op
                    0, #target name len
                    0, #target len off
                    1, 2, 0x81, 1, #flags
                    0, #challenge
                    0, #context
                    0, #target info len
                    0x30, #target info offset
                )

                # response = HttpResponse(status=401)
                # response['WWW-Authenticate'] = "NTLM " + base64.b64encode(out_msg).strip()
            elif op == 3:
                # print 'msg', msg
                # for i in xrange(100):
                #     print i, get_msg_str(msg, i)
                # print '1111 ', get_msg_str(msg, 36).decode('cp1251')
                username = get_msg_str(msg, 36)
                domain = get_msg_str(msg, 28)
                comp = get_msg_str(msg, 44)
                #username, domain, comp
    return {
        'username': username,
        'domain': domain,
        'comp': comp
    }

class NTLMMiddleware(object):
    """
    Middleware for utilizing Web-server-provided authentication.
    If request.user is not authenticated, then this middleware attempts to
    authenticate the username passed in the ``REMOTE_USER`` request header.
    If authentication is successful, the user is automatically logged in to
    persist the user in the session.
    The header used is configurable and defaults to ``REMOTE_USER``.  Subclass
    this class and change the ``header`` attribute if you need to use a
    different header.
    """

    # Name of request header to grab username from.  This will be the key as
    # used in the request.META dictionary, i.e. the normalization of headers to
    # all uppercase and the addition of "HTTP_" prefix apply.
    header = "HTTP_AUTHORIZATION"

    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")
        try:
            http_auth = request.META[self.header]
        except KeyError:
            # If specified header doesn't exist then remove any existing
            # authenticated remote-user, or return (leaving request.user set to
            # AnonymousUser by the AuthenticationMiddleware).
            # if request.user.is_authenticated():
            #     self._remove_invalid_user(request)
            return
        user = None
        if http_auth and http_auth.startswith('NTLM'):
            # for key in request.META:
            #     print key, request.META[key]
            result = ntlm_auth(http_auth)
            username = result.get('username', '')
            domain = result.get('domain', '')
            if not username:
                return
            # prefix = ''
            # if domain:
            # #     prefix = domain + '\\'
            # # (auth_profile, created) = models.AuthProfile.objects.get_or_create(type='ad', auth_name=prefix + username)
            # # user = models.create_user_with_auth(auth_profile)
        else:
            return
        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        # if request.user.is_authenticated():
        #     if request.user.get_username() == user.username:
        #         return
        #     else:
        #         # An authenticated user is associated with the request, but
        #         # it does not match the authorized user in the header.
        #         self._remove_invalid_user(request)

        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        user = auth.authenticate(ad_username=username, ad_domain=domain)
        if user:
            # User is valid.  Set request.user and persist user in the session
            # by logging the user in.
            request.user = user
            auth.login(request, user)

    def clean_username(self, username, request):
        """
        Allows the backend to clean the username, if the backend defines a
        clean_username method.
        """
        backend_str = request.session[auth.BACKEND_SESSION_KEY]
        backend = auth.load_backend(backend_str)
        try:
            username = backend.clean_username(username)
        except AttributeError:  # Backend has no clean_username method.
            pass
        return username

    def _remove_invalid_user(self, request):
        """
        Removes the current authenticated user in the request which is invalid
        but only if the user is authenticated via the RemoteUserBackend.
        """
        try:
            stored_backend = load_backend(request.session.get(auth.BACKEND_SESSION_KEY, ''))
        except ImportError:
            # backend failed to load
            auth.logout(request)
        else:
            if isinstance(stored_backend, RemoteUserBackend):
                auth.logout(request)