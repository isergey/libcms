# coding=utf-8
import os
import uuid
from datetime import datetime
import requests
from django.conf import settings
from django.db import transaction
from django.shortcuts import render, redirect, resolve_url, HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User, Group

ESIA_SSO = getattr(settings, 'ESIA_SSO', {})
TMP_DIR = ESIA_SSO.get('tmp_dir', '/tmp')
JAR_CERT_GENERATOR = ESIA_SSO.get('jar_cert_generator')
CERT_ALIAS = ESIA_SSO.get('cert_alias', 'RaUser-561d2f13-c72b-4018-a473-48017a4622d2')
CERT_PASSWORD= ESIA_SSO.get('cert_password', '1234567890')

CLIENT_ID = unicode(ESIA_SSO.get('client_id', ''))
SCOPE = unicode(ESIA_SSO.get('scope', 'http://esia.gosuslugi.ru/openid'))
ACCESS_TOKEN_URL = ESIA_SSO.get('access_token_url', 'https://esia-portal1.test.gosuslugi.ru/aas/oauth2/ac')
RESPONSE_TYPE = 'code'
# KITAP_TATAR_API_BASE_ADDRESS = getattr(settings, 'KITAP_TATAR_API_BASE_ADDRESS', 'http://127.0.0.1')



def index(request):
    timestamp = unicode(request.POST.get('timestamp', datetime.now().strftime('%Y.%m.%d %H:%M:%S +0300')))
    state = request.POST.get('state', unicode(uuid.uuid4()))
    client_secret = _get_client_secret(SCOPE, timestamp, CLIENT_ID, state)
    return render(request, 'esia_sso/index.html', {
        'client_id': CLIENT_ID,
        'scope': SCOPE,
        'response_type': RESPONSE_TYPE,
        'timestamp': timestamp,
        'state': state,
        'client_secret': client_secret,
        'access_token_url': ACCESS_TOKEN_URL
    })


def redirect(request):

    return HttpResponse(u'Ok')


def _get_client_secret(scope, timestamp, client_id, state):
    signed_data = (scope + timestamp + client_id + state).encode('utf-8')
    data_file_path = os.path.join(TMP_DIR, state + '.esia')
    signed_file_path = data_file_path + '.signed'
    data_file = open(data_file_path, mode='w')
    data_file.write(signed_data)
    data_file.close()
    os.system(
        "java -jar %s -alias %s -password %s -file %s -sign %s" % (
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