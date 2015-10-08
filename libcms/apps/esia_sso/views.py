# coding=utf-8
import os
import json
import uuid
from datetime import datetime
import requests
import base64
import logging
from django.conf import settings
from django.db import transaction
from django.shortcuts import render, redirect, resolve_url, HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User, Group

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

RESPONSE_TYPE = 'code'
REDIRECT_URI = 'https://kitap.tatar.ru/esia_sso/redirect'


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


def redirect(request):
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
            error_description='No access token in access_marker'
        )

    try:
        oid = _get_oid(access_token)
    except Exception as e:
        return _error_response(
            request=request,
            error='get_oid',
            state=state,
            error_description=u'Error while get oid',
            exception=e
        )

    if not oid:
        return _error_response(
            request=request,
            error='no_oid',
            state=state,
            error_description='No oid in access token'
        )

    person_info = _get_person_info(oid, access_token)
    person_contacts = _get_person_contact(oid, access_token)

    resp = {
        'person_info': person_info,
        'person_contacts': person_contacts
    }
    return HttpResponse(json.dumps(resp, ensure_ascii=False))


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
    })
    person_response.raise_for_status()
    return person_response.json()


def _get_person_contact(oid, access_token):
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
    response = requests.get('%s/%s/%s' % (PERSON_URL, oid, PERSON_CONTACTS_URL_SUFFIX), headers={
        'Authorization': 'Bearer ' + access_token
    })
    response.raise_for_status()
    return response.json()


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

    }, verify=False)

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
    #
    #
    # @transaction.atomic()
    # def index(request):
    #     now = datetime.now().strftime('%Y.%m.%d %H:%M:%S +0400')
    #     state = unicode(uuid.uuid4())
    #     redirect_url = request.GET.get('redirect_url', settings.LOGIN_REDIRECT_URL)
    #     access_token_address = ACCESS_TOKEN_URL
    #     client_id = CLIENT_ID
    #     client_secret = _get_client_secret(state)
    #     code = request.GET.get('code', '')
    #     errors = []
    #
    #     if not code:
    #         return HttpResponse(u'Необходимо заново начать процедуру аутентификации Oauth')
    #
    #     response = requests.post(access_token_address, data={
    #         'code': code,
    #         'client_id': client_id,
    #         'client_secret': client_secret,
    #         'redirect_uri': _get_redirect_uri(request)
    #     }, verify=False)
    #
    #     try:
    #         response.raise_for_status()
    #     except requests.HTTPError as e:
    #         errors.append(e.message)
    #
    #     response_dict = response.json()
    #
    #     if errors:
    #         return render(request, 'oauth2/index.html', {
    #             'errors': errors
    #         })
    #
    #     access_token = response_dict.get('access_token')
    #
    #     user_organizations_response = requests.get(KITAP_TATAR_API_BASE_ADDRESS + u'/participants/api/user_organizations/', headers={
    #         'Authorization': 'token ' + access_token
    #     }, verify=False)
    #
    #     user_organizations_response.raise_for_status()
    #
    #     user_organizations = user_organizations_response.json()
    #
    #     if not user_organizations:
    #         return HttpResponse(u'Вы не являетесь сотрудником. Если Вы считаете это ошибкой, обратитесь к администратору.')
    #
    #     user_info_response = requests.get(KITAP_TATAR_API_BASE_ADDRESS + u'/accounts/api/user/', headers={
    #         'Authorization': 'token ' + access_token
    #     }, verify=False)
    #
    #     personal_cabinet_links_response = requests.get(KITAP_TATAR_API_BASE_ADDRESS + u'/participants/api/personal_cabinet_links/', headers={
    #         'Authorization': 'token ' + access_token
    #     }, verify=False)
    #
    #     personal_cabinet_links_response.raise_for_status()
    #
    #     personal_cabinet_links = personal_cabinet_links_response.json()
    #
    #     users_list = user_info_response.json()
    #     if users_list:
    #         user_fields = users_list[0]['fields']
    #         try:
    #             user = User.objects.get(username=user_fields['username'])
    #         except User.DoesNotExist:
    #             user = User(
    #                 username=user_fields['username'],
    #                 password=user_fields.get('password', u''),
    #                 email=user_fields.get('email', u''),
    #                 first_name=user_fields.get('first_name', u''),
    #                 last_name=user_fields.get('last_name', u''),
    #                 last_login=datetime.now(),
    #                 is_active=True,
    #                 is_staff=True
    #             )
    #             user.save()
    #             try:
    #                 g = Group.objects.get(name='users')
    #                 g.user_set.add(user)
    #             except Group.DoesNotExist:
    #                 pass
    #
    #
    #     user = auth.authenticate(user_model=user)
    #
    #     if user:
    #         request.user = user
    #         auth.login(request, user)
    #         request.session['access_token'] = access_token
    #         request.session['personal_cabinet_links'] = personal_cabinet_links
    #         request.session['organizations'] = user_organizations
    #         return redirect(redirect_url)
    #
    #     return HttpResponse(
    #         u'Аутентификация не завершена. Попробуйте начать процесс входа заново или обратитесь к администратору.')
    #
    #
    # def login(request):
    #     if not OAUTH2_URL:
    #         return render(request, 'oauth2/error.html')
    #
    #     redirect_uri = _get_redirect_uri(request)
    #     authorize_address = OAUTH2_URL.get('authorize_address')
    #     client_id = OAUTH2_URL.get('client_id')
    #     redirect_url = u'%s?client_id=%s&redirect_uri=%s' % (authorize_address, client_id, redirect_uri)
    #     return redirect(redirect_url)
    #
    #
    # def _get_redirect_uri(request):
    #     redirect_uri = u'%s://%s%s' % (request.scheme, request.get_host(), resolve_url('oauth2:index'))
    #     return redirect_uri
    #
    #
    # def _get_client_secret():
    #     return  ''
