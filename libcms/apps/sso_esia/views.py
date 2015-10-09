# coding=utf-8
import os
import json
import uuid
from datetime import datetime
import base64
import logging

import requests
from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login
from sso import models as sso_models
from . import models

AUTH_SOURCE = 'esia'

ESIA_SSO = getattr(settings, 'ESIA_SSO', {})
TMP_DIR = ESIA_SSO.get('tmp_dir', '/tmp')
JAR_CERT_GENERATOR = ESIA_SSO.get('jar_cert_generator')
CERT_ALIAS = ESIA_SSO.get('cert_alias', 'RaUser-561d2f13-c72b-4018-a473-48017a4622d2')
CERT_PASSWORD = ESIA_SSO.get('cert_password', '1234567890')

CLIENT_ID = unicode(ESIA_SSO.get('client_id', ''))
SCOPE = unicode(ESIA_SSO.get('scope', 'http://esia.gosuslugi.ru/usr_inf'))
ACCESS_TOKEN_URL = ESIA_SSO.get('access_token_url', 'https://esia-portal1.test.gosuslugi.ru/aas/oauth2/ac')
ACCESS_MARKER_URL = ESIA_SSO.get('access_marker_url', 'https://esia-portal1.test.gosuslugi.ru/aas/oauth2/te')
PERSON_URL = ESIA_SSO.get('person_url', 'https://esia-portal1.test.gosuslugi.ru/rs/prns')
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
    client_secret = _get_client_secret(SCOPE, timestamp, CLIENT_ID, state)
    return render(request, 'esia_sso/index.html', {
        'access_type': 'offline',
        'client_id': CLIENT_ID,
        'scope': SCOPE,
        'response_type': RESPONSE_TYPE,
        'timestamp': timestamp,
        'state': state,
        'client_secret': client_secret,
        'access_token_url': ACCESS_TOKEN_URL
    })


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


def redirect_from_ip(request):
    error = request.GET.get('error')
    state = request.GET.get('state')
    error_description = request.GET.get('error_description')
    if error:
        return _error_response(
            request=request,
            error=error,
            state=state,
            error_description=error_description
        )

    code = request.GET.get('code')
    state = request.GET.get('state')

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


    external_user = sso_models.create_or_update_external_user(
        external_username=oid,
        auth_source=AUTH_SOURCE,
        first_name=person_info.get('firstName', ''),
        last_name=person_info.get('lastName', ''),
        email=(_find_contacts_attr('EML', person_contacts) or [''])[0],
        attributes=user_attrs,
        is_active=(person_info.get('status', '') == 'REGISTERED')
    )

    user = authenticate(user_model=external_user.user)

    if user:
        if user.is_active:
            login(request, user)
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


def _get_oid(access_token):
    access_token_parts = access_token.split('.')

    if len(access_token_parts) < 3:
        return ''

    access_token_json = base64.urlsafe_b64decode(access_token_parts[1].encode('utf-8'))
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
    person_response = requests.get(PERSON_URL + '/' + oid, headers={
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
    response = requests.get('%s/%s/%s' % (PERSON_URL, oid, PERSON_CONTACTS_URL_SUFFIX), headers={
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
    response = requests.get('%s/%s/%s' % (PERSON_URL, oid, PERSON_ADDRESS_URL_SUFFIX), headers={
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
    client_secret = _get_client_secret(SCOPE, timestamp, CLIENT_ID, state)
    response = requests.post(ACCESS_MARKER_URL, data={
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'state': state,
        'scope': SCOPE,
        'refresh_token': state,
        'redirect_uri': REDIRECT_URI,
        'token_type': 'Bearer',
        'timestamp': timestamp

    }, verify=VERIFY_REQUESTS)

    response.raise_for_status()
    return response.json()


def _get_client_secret(scope, timestamp, client_id, state):
    signed_data = (scope + timestamp + client_id + state).encode('utf-8')
    data_file_path = os.path.join(TMP_DIR, state + '.esia')
    signed_file_path = data_file_path + '.signed'
    data_file = open(data_file_path, mode='w')
    data_file.write(signed_data)
    data_file.close()
    os.system(
        'java -jar "%s" -alias "%s" -password "%s" -file "%s" -sign "%s"' % (
            JAR_CERT_GENERATOR,
            CERT_ALIAS,
            CERT_PASSWORD,
            data_file_path,
            signed_file_path
        )
    )
    sign_file = open(signed_file_path)
    sign = sign_file.read().decode('utf-8')
    os.unlink(data_file_path)
    os.unlink(signed_file_path)
    return sign
