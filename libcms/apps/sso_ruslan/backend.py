# encoding: utf-8
import logging
from django.conf import settings
from django.db import transaction
from django.contrib.auth.models import User, check_password, Group
from ruslan import connection_pool, client, humanize
from .models import RuslanUser
from sso import models as sso_models

RUSLAN = getattr(settings, 'RUSLAN', {})

API_ADDRESS = RUSLAN.get('api_address', 'http://localhost/')
API_USERNAME = RUSLAN.get('username')
API_PASSWORD = RUSLAN.get('password')

AUTH_SOURCE = 'ruslan'

logger = logging.getLogger('django.request')


class RuslanAuthBackend(object):
    def authenticate(self, username=None, password=None):
        if not username:
            return None
        user_auth_client = client.HttpClient(API_ADDRESS, username, password)
        portal_client = connection_pool.get_client(API_ADDRESS, API_USERNAME, API_PASSWORD)

        try:
            principal = user_auth_client.principal()
            if principal.get('id', '') != username:
                return None
        except Exception as e:
            logger.exception(e)
            return None

        sru_reps = portal_client.get_user(username)
        records = humanize.get_records(sru_reps)
        if not records:
            return None
        # 101 - фамилия
        # 102 - имя
        # 103 - отчество
        grs_record = humanize.grs_to_dict(humanize.get_record_content(records[0]).get('GRSTag', [{}]))
        user_password = password
        if user_password != password:
            return None

        return self.get_or_create_user(username, password, grs_record)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    @transaction.atomic()
    def get_or_create_user(self, username, password, user_info):
        first_name = user_info.get(u'102', [{}])[0].get('content', '')[:30]
        last_name = user_info.get(u'101', [{}])[0].get('content', '')[:30]
        email = user_info.get(u'122', [{}])[0].get('content', '')[:75]
        groups = ['users']

        user = sso_models.create_or_update_external_user(
            external_username=username,
            auth_source=AUTH_SOURCE,
            first_name=first_name,
            last_name=last_name,
            email=email,
            groups=groups,
            is_active=True
        ).user
        try:
            ruslan_user = RuslanUser.objects.get(user=user)
            need_update = False
            if ruslan_user.username != username:
                ruslan_user.username = username
                need_update = True
            if ruslan_user.password != password:
                ruslan_user.password = password
                need_update = True

            if need_update:
                ruslan_user.save()
        except RuslanUser.DoesNotExist:
            ruslan_user = RuslanUser(user=user, username=username, password=password)
            ruslan_user.save()

        return user
