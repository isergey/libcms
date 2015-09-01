# coding=utf-8
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from accounts import models as accounts_models
from . import ldap_api

LDAP_SYNC_SETTINGS = getattr(settings, 'LDAP_SYNC', {})

LDAP_SERVER = LDAP_SYNC_SETTINGS.get('ldap_server', 'ldaps://127.0.0.1:636')
BIND_DN = LDAP_SYNC_SETTINGS.get('bind_dn', '')
BIND_PASS = LDAP_SYNC_SETTINGS.get('bind_pass', '')
BASE_DN = LDAP_SYNC_SETTINGS.get('base_dn', '')
DOMAIN = LDAP_SYNC_SETTINGS.get('domain', '')


class SyncStatus(models.Model):
    sync_count = models.IntegerField(default=0)
    sync_date = models.DateTimeField(auto_now=True, db_index=True)
    last_error = models.CharField(max_length=1024, blank=True)

    class Meta:
        verbose_name = u'Статус синхронизации'
        verbose_name_plural = u'Статусы синхронизаций'
        ordering = ['-sync_date']


class PasswordSync(models.Model):
    password = models.OneToOneField(accounts_models.Password)
    sync_date = models.DateTimeField(auto_now=True)
    synchronized = models.BooleanField(default=False, db_index=True)
    need_to_delete = models.BooleanField(default=False, db_index=True)
    last_error = models.CharField(max_length=1024, blank=True)


def _truncate_username(username):
    suffix = u'@tatar.ru'
    if username.endswith(suffix):
        username = username.replace(suffix, u'')
    return username


def sync_account(password_model, already_ldap_session=None):
    user = password_model.user
    password = password_model.password

    username = _truncate_username(user.username)
    try:
        password_sync = PasswordSync.objects.get(password=password_model)
    except PasswordSync.DoesNotExist:
        password_sync = PasswordSync(password=password_model)
        password_sync.save()

    user_already_exist = False
    api_client = None

    if not already_ldap_session:
        api_client = ldap_api.Client(ldap_server=LDAP_SERVER, bind_dn=BIND_DN, bind_password=BIND_PASS)
        try:
            ldap_session = api_client.connect()
        except ldap_api.LdapApiError as e:
            password_sync.synchronized = False
            password_sync.last_error = e.message[:1024]
            password_sync.save()
            api_client.disconnect()
            return
    else:
        ldap_session = already_ldap_session

    try:
        if ldap_session.search_user(username, BASE_DN):
            user_already_exist = True
    except ldap_api.LdapApiError as e:
        password_sync.synchronized = False
        password_sync.last_error = e.message[:1024]
        password_sync.save()

    if not user_already_exist:
        try:
            ldap_session.create_user(
                username=username,
                password=password,
                base_dn=BASE_DN,
                domain=DOMAIN,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email
            )
            password_sync.synchronized = True
            password_sync.last_error = ''
        except ldap_api.LdapApiError as e:
            password_sync.synchronized = False
            password_sync.last_error = e.message[:1024]
    else:
        try:
            ldap_session.update_user(
                username=username,
                password=password,
                base_dn=BASE_DN,
                domain=DOMAIN,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email
            )
            password_sync.synchronized = True
            password_sync.last_error = ''
        except ldap_api.LdapApiError as e:
            password_sync.synchronized = False
            password_sync.last_error = e.message[:1024]

    if not already_ldap_session:
        api_client.disconnect()
    password_sync.save()


def sync_all_passwords():
    api_client = ldap_api.Client(ldap_server=LDAP_SERVER, bind_dn=BIND_DN, bind_password=BIND_PASS)
    try:
        ldap_session = api_client.connect()
    except ldap_api.LdapApiError as e:
        print u'Error of connection to LDAP: %s' % e.message
        return
    i = 0
    for password_model in accounts_models.Password.objects.select_related('user').all().iterator():
        i += 1
        sync_account(password_model, ldap_session)
        print u'%s %s' % (i, password_model.user.username)

    api_client.disconnect()
    print 'All passwords synchronized'


@receiver(post_save, sender=accounts_models.Password)
def pre_save_password_callback(sender, **kwargs):
    password_model = kwargs['instance']
    sync_account(password_model)


@receiver(post_delete, sender=accounts_models.Password)
def post_delete_password_callback(sender, **kwargs):
    api_client = ldap_api.Client(ldap_server=LDAP_SERVER, bind_dn=BIND_DN, bind_password=BIND_PASS)
    inst = kwargs['instance']
    user = inst.user
    #
    # password_sync = None
    #
    # try:
    #     password_sync = PasswordSync.objects.get(password=inst)
    # except accounts_models.Password.DoesNotExist:
    #     pass
    #
    try:
        ldap_session = api_client.connect()
        ldap_session.delete_user(
            username=_truncate_username(user.username),
            base_dn=BASE_DN,
        )
    except ldap_api.LdapApiError as e:
        pass
