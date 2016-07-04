# -*- coding: utf-8 -*-
import base64
import json
import logging
import os
import uuid
from datetime import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.shortcuts import render, redirect

import requests
from ruslan import connection_pool, humanize
from ruslan import grs
from . import forms
from . import models

SITE_DOMAIN = getattr(settings, 'SITE_DOMAIN', 'esia.gosuslugi.ru')
RUSLAN = getattr(settings, 'RUSLAN', {})

RUSLAN_API_ADDRESS = RUSLAN.get('api_address', 'http://localhost/')
RUSLAN_API_USERNAME = RUSLAN.get('username')
RUSLAN_API_PASSWORD = RUSLAN.get('password')
RUSLAN_USERS_DATABASE = RUSLAN.get('users_database', 'allusers')
RUSLAN_ID_MASK = RUSLAN.get('id_mask', '000000000')

AUTH_SOURCE = 'esia'

ESIA_SSO = getattr(settings, 'ESIA_SSO', {})
ESIA_SSO_TMP_DIR = ESIA_SSO.get('tmp_dir', '/tmp')
ESIA_SSO_JAR_CERT_GENERATOR = ESIA_SSO.get('jar_cert_generator')
ESIA_SSO_CERT_ALIAS = ESIA_SSO.get('cert_alias', 'RaUser-561d2f13-c72b-4018-a473-48017a4622d2')
ESIA_SSO_CERT_PASSWORD = ESIA_SSO.get('cert_password', '1234567890')
ESIA_SSO_CLIENT_ID = unicode(ESIA_SSO.get('client_id', ''))
ESIA_SSO_SCOPE = unicode(ESIA_SSO.get('scope', 'http://esia.gosuslugi.ru/usr_inf'))
ESIA_SSO_ACCESS_TOKEN_URL = ESIA_SSO.get('access_token_url', 'https://esia.gosuslugi.ru/aas/oauth2/ac')
ESIA_SSO_ACCESS_MARKER_URL = ESIA_SSO.get('access_marker_url', 'https://esia.gosuslugi.ru/aas/oauth2/te')
ESIA_SSO_PERSON_URL = ESIA_SSO.get('person_url', 'https://esia.gosuslugi.ru/rs/prns')
ESIA_SSO_ASK_FOR_EXIST_READER = ESIA_SSO.get('ask_for_exist_reader', True)
ESIA_SSO_PASSWORD_LENGTH = ESIA_SSO.get('password_length', 8)

PERSON_CONTACTS_URL_SUFFIX = 'ctts'
PERSON_ADDRESS_URL_SUFFIX = 'addrs'

RESPONSE_TYPE = 'code'
REDIRECT_URI = 'https://kitap.tatar.ru/esia_sso/redirect'

VERIFY_REQUESTS = False

# KITAP_TATAR_API_BASE_ADDRESS = getattr(settings, 'KITAP_TATAR_API_BASE_ADDRESS', 'http://127.0.0.1')


logger = logging.getLogger('django.request')


def index(request):
    timestamp = unicode(datetime.now().strftime('%Y.%m.%d %H:%M:%S +0300'))
    state = unicode(uuid.uuid4())
    client_secret = _get_client_secret(ESIA_SSO_SCOPE, timestamp, ESIA_SSO_CLIENT_ID, state)
    return render(request, 'esia_sso/index.html', {
        'access_type': 'offline',
        'client_id': ESIA_SSO_CLIENT_ID,
        'scope': ESIA_SSO_SCOPE,
        'response_type': RESPONSE_TYPE,
        'timestamp': timestamp,
        'state': state,
        'client_secret': client_secret,
        'access_token_url': ESIA_SSO_ACCESS_TOKEN_URL
    })


def _generate_password(length=ESIA_SSO_PASSWORD_LENGTH):
    if not isinstance(length, int) or length < ESIA_SSO_PASSWORD_LENGTH:
        raise ValueError("temp password must have positive length")
    chars = "ABCDEFGHJKMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz123456789"
    return "".join([chars[ord(c) % len(chars)] for c in os.urandom(length)])


def _create_grs_from_esia(oid, email='', user_attrs=None):
    user_attrs = user_attrs or {}
    gender_map = {
        'm': u'М',
        'f': u'Ж'
    }

    person_info = user_attrs.get('person_info', {})
    person_addresses = user_attrs.get('person_addresses', [])
    person_address = {}

    if person_addresses:
        person_address = person_addresses[0]

    birth_date = person_info.get('birthDate', '')
    if birth_date:
        birth_date = datetime.strptime(birth_date, '%d.%m.%Y').strftime('%Y%m%d')

    registration_address_parts = []

    def add_to_registration_address(item):
        if not item:
            return
        registration_address_parts.append(item.strip())

    add_to_registration_address(person_address.get('region', ''))
    add_to_registration_address(person_address.get('city', ''))
    add_to_registration_address(person_address.get('street', ''))
    add_to_registration_address(person_address.get('house', ''))

    flat = person_address.get('flat', '')
    if flat:
        flat = u'кв. ' + flat
        add_to_registration_address(flat)

    region_city_parts = []
    region = person_address.get('region', '')
    city = person_address.get('city', '')

    if region:
        region_city_parts.append(region)
    if city:
        region_city_parts.append(city)

    foreigner = u''
    citizenship = person_info.get('citizenship', '').lower()

    if citizenship:
        if citizenship == 'rus':
            foreigner = u'0'
        else:
            foreigner = u'1'

    record = grs.Record()

    def add_field_to_record(tag, value):
        if not value:
            return
        record.add_field(grs.Field(tag, value))

    add_field_to_record('101', person_info.get('lastName', ''))
    add_field_to_record('102', person_info.get('firstName', ''))
    add_field_to_record('103', person_info.get('middleName', ''))
    add_field_to_record('105', datetime.now().strftime('%Y%m%d'))
    add_field_to_record('115', _generate_password())
    add_field_to_record('122', email)
    add_field_to_record('130', ', '.join(registration_address_parts))
    add_field_to_record('234', birth_date)
    add_field_to_record('402', person_info.get('snils', ''))
    add_field_to_record('403', oid)
    add_field_to_record('404', gender_map.get(person_info.get('gender', '').lower(), u''))
    add_field_to_record('423', person_address.get('zipCode', ''))
    add_field_to_record('424', ' / '.join(region_city_parts))
    add_field_to_record('427', foreigner)
    add_field_to_record('501', '2')

    trusted = person_info.get('trusted', False)
    if trusted is True:
        add_field_to_record('502', '1')
        add_field_to_record('503', '1')

    return record


esia_response = {
    "person_info": {
        "status": "REGISTERED",
        "birthPlace": "!Общая тестовая УЗ! ПОЖАЛУЙСТА, не изменяйте данные УЗ!ПОЖАЛУЙСТА!!!!!!!",
        "citizenship": "TJK", "firstName": "Имя001", "updatedOn": 1438692792, "middleName": "Отчество001",
        "lastName": "Фамилия0012",
        "birthDate": "07.01.1994",
        "eTag": "42D905D3CBEF2F2DC9FF85CCFC91ED82FCEFA723", "snils": "000-000-600 01",
        "stateFacts": ["EntityRoot"],
        "gender": "F",
        "trusted": True
    },
    "person_contacts": [{
        "vrfStu": "VERIFIED",
        "value": "EsiaTest001@yandex.ru",
        "eTag": "EC3E57C01CFEC3C3AE0847005F1A39228C088700",
        "stateFacts": ["Identifiable"],
        "type": "EML",
        "id": 14239100
    }],
    "person_addresses": [{
        "city": "Воронеж Город",
        "countryId": "RUS",
        "fiasCode": "36-0-000-001-000-000-0856-0000-000",
        "house": "23 \"a\"",
        "region": "Воронежская Область",
        "zipCode": "369000",
        "addressStr": "Воронежская область, Воронеж город, Станкевича улица",
        "eTag": "A476F27783D0A6DA3B4E270CF3B71701BE5E57FA",
        "street": "Станкевича Улица",
        "stateFacts": ["Identifiable"],
        "type": "PLV",
        "id": 15842
    }]
}


def _create_or_update_ruslan_user(grs_user_record):
    portal_client = connection_pool.get_client(RUSLAN_API_ADDRESS, RUSLAN_API_USERNAME, RUSLAN_API_PASSWORD)
    response = portal_client.create_grs(grs_user_record, RUSLAN_USERS_DATABASE)
    grs_record = response.get('content', [{}])[0]
    record = grs.Record.from_dict(grs_record)

    fields_1 = record.get_field('1')
    record_id = ''

    if fields_1:
        record_id = fields_1[0].content

    if not record_id:
        raise ValueError('record_id must be not empty')

    fields_100 = record.get_field('100')

    if not fields_100:
        field_100 = grs.Field('100')
        record.add_field(field_100)
    else:
        field_100 = fields_100[0]

    fields_115 = grs_user_record.get_field('115')
    if fields_115:
        exist_fields_115 = record.get_field('115')
        if not exist_fields_115:
            record.add_field(fields_115[0])

    field_100.content = RUSLAN_ID_MASK[:len(record_id) * -1] + record_id
    portal_client.update_grs(grs_record=record, database=RUSLAN_USERS_DATABASE, id=record_id)
    return record


def _error_response(request, error, state, error_description, exception=None):
    if exception:
        logger.exception(exception)
    else:
        logger.error(u'%s: %s' % (error, error_description))

    return render(request, 'esia_sso/error.html', {
        'error': error,
        'state': state,
        'error_description': error_description
    })


@transaction.atomic()
def redirect_from_idp(request):
    error = request.GET.get('error')
    state = request.GET.get('state')
    code = request.GET.get('code')
    error_description = request.GET.get('error_description')

    if error:
        return _error_response(
            request=request,
            error=error,
            state=state,
            error_description=error_description
        )

    try:
        access_marker = _get_access_marker(code)
    except Exception as e:
        return _error_response(
            request=request,
            error='get_access_marker',
            state=state,
            error_description=u'При получении маркера возникла ошибка',
            exception=e
        )

    access_token = access_marker.get('access_token', '')

    if not access_token:
        return _error_response(
            request=request,
            error='no_access_toke',
            state=state,
            error_description=u'Авторизационный код доступа не был получен'
        )

    try:
        oid = _get_oid(access_token)
    except Exception as e:
        return _error_response(
            request=request,
            error='get_oid',
            state=state,
            error_description=u'Ошибка при получении oid',
            exception=e
        )

    if not oid:
        return _error_response(
            request=request,
            error='no_oid',
            state=state,
            error_description=u'oid не был получен'
        )

    try:
        person_info = _get_person_info(oid, access_token)
        person_contacts = _get_person_contacts(oid, access_token)
        person_addresses = _get_person_addresses(oid, access_token)
    except Exception as e:
        return _error_response(
            request=request,
            error='user_info_error',
            state=state,
            error_description=u'Ошибка при получении информации из ЕСИА',
            exception=e
        )

    user_attrs = {
        'person_info': person_info,
        'person_contacts': person_contacts,
        'person_addresses': person_addresses
    }

    portal_client = connection_pool.get_client(RUSLAN_API_ADDRESS, RUSLAN_API_USERNAME, RUSLAN_API_PASSWORD)
    # oid = u'erf'
    # state = '112313'
    # user_attrs = esia_response
    # person_info = user_attrs.get('person_info', {})
    # person_contacts = user_attrs.get('person_contacts', [])


    sru_response = portal_client.search(
        query='@attrset bib-1 @attr 1=403 "%s"' % (oid.replace('\\', '\\\\').replace('"', '\\"'),),
        database=RUSLAN_USERS_DATABASE,
        maximum_records=1
    )

    sru_records = humanize.get_records(sru_response)

    if not sru_records:
        esia_user = models.create_or_update_esia_user(oid, user_attrs)
        return redirect('sso_esia:ask_for_exist_reader', id=esia_user.id)
    else:
        user_grs_record = grs.Record.from_dict(humanize.get_record_content(sru_records[0]))
        fields_100 = user_grs_record.get_field('100')

        if not fields_100:
            return _error_response(
                request=request,
                error='no_user',
                state=state,
                error_description=u'Система в данный момент не может произвести авторизацию'
            )
        else:
            user = authenticate(username=fields_100[0].content, need_check_password=False)
            if user:
                if user.is_active:
                    login(request, user)
                    request.session[
                        'logout_idp_url'] = 'https://esia.gosuslugi.ru/idp/ext/Logout?client_id=%s&redirect_url=http://%s' % (ESIA_SSO_CLIENT_ID, SITE_DOMAIN)
                    return redirect('index:frontend:index')
                else:
                    return _error_response(
                        request=request,
                        error='no_access_toke',
                        state=state,
                        error_description=u'Ваша учетная запись не активна'
                    )
            else:
                return _error_response(
                    request=request,
                    error='no_user',
                    state=state,
                    error_description=u'Система не может сопоставить вашу учетную запись ЕСИА'
                )


@transaction.atomic()
def register_new_user(request, id):
    try:
        esia_user = models.EsiaUser.objects.get(id=id)
    except models.EsiaUser.DoesNotExist:
        return redirect('sso_esia:index')

    user_attrs = json.loads(esia_user.user_attrs)
    person_contacts = user_attrs.get('person_contacts', [])

    portal_client = connection_pool.get_client(RUSLAN_API_ADDRESS, RUSLAN_API_USERNAME, RUSLAN_API_PASSWORD)
    # oid = u'777'
    query = u'@attrset bib-1 @attr 1=403 "%s"' % (esia_user.oid.replace('\\', '\\\\'))
    sru_response = portal_client.search(database=RUSLAN_USERS_DATABASE, query=query, start_record=1, maximum_records=1)
    sru_records = humanize.get_records(sru_response)

    reader_id = ''
    password = ''

    if not sru_records:
        user_grs_record = _create_grs_from_esia(
            oid=esia_user.oid,
            email=(_find_contacts_attr('EML', person_contacts) or [''])[0],
            user_attrs=user_attrs
        )
        fields_115 = user_grs_record.get_field('115')
        if fields_115:
            password = fields_115[0].content
        user_grs_record = _create_or_update_ruslan_user(user_grs_record)

    else:
        user_grs_record = grs.Record.from_dict(humanize.get_record_content(sru_records[0]))

    fields_100 = user_grs_record.get_field('100')

    if fields_100:
        reader_id = fields_100[0].content

    esia_user.delete()

    user = authenticate(username=reader_id, password=password, need_check_password=False)

    if user:
        if user.is_active:
            login(request, user)
            return render(request, 'esia_sso/register_new_user.html', {
                'reader_id': reader_id,
                'password': password
            })
        else:
            return _error_response(
                request=request,
                error='no_access_toke',
                state='',
                error_description=u'Ваша учетная запись не активна'
            )
    else:
        return _error_response(
            request=request,
            error='no_user',
            state='',
            error_description=u'Система не может сопоставить вашу учетную запись ЕСИА'
        )


@transaction.atomic()
def ask_for_exist_reader(request, id):
    try:
        esia_user = models.EsiaUser.objects.get(id=id)
    except models.EsiaUser.DoesNotExist:
        return redirect('sso_esia:index')

    portal_client = connection_pool.get_client(RUSLAN_API_ADDRESS, RUSLAN_API_USERNAME, RUSLAN_API_PASSWORD)

    if request.method == 'POST':
        ruslan_auth_form = forms.RuslanAuthForm(request.POST)
        if ruslan_auth_form.is_valid():
            reader_id = ruslan_auth_form.cleaned_data['reader_id'].replace('\\', '\\\\').replace('"', '\\"')
            password = ruslan_auth_form.cleaned_data['password'].replace('\\', '\\\\').replace('"', '\\"')

            sru_response = portal_client.search(
                query='@attrset bib-1 @attr 1=100 "%s"' % (reader_id,),
                database=RUSLAN_USERS_DATABASE,
                maximum_records=1
            )

            sru_records = humanize.get_records(sru_response)

            if not sru_records:
                ruslan_auth_form.add_error('reader_id', u'Идентификатор читателя не найден')
            else:
                sru_response = portal_client.search(
                    query='@attrset bib-1 @and @attr 1=100 "%s" @attr 1=115 "%s"' % (reader_id, password),
                    database=RUSLAN_USERS_DATABASE,
                    maximum_records=1
                )
                sru_records = humanize.get_records(sru_response)
                if not sru_records:
                    ruslan_auth_form.add_error('reader_id', u'Неверный пароль')
                else:
                    user_record = humanize.get_record_content(sru_records[0])
                    user_grs_record = grs.Record.from_dict(user_record)
                    fields_403 = user_grs_record.get_field('403')

                    if fields_403:
                        if fields_403[0].content != esia_user.oid:
                            ruslan_auth_form.add_error(
                                'reader_id',
                                u'Идентификатор читателя уже связан с учетной записью ЕСИА'
                            )
                    else:
                        user_grs_record.add_field(grs.Field('403', esia_user.oid))
                        portal_client.update_grs(
                            grs_record=user_grs_record,
                            database=RUSLAN_USERS_DATABASE,
                            id=reader_id
                        )
                        esia_user.delete()
                        user = authenticate(
                            username=ruslan_auth_form.cleaned_data['reader_id'],
                            password=ruslan_auth_form.cleaned_data['password']
                        )
                        if user:
                            if user.is_active:
                                login(request, user)
                                return redirect('index:frontend:index')
                            else:
                                return _error_response(
                                    request=request,
                                    error='no_access_toke',
                                    state='',
                                    error_description=u'Ваша учетная запись читателя не активна'
                                )
                        else:
                            return _error_response(
                                request=request,
                                error='no_user',
                                state='',
                                error_description=u'Система не может сопоставить вашу учетную запись ЕСИА'
                            )
    else:
        ruslan_auth_form = forms.RuslanAuthForm()

    return render(request, 'esia_sso/ask_for_exist_reader.html', {
        'ruslan_auth_form': ruslan_auth_form,
        'esia_id': id
    })


def _find_contacts_attr(type_name, contacts, only_verified=False):
    values = []
    for contact in contacts:
        contact_type = contact.get('type', '')
        contact_value = contact.get('value', '')
        contact_vrfsu = contact.get('vrfStu', '')
        if contact_type and contact_type == type_name and contact_value:
            if only_verified and contact_vrfsu != 'VERIFIED':
                continue
            values.append(contact_value)
    return values


def decode_base64(data):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += b'=' * missing_padding
    return base64.decodestring(data)


def _get_oid(access_token):
    access_token_parts = access_token.replace('-', '+').replace('_', '/').replace(',', '=').split('.')

    if len(access_token_parts) < 3:
        return ''

    access_token_json = decode_base64(access_token_parts[1])

    access_token_params = json.loads(access_token_json)
    access_token_scope = access_token_params.get('scope', '')
    oid_prefix = 'oid='
    oid_index = access_token_scope.find(oid_prefix)

    if oid_index < 0:
        return ''

    oid = access_token_scope[oid_index + len(oid_prefix):]
    return oid


def _get_person_info(oid, access_token):
    """
    :param oid:
    :param access_token:
    :return: {
        "status": "REGISTERED",
        "birthPlace": "",
        "citizenship": "",
        "firstName": "",
        "updatedOn": 1438692792,
        "middleName": "",
        "lastName": "",
        "birthDate": "07.01.1994",
        "eTag": "42D905D3CBEF2F2DC9FF85CCFC91ED82FCEFA723",
        "snils": "000-000-600 01",
        "stateFacts": ["EntityRoot"],
        "gender": "F|M",
        "trusted": False
    }
    """
    person_response = requests.get(ESIA_SSO_PERSON_URL + '/' + oid, headers={
        'Authorization': 'Bearer ' + access_token
    }, verify=VERIFY_REQUESTS)
    person_response.raise_for_status()
    return person_response.json()


def _get_person_contacts(oid, access_token):
    """
    :param oid:
    :param access_token:
    :return:
    [
        {
        "vrfStu": "VERIFIED",
        "value": "EsiaTest001@yandex.ru",
        "eTag": "EC3E57C01CFEC3C3AE0847005F1A39228C088700",
        "stateFacts": ["Identifiable"],
        "type": "EML",
        "id": 14239100
        }
    ]
    """
    response = requests.get('%s/%s/%s' % (ESIA_SSO_PERSON_URL, oid, PERSON_CONTACTS_URL_SUFFIX), headers={
        'Authorization': 'Bearer ' + access_token
    }, verify=VERIFY_REQUESTS)
    response.raise_for_status()

    response_dict = response.json()

    contact = []
    for element in response_dict['elements']:
        response = requests.get(element, headers={
            'Authorization': 'Bearer ' + access_token
        }, verify=VERIFY_REQUESTS)
        response.raise_for_status()
        contact.append(response.json())
    return contact


def _get_person_addresses(oid, access_token):
    """
    :param oid:
    :param access_token:
    :return:
    [
        {
            "city": "Воронеж Город",
            "countryId": "RUS",
            "fiasCode": "36-0-000-001-000-000-0856-0000-000",
            "house": "23 \"a\"",
            "region": "Воронежская Область",
            "zipCode": "369000",
            "addressStr": "Воронежская область, Воронеж город, Станкевича улица",
            "eTag": "A476F27783D0A6DA3B4E270CF3B71701BE5E57FA",
            "street": "Станкевича Улица",
            "stateFacts": ["Identifiable"],
            "type": "PLV",
            "id": 15842
        }
    ]
    """
    response = requests.get('%s/%s/%s' % (ESIA_SSO_PERSON_URL, oid, PERSON_ADDRESS_URL_SUFFIX), headers={
        'Authorization': 'Bearer ' + access_token
    }, verify=VERIFY_REQUESTS)
    response.raise_for_status()
    response_dict = response.json()

    adresses = []
    for element in response_dict['elements']:
        response = requests.get(element, headers={
            'Authorization': 'Bearer ' + access_token
        }, verify=VERIFY_REQUESTS)
        response.raise_for_status()
        adresses.append(response.json())

    return adresses


def _get_access_marker(code):
    timestamp = unicode(datetime.now().strftime('%Y.%m.%d %H:%M:%S +0300'))
    state = unicode(uuid.uuid4())
    client_secret = _get_client_secret(ESIA_SSO_SCOPE, timestamp, ESIA_SSO_CLIENT_ID, state)
    response = requests.post(ESIA_SSO_ACCESS_MARKER_URL, data={
        'code': code,
        'client_id': ESIA_SSO_CLIENT_ID,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'state': state,
        'scope': ESIA_SSO_SCOPE,
        'refresh_token': state,
        'redirect_uri': REDIRECT_URI,
        'token_type': 'Bearer',
        'timestamp': timestamp

    }, verify=VERIFY_REQUESTS)
    response.raise_for_status()
    return response.json()


def _get_client_secret(scope, timestamp, client_id, state):
    signed_data = (scope + timestamp + client_id + state).encode('utf-8')
    data_file_path = os.path.join(ESIA_SSO_TMP_DIR, state + '.esia')
    signed_file_path = os.path.join(ESIA_SSO_TMP_DIR, state + '.esia.sign')
    data_file = open(data_file_path, mode='w')
    data_file.write(signed_data)
    data_file.close()
    command = '/opt/cprocsp/bin/amd64/cryptcp -pin ' + ESIA_SSO_CERT_PASSWORD + u' -sign -nochain -dn \'OGRN=1091690014712, INN=001655174024, E=nebrt@tatar.ru, C=RU, S=16 Республика Татарстан, L=Казань, O="ГУП ""Центр информационных технологий РТ""", CN=kitap.tatar.ru, STREET="Петербургская ул, 52"\' -q ' + data_file_path + ' ' + signed_file_path
    os.system(
        command.encode('utf-8')
    )
    sign_file = open(signed_file_path)
    sign = sign_file.read().decode('utf-8')
    sign = sign.replace('+', '-').replace('/', '_').replace('=', ',')
    os.unlink(data_file_path)
    os.unlink(signed_file_path)
    return sign
