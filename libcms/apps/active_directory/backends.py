# encoding: utf-8
#import ldap
import logging
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from models import AdUser

logger = logging.getLogger('')

ACTIVE_DIRECTORY = getattr(settings, 'ACTIVE_DIRECTORY', {})

AD_REST_PATH = ACTIVE_DIRECTORY.get('AD_REST_PATH', 'http://localhost/handler.ashx')

AUTH_IF_NOT_FOUND = ACTIVE_DIRECTORY.get('AUTH_IF_NOT_FOUND', True)


def get_user_info(ad_username, ad_domain=''):
    response = requests.get(AD_REST_PATH, params={
        'login': ad_username,
        'domain': ad_domain
    })

    response.raise_for_status()

    response_dict = response.json()

    if 'error' in response_dict:
        return None

    user_info = {}

    response_user_info = response_dict.get('userInfo', {})
    user_info['first_name'] = response_user_info.get('GivenName', u'')
    user_info['last_name'] = response_user_info.get('Surname', u'')
    user_info['middle_name'] = response_user_info.get('MiddleName', u'')
    user_info['email'] = response_user_info.get('EmailAddress', u'')

    return user_info



class RemoteUserBackend(object):

    create_unknown_user = True

    def authenticate(self, ad_remote_user):
        remote_user_parts = ad_remote_user.split('\\')
        if len(remote_user_parts) != 2:
            return None
        ad_domain = remote_user_parts[0]
        ad_username = remote_user_parts[1]

        """
        The username passed as ``remote_user`` is considered trusted.  This
        method simply returns the ``User`` object with the given username,
        creating a new ``User`` object if ``create_unknown_user`` is ``True``.
        Returns None if ``create_unknown_user`` is ``False`` and a ``User``
        object with the given username is not found in the database.
        """
        if not ad_remote_user:
            return
        user = None
        username = self.clean_username(ad_remote_user)


        first_name = u''
        last_name = u''
        email = u''

        user_info = None
        try:
            user_info = get_user_info(ad_username, ad_domain)
            if user_info:
                first_name = user_info.get('first_name', u'')
                middle_name = user_info.get('middle_name', u'')

                if middle_name:
                    first_name += u' %s.' % middle_name[0]

                last_name = user_info.get('last_name', u'')
                email = user_info.get('email', u'')
        except Exception as e:
            logger.error(u'Error while get user info from AD: %s' % e.message)

        if not AUTH_IF_NOT_FOUND and not user_info:
            return None

        (ad_user, user) = AdUser.get_or_create(username, first_name, last_name, email)

        return user

    def clean_username(self, username):
        """
        Performs any cleaning on the "username" prior to using it to get or
        create the user object.  Returns the cleaned username.
        By default, returns the username unchanged.
        """
        if len(username) > 255: username = username[0:255]
        return username

    def configure_user(self, user):
        """
        Configures a user after creation and returns the updated user.
        By default, returns the user unmodified.
        """
        return user

    def get_user(self, id):
        User = get_user_model()
        try:
            return User.objects.get(pk=id)
        except:
            return None


"""
class ActiveDirectoryLdapBackend(object):
    def authenticate(self, username=None, password=None):
        if not username:
            return None

        dj_username = username.lower()

        if len(dj_username) > 255:
            return None

        domain = ''

        username_parts = dj_username.split('\\')

        if len(username_parts) > 2:
            return None

        elif len(username_parts) == 2:
            username_parts.reverse()
            dj_username = username_parts[0]
            domain = username_parts[1]
        else:
            dj_username = username_parts[0]

        username_parts = dj_username.split('@')

        if len(username_parts) > 2:
            return None
        elif len(username_parts) == 2:
            dj_username = username_parts[0]
            domain = username_parts[1]
        else:
            dj_username = username_parts[0]

        auth_name = ''
        if domain:
            auth_name = dj_username + '@' + domain

        try:
            l = ldap.initialize('ldap://' + settings.ACTIVE_DIRECTORY.get('HOST'))
            l.set_option(ldap.OPT_REFERRALS, 0)
            l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
            l.set_option(ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
            l.set_option(ldap.OPT_X_TLS_DEMAND, False)
            l.set_option(ldap.OPT_X_TLS_DEMAND, False)
            l.set_option(ldap.OPT_DEBUG_LEVEL, 255)
            ldap.set_option(ldap.OPT_REFERRALS, 0)
            l.simple_bind_s(auth_name.encode('utf-8'), password.encode('utf-8'))
        except ldap.LDAPError as e:
            connectError = 'Error connecting to LDAP server: ' + str(e)
            return None

        try:
            res = l.search_s('dc=' + settings.ACTIVE_DIRECTORY.get('BASE_DC'), ldap.SCOPE_SUBTREE,
                             '(userprincipalName=%s)' % (auth_name.encode('utf-8')))
        except Exception as e:
            logger.error(unicode(e))
            return None

        first_name = u''
        last_name = u''
        email = u''

        try:
            first_name = res[0][1].get('givenName', [])[0]
        except:
            pass

        try:
            last_name = res[0][1].get('sn', [])[0]
        except:
            pass

        try:
            email = res[0][1].get('mail', [])[0]
        except:
            pass

        return get_or_create_user(
            username=dj_username,
            domain=domain,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
"""
