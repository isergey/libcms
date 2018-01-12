# coding=utf-8
import json
from datetime import datetime, timedelta
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from ruslan_users.models import SyncStatus, RuslanUser
from ruslan import client, connection_pool, humanize, holdings, grs

RUSLAN = getattr(settings, 'RUSLAN', {})
API_ADDRESS = RUSLAN.get('api_address', 'http://localhost/')
API_USERNAME = RUSLAN.get('username')
API_PASSWORD = RUSLAN.get('password')

SYNC_TIMEOUT_MINUTES = 60 * 2


class Command(BaseCommand):
    @atomic
    def handle(self, *args, **options):
        # sync_status = SyncStatus.get_or_create()
        # now = datetime.now()
        #
        # if sync_status.sync_started_at:
        #     if now - timedelta(minutes=SYNC_TIMEOUT_MINUTES) < sync_status.sync_started_at:
        #         return
        #
        # sync_status.sync_started_at = now
        # sync_status.last_sync = now
        # sync_status.record_processed = 0
        # sync_status.save()

        ruslan_client = client.HttpClient(API_ADDRESS, API_USERNAME, API_PASSWORD, auto_close=False)

        maximum_records = 200
        res = ruslan_client.extract_records(
            database='lusr_rt',
            query='@attrset bib-1 @attr 1=100 @attr 2=4 0',
            maximum_records=maximum_records,
            start_record=1,
            accept='application/json',
            result_set_ttl=60,
            limit=1
        )
        i = 1
        for record in res:
            grs_record = grs.Record.from_dict(humanize.get_record_content(record))
            user_id = grs_record.get_field_value('100')
            rusln_user = RuslanUser()
            rusln_user.user_id = user_id
            rusln_user.first_name = grs_record.get_field_value('101')
            rusln_user.patronymic = grs_record.get_field_value('103')
            rusln_user.last_name = grs_record.get_field_value('102')
            rusln_user.email = grs_record.get_field_value('122')
            birth_date_str = grs_record.get_field_value('234')
            if birth_date_str:
                rusln_user.birth_date = datetime.strptime(birth_date_str, '%Y%m%d')
            sex = grs_record.get_field_value('404')
            if sex == 'М':
                rusln_user.sex = 'm'
            elif sex == 'Ж':
                rusln_user.sex = 'f'

            rusln_user.grs_json = json.dumps(grs_record.to_dict(), ensure_ascii=False)

            if i % 10 == 0:
                print i
            i += 1

        ruslan_client.close_session()
