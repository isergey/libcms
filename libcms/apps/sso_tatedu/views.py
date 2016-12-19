# -*- coding: utf-8 -*-
import requests
import json
import logging
import os
from datetime import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.shortcuts import render, redirect

from sso.utils import normalize_fio
from ruslan import connection_pool, humanize
from ruslan import grs
from participants.models import Library

from . import models

SITE_DOMAIN = getattr(settings, 'SITE_DOMAIN', 'esia.gosuslugi.ru')
RUSLAN = getattr(settings, 'RUSLAN', {})

RUSLAN_API_ADDRESS = RUSLAN.get('api_address', 'http://localhost/')
RUSLAN_API_USERNAME = RUSLAN.get('username')
RUSLAN_API_PASSWORD = RUSLAN.get('password')
RUSLAN_USERS_DATABASE = RUSLAN.get('users_database', 'allusers')
RUSLAN_ID_MASK = RUSLAN.get('id_mask', '000000000')

AUTH_SOURCE = 'tatedu'
PASSWORD_LENGTH = 8

# PERSON_CONTACTS_URL_SUFFIX = 'ctts'
# PERSON_ADDRESS_URL_SUFFIX = 'addrs'
# PERSON_DOCS_URL_SUFFIX = 'docs'

RESPONSE_TYPE = 'code'

VERIFY_REQUESTS = False

# KITAP_TATAR_API_BASE_ADDRESS = getattr(settings, 'KITAP_TATAR_API_BASE_ADDRESS', 'http://127.0.0.1')

SSO_TATEDU = getattr(settings, 'SSO_TATEDU', {})
CLIENT_ID = SSO_TATEDU.get('client_id', '')
SECRET = SSO_TATEDU.get('secret', '')
AUTH_URL = SSO_TATEDU.get('authorize_url', '')
TOKEN_URL = SSO_TATEDU.get('token_url', '')
USER_INFO_URL = SSO_TATEDU.get('user_info_url', '')
LOGOUT_URL = 'https://edu.tatar.ru/logoff'
OID_FIELD = '507'

logger = logging.getLogger('sso_tatedu')


def index(request):
    return render(request, 'sso_tatedu/index.html', {
        'auth_url': AUTH_URL,
        'client_id': CLIENT_ID,
    })


def _generate_password(length=PASSWORD_LENGTH):
    if not isinstance(length, int) or length < PASSWORD_LENGTH:
        raise ValueError("temp password must have positive length")
    chars = "ABCDEFGHJKMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz123456789"
    return "".join([chars[ord(c) % len(chars)] for c in os.urandom(length)])


# def _generate_registraion_address(person_address):
#     registration_address_parts = []
#
#     def add_to_registration_address(item):
#         if not item:
#             return
#         registration_address_parts.append(item.strip())
#
#     add_to_registration_address(person_address.get('region', ''))
#     add_to_registration_address(person_address.get('city', ''))
#     add_to_registration_address(person_address.get('street', ''))
#     add_to_registration_address(person_address.get('house', ''))
#
#     flat = person_address.get('flat', '')
#     if flat:
#         flat = u'кв. ' + flat
#         add_to_registration_address(flat)
#
#     return ', '.join(registration_address_parts)

#
# def _generate_region_city(person_address):
#     region_city_parts = []
#     region = person_address.get('region', '')
#     city = person_address.get('city', '')
#
#     if region:
#         region_city_parts.append(region)
#     if city:
#         region_city_parts.append(city)
#     return ' / '.join(region_city_parts)


def _create_grs_from_user(oid, email='', user_attrs=None):
    user_attrs = user_attrs or {}
    gender_map = {
        'male': u'М',
        'female': u'Ж'
    }

    person_info = user_attrs.get('person_info', {})
    # person_contacts = user_attrs.get('person_contacts', {})
    # person_addresses = user_attrs.get('person_addresses', [])
    # rf_passports = filter(lambda doc: doc['type'] == 'RF_PASSPORT' and 'Identifiable' in doc['stateFacts'],
    #                       user_attrs.get('person_docs', []))
    # reg_address = {}
    # prozhiv_address = {}
    #
    # for person_address in person_addresses:
    #     if person_address.get('type', '') == 'PRG':
    #         reg_address = person_address
    #     elif person_address.get('type', '') == 'PLV':
    #         prozhiv_address = person_address

    # phone_contact = {}
    # for person_contact in person_contacts:
    #     if person_contact.get('type', '') == 'MBT':
    #         phone_contact = person_contact

    # foreigner = u''
    # citizenship = person_info.get('citizenship', '').lower()
    #
    # if citizenship:
    #     if citizenship == 'rus':
    #         foreigner = u'0'
    #     else:
    #         foreigner = u'1'

    birth_date = person_info.get('birth_year', '')
    if birth_date:
        birth_date += '0101'

    record = grs.Record()

    def add_field_to_record(tag, value):
        if not value:
            return
        record.add_field(grs.Field(tag, value))

    add_field_to_record('101', normalize_fio(person_info.get('lname', '')))
    add_field_to_record('102', normalize_fio(person_info.get('fname', '')))
    add_field_to_record('103', normalize_fio(person_info.get('pname', '')))
    add_field_to_record('105', datetime.now().strftime('%Y%m%d'))
    add_field_to_record('115', _generate_password())
    # add_field_to_record('120', phone_contact.get('value', ''))
    # add_field_to_record('121', _generate_registraion_address(prozhiv_address))
    add_field_to_record('122', email)
    # add_field_to_record('130', _generate_registraion_address(reg_address))
    add_field_to_record('234', birth_date)
    # add_field_to_record('402', person_info.get('snils', ''))
    add_field_to_record(OID_FIELD, oid)
    add_field_to_record('404', gender_map.get(person_info.get('gender', '').lower(), u''))

    organisations = person_info.get('organizations', [])
    for organisation in organisations:
        add_field_to_record('505', unicode(organisation.get('id', '')))
        add_field_to_record('506', unicode(organisation.get('region', {}).get('id')))
    # if rf_passports:
    #     rf_passport = rf_passports[-1]
    #     add_field_to_record('417', u'Паспорт')
    #     add_field_to_record('418', rf_passport.get('series', ''))
    #     add_field_to_record('419', rf_passport.get('number', ''))
    #     add_field_to_record('420', rf_passport.get('issuedBy', ''))
    #     issue_date_parts = rf_passport.get('issueDate', '').split('.')
    #     issue_date = ''
    #     if len(issue_date_parts) == 3:
    #         issue_date = issue_date_parts[2] + issue_date_parts[1] + issue_date_parts[0]
    #     add_field_to_record('421', issue_date)
    #     add_field_to_record('422', rf_passport.get('issueId', ''))
    #
    # add_field_to_record('423', reg_address.get('zipCode', ''))
    # add_field_to_record('424', _generate_region_city(reg_address))
    # add_field_to_record('425', prozhiv_address.get('zipCode', ''))
    # add_field_to_record('426', _generate_region_city(prozhiv_address))
    # add_field_to_record('427', foreigner)
    add_field_to_record('501', '3')

    # Trusted
    # add_field_to_record('502', '1')
    # add_field_to_record('503', '1')

    return record


def _create_or_update_ruslan_user(grs_user_record):
    portal_client = connection_pool.get_client(RUSLAN_API_ADDRESS, RUSLAN_API_USERNAME, RUSLAN_API_PASSWORD)
    response = portal_client.create_grs(grs_user_record, RUSLAN_USERS_DATABASE)
    record = grs.Record.from_dict(response)

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
        person_info_resp = _get_person_info(access_token)
        # print person_info_resp
        # person_contacts = _get_person_contacts(oid, access_token)
        # person_addresses = _get_person_addresses(oid, access_token)
        # person_docs = _get_person_docs(oid, access_token)
    except Exception as e:
        return _error_response(
            request=request,
            error='user_info_error',
            error_description=u'Ошибка при получении информации из ЭО РТ',
            exception=e
        )

    if person_info_resp.get('status', '') != 'success':
        return _error_response(
            request=request,
            error='user_info_error',
            error_description=u'Ошибка при получении информации из ЭО РТ ' + person_info_resp.get('message')
        )
    # return HttpResponse(json.dumps(person_info_resp, ensure_ascii=False), content_type='application/json')
    person_info = person_info_resp.get('data', {})

    if person_info.get('status', '') != 'active':
        return _error_response(
            request=request,
            error='user_not_active',
            error_description=u'Учетная запись неактивна. Обратитесь к администратору портала ЭО'
        )

    user_id = person_info.get('id')

    if not user_id:
        return _error_response(
            request=request,
            error='no_user_id',
            error_description=u'Ответ не содержит идентификатор пользователя'
        )

    user_attrs = {
        'person_info': person_info,
        # 'person_contacts': person_contacts,
        # 'person_addresses': person_addresses,
        # 'person_docs': person_docs,
    }

    portal_client = connection_pool.get_client(RUSLAN_API_ADDRESS, RUSLAN_API_USERNAME, RUSLAN_API_PASSWORD)
    # oid = u'erf'
    # state = '112313'
    # user_attrs = esia_response
    # person_info = user_attrs.get('person_info', {})
    # person_contacts = user_attrs.get('person_contacts', [])


    sru_response = portal_client.search(
        query=u'@attrset bib-1 @attr 1=%s "%s"' % (
        OID_FIELD, unicode(user_id).replace('\\', '\\\\').replace('"', '\\"'),),
        database=RUSLAN_USERS_DATABASE,
        maximum_records=1
    )

    sru_records = humanize.get_records(sru_response)
    if not sru_records:
        tatedu_user = models.create_or_update_user(user_id, user_attrs)
        return register_new_user(request, tatedu_user.id)
    else:
        user_grs_record = grs.Record.from_dict(humanize.get_record_content(sru_records[0]))
        fields_100 = user_grs_record.get_field('100')
        if not fields_100:
            return _error_response(
                request=request,
                error='no_user',
                error_description=u'Система в данный момент не может произвести авторизацию'
            )
        else:
            user = authenticate(username=fields_100[0].content, need_check_password=False)
            if user:
                if user.is_active:
                    login(request, user)
                    library_id = _get_library_id(user_grs_record)
                    if library_id:
                        request.session['org_id'] = library_id
                    request.session['logout_idp_url'] = LOGOUT_URL
                    request.session['auth_source'] = AUTH_SOURCE
                    return redirect('index:frontend:index')
                else:
                    return _error_response(
                        request=request,
                        error='no_access_token',
                        state=state,
                        error_description=u'Ваша учетная запись не активна'
                    )
            else:
                return _error_response(
                    request=request,
                    error='no_user',
                    state=state,
                    error_description=u'Система не может сопоставить вашу учетную запись ЭО РТ'
                )
                # """
                # return HttpResponse(json.dumps(person_info, ensure_ascii=False), content_type='application/json')


@transaction.atomic()
def register_new_user(request, id):
    try:
        tatedu_user = models.TatEduUser.objects.get(id=id)
    except models.TatEduUser.DoesNotExist:
        return redirect('sso_tatedu:index')

    user_attrs = json.loads(tatedu_user.user_attrs)
    person_info = user_attrs.get('person_info', {})

    portal_client = connection_pool.get_client(RUSLAN_API_ADDRESS, RUSLAN_API_USERNAME, RUSLAN_API_PASSWORD)
    # oid = u'777'
    query = u'@attrset bib-1 @attr 1=%s "%s"' % (OID_FIELD, tatedu_user.oid.replace('\\', '\\\\'))
    sru_response = portal_client.search(database=RUSLAN_USERS_DATABASE, query=query, start_record=1, maximum_records=1)
    sru_records = humanize.get_records(sru_response)

    reader_id = ''
    password = ''

    if not sru_records:
        user_grs_record = _create_grs_from_user(
            oid=tatedu_user.oid,
            email=person_info.get('email', ''),
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

    # tatedu_user.delete()

    user = authenticate(username=reader_id, password=password, need_check_password=False)

    if user:
        if user.is_active:
            login(request, user)
            request.session[
                'logout_idp_url'] = LOGOUT_URL
            return render(request, 'sso_tatedu/register_new_user.html', {
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
            error_description=u'Система не может сопоставить вашу учетную запись ОЭ РТ'
        )


#
# @transaction.atomic()
# def ask_for_exist_reader(request, id):
#     try:
#         esia_user = models.EsiaUser.objects.get(id=id)
#     except models.EsiaUser.DoesNotExist:
#         return redirect('sso_esia:index')
#
#     portal_client = connection_pool.get_client(RUSLAN_API_ADDRESS, RUSLAN_API_USERNAME, RUSLAN_API_PASSWORD)
#
#     if request.method == 'POST':
#         ruslan_auth_form = forms.RuslanAuthForm(request.POST)
#         if ruslan_auth_form.is_valid():
#             reader_id = ruslan_auth_form.cleaned_data['reader_id'].replace('\\', '\\\\').replace('"', '\\"')
#             password = ruslan_auth_form.cleaned_data['password'].replace('\\', '\\\\').replace('"', '\\"')
#
#             sru_response = portal_client.search(
#                 query='@attrset bib-1 @attr 1=100 "%s"' % (reader_id,),
#                 database=RUSLAN_USERS_DATABASE,
#                 maximum_records=1
#             )
#
#             sru_records = humanize.get_records(sru_response)
#
#             if not sru_records:
#                 ruslan_auth_form.add_error('reader_id', u'Идентификатор читателя не найден')
#             else:
#                 sru_response = portal_client.search(
#                     query='@attrset bib-1 @and @attr 1=100 "%s" @attr 1=115 "%s"' % (reader_id, password),
#                     database=RUSLAN_USERS_DATABASE,
#                     maximum_records=1
#                 )
#                 sru_records = humanize.get_records(sru_response)
#                 if not sru_records:
#                     ruslan_auth_form.add_error('reader_id', u'Неверный пароль')
#                 else:
#                     user_record = humanize.get_record_content(sru_records[0])
#                     user_grs_record = grs.Record.from_dict(user_record)
#                     fields_403 = user_grs_record.get_field('403')
#
#                     if fields_403:
#                         if fields_403[0].content != esia_user.oid:
#                             ruslan_auth_form.add_error(
#                                 'reader_id',
#                                 u'Идентификатор читателя уже связан с учетной записью ЭО РТ'
#                             )
#                     else:
#                         user_grs_record.add_field(grs.Field('403', esia_user.oid))
#                         portal_client.update_grs(
#                             grs_record=user_grs_record,
#                             database=RUSLAN_USERS_DATABASE,
#                             id=reader_id
#                         )
#                         esia_user.delete()
#                         user = authenticate(
#                             username=ruslan_auth_form.cleaned_data['reader_id'],
#                             password=ruslan_auth_form.cleaned_data['password']
#                         )
#                         if user:
#                             if user.is_active:
#                                 login(request, user)
#                                 return redirect('index:frontend:index')
#                             else:
#                                 return _error_response(
#                                     request=request,
#                                     error='no_access_toke',
#                                     state='',
#                                     error_description=u'Ваша учетная запись читателя не активна'
#                                 )
#                         else:
#                             return _error_response(
#                                 request=request,
#                                 error='no_user',
#                                 state='',
#                                 error_description=u'Система не может сопоставить вашу учетную запись ЭО РТ'
#                             )
#     else:
#         ruslan_auth_form = forms.RuslanAuthForm()
#
#     return render(request, 'esia_sso/ask_for_exist_reader.html', {
#         'ruslan_auth_form': ruslan_auth_form,
#         'esia_id': id
#     })


def _get_person_info(access_token):
    """
    :param access_token:
    :return: {
      "status": "success",
      "message": "",
      "data": {
        "status": "active",
        "organizations": [
          {
            "region": {
              "of_kazan": true,
              "ate_code": "159",
              "id": 48,
              "title": "Приволжский"
            },
            "title_short": "МБОУ \"Школа\"",
            "id": 2298,
            "title": "Муниципальное бюджетное общеобразовательное учреждение"
          }
        ],
        "gender": "male",
        "email": "1236@edu.tatar.ru",
        "lname": "Ф",
        "pname": "О",
        "fname": "И",
        "id": 123213,
        "birth_year": "2001"
      }
    }
    """
    person_response = requests.get(USER_INFO_URL, headers={
        'Authorization': 'Bearer ' + access_token
    }, verify=VERIFY_REQUESTS)
    person_response.raise_for_status()
    return person_response.json()


def _get_access_marker(code):
    response = requests.post(TOKEN_URL, data={
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': SECRET,
        'grant_type': 'authorization_code',

    }, verify=VERIFY_REQUESTS)
    response.raise_for_status()
    return response.json()


def _get_library_id(user_grs_record):
    fields_505 = user_grs_record.get_field('505')
    if not fields_505:
        return ''
    for field in fields_505:
        org_id = field.content
        try:
            return Library.objects.get(school_id=org_id).id
        except Library.DoesNotExist:
            pass
    return ''
