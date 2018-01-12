# coding=utf-8
import json
import re
import logging
import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
import junimarc
from ruslan import client, connection_pool, humanize, holdings, grs
from sso_ruslan.models import get_ruslan_user
from transformers_pool.transformers import transformers
from participants.models import Library, find_holders

RUSLAN = getattr(settings, 'RUSLAN', {})
API_ADDRESS = RUSLAN.get('api_address', 'http://localhost/')
API_USERNAME = RUSLAN.get('username')
API_PASSWORD = RUSLAN.get('password')

ON_HAND_DB = 'circ'
RCIRC = 'RCIRC_RT'
ORDERS_DB = 'extd'
ARCHIVE_ORDERS_DB = 'aextd'
HOLDINGS_BASE = 'spstu'

FINE_PER_DAY = 10.0
MAX_FINE = 500.0

PLACES = {
    u'0': u"на абонементе",
    u'1': u"в читальном зале",
    u'2': u"на руках",
    u'3': u"утерян",
    u'4': u"на руках в читальном зале"
}

PLACES_WITHOUT_FINE = ['0', '1']

# ruslan_client = connection_pool.get_client(API_ADDRESS, API_USERNAME, API_PASSWORD)

logger = logging.getLogger('django.request')


@login_required
def on_hand(request):
    now = datetime.datetime.now().date()
    ruslan_user = get_ruslan_user(request)

    if not ruslan_user:
        return HttpResponse(u'Вы не являетесь читателем')

    ruslan_client = client.HttpClient(API_ADDRESS, API_USERNAME, API_PASSWORD, auto_close=False)

    def make_request(start_record=1, maximum_records=20):
        return ruslan_client.search(
            database=ON_HAND_DB,
            query='@attrset bib-1 @attr 1=100 "%s"' % ruslan_user.username,
            maximum_records=maximum_records,
            start_record=start_record,
            accept='application/json'
        )

    responses = []

    per_request = 20
    errors = []
    orders = []
    fine = 0

    try:
        response = make_request(start_record=1, maximum_records=per_request)
        # print json.dumps(response, ensure_ascii=False)
    except Exception as e:
        errors.append(u'Сервер заказов недоступен. Пожалуйста, попробуйте позже.')
        logger.exception(e)
        pass

    if not errors:
        responses.append(response)

        while True:
            next_position = int(response.get('nextRecordPosition', 0))
            number_of_records = int(response.get('numberOfRecords', 0))

            if next_position and next_position < number_of_records:
                response = make_request(next_position, maximum_records=per_request)
                responses.append(response)
            else:
                break

        ruslan_client.close_session()

        for response in responses:
            for record in humanize.get_records(response):
                opac_record = humanize.get_record_content(record)
                # print json.dumps(opac_record, ensure_ascii=False)
                grs_record = humanize.grs_to_dict(opac_record['tag'])

                bib_record = grs_record.get('202', [{}])[0].get('value', {}).get('record', {})
                item_place = grs_record.get('148', [{}])[0].get('value', '')
                record = junimarc.json_schema.record_from_json(bib_record)
                libcard = junimarc.utils.beautify(
                    unicode(transformers['libcard'](junimarc.ruslan_xml.record_to_xml(record)))
                )
                org = grs_record.get('146', [{}])[0].get('value', '')
                branch = grs_record.get('147', [{}])[0].get('value', '')

                get_date_str = grs_record.get('142', [{}])[0].get('value', '')
                get_date = None

                if get_date_str:
                    get_date = datetime.datetime.strptime(get_date_str, '%Y%m%d').date()

                return_date_str = grs_record.get('143', [{}])[0].get('value', '')
                return_date = None

                if return_date_str:
                    return_date = datetime.datetime.strptime(return_date_str, '%Y%m%d').date()
                item_fine = 0

                if return_date and return_date < now and item_place not in PLACES_WITHOUT_FINE:
                    item_fine = (now - return_date).days * FINE_PER_DAY
                    if item_fine > MAX_FINE:
                        item_fine = MAX_FINE
                    fine += item_fine

                out_of_date = False
                if return_date and return_date < now:
                    out_of_date = True

                orders.append({
                    'libcard': libcard,
                    'org': org,
                    'branch': branch,
                    'item_place': {
                        'id': item_place,
                        'title': PLACES.get(item_place, u''),
                    },
                    'get_date': get_date,
                    'return_date': return_date,
                    'fine': item_fine,
                    'out_of_date': out_of_date,
                })
    ruslan_client.close_session()
    return render(request, 'ruslan_cabinet/frontend/on_hand_items.html', {
        'orders': orders,
        'fine': fine,
        'errors': errors
    })


REMOTE_STATES = {
    '0': u'принят',
    '1': u'отправлен',
    '2': u'получен',
    '3': u'отменен',
}


@login_required
def remote_return(request):
    now = datetime.datetime.now().date()
    ruslan_user = get_ruslan_user(request)

    if not ruslan_user:
        return HttpResponse(u'Вы не являетесь читателем')

    ruslan_client = client.HttpClient(API_ADDRESS, API_USERNAME, API_PASSWORD, auto_close=False)

    def make_request(start_record=1, maximum_records=20):
        return ruslan_client.search(
            database=RCIRC,
            query='@attrset bib-1 @attr 1=100 "%s"' % ruslan_user.username,
            maximum_records=maximum_records,
            start_record=start_record,
            accept='application/json'
        )

    responses = []

    per_request = 20
    errors = []
    orders = []
    fine = 0

    try:
        response = make_request(start_record=1, maximum_records=per_request)
        # print json.dumps(response, ensure_ascii=False)
    except Exception as e:
        errors.append(u'Сервер заказов недоступен. Пожалуйста, попробуйте позже.')
        logger.exception(e)
        pass

    if not errors:
        responses.append(response)

        while True:
            next_position = int(response.get('nextRecordPosition', 0))
            number_of_records = int(response.get('numberOfRecords', 0))

            if next_position and next_position < number_of_records:
                response = make_request(next_position, maximum_records=per_request)
                responses.append(response)
            else:
                break

        ruslan_client.close_session()

        for response in responses:
            for record in humanize.get_records(response):
                opac_record = humanize.get_record_content(record)
                # print json.dumps(opac_record, ensure_ascii=False)
                grs_record = grs.Record.from_dict(opac_record)
                order_id = grs_record.get_field_value('1', '')
                receipt_date = grs_record.get_field_value('142', '')
                bib_card = grs_record.get_field_value('144', '')
                record_id = grs_record.get_field_value('145', '')
                owner_id = grs_record.get_field_value('146', '')
                receipter_id = grs_record.get_field_value('410', '')
                state = REMOTE_STATES.get(grs_record.get_field_value('148', ''), u'неизвестно')
                owner_sigla = grs_record.get_field_value('147', '')
                receipter_sigla = grs_record.get_field_value('411', '')

                owner_org = None
                try:
                    owner_org = Library.objects.get(code=owner_id)
                    if owner_sigla:
                        owner_org = find_holders(owner_org, owner_sigla)
                except Library.DoesNotExist:
                    pass

                receipter_org = None
                try:
                    receipter_org = Library.objects.get(code=receipter_id)
                    if receipter_sigla:
                        receipter_org = find_holders(receipter_org, receipter_sigla)
                except Library.DoesNotExist:
                    pass

                orders.append({
                    'order_id': order_id,
                    'receipt_date': receipt_date,
                    'bib_card': bib_card,
                    'record_id': record_id,
                    'owner_id': owner_id,
                    'receipter_id': receipter_id,
                    'state': state,
                    'owner_org': owner_org,
                    'receipter_org': receipter_org,
                })
    ruslan_client.close_session()
    return render(request, 'ruslan_cabinet/frontend/remote_items.html', {
        'orders': orders,
        'fine': fine,
        'errors': errors
    })


def _get_orders(ruslan_client, ruslan_user, database):
    errors = []

    def make_request(start_record=1, maximum_records=20):
        return ruslan_client.search(
            database=database,
            query='@attrset ext-1 @attr 1=1 "%s"' % ruslan_user.username,
            maximum_records=maximum_records,
            start_record=start_record,
            accept='application/opac+json'
        )

    responses = []

    per_request = 20
    response = make_request(start_record=1, maximum_records=per_request)

    diagnostics = response.get('diagnostics', {}).get('diagnostic', [])

    if diagnostics:
        json_diagnostics = ''
        try:
            json_diagnostics = json.dumps(diagnostics)
        except json.JSONEncoder:
            pass
        logger.error(u'Ошибка при получении списка заказов: %s' % (json_diagnostics,))
        errors.append(u'Ошибка при получении списка заказов.')

    responses.append(response)
    next_position = int(response.get('nextRecordPosition', 1))
    number_of_records = int(response.get('numberOfRecords', 0))

    while next_position and next_position > number_of_records:
        next_position = int(response.get('nextRecordPosition', next_position + per_request))
        response = make_request(next_position, maximum_records=per_request)
        responses.append(response)

    orders = []

    for response in responses:
        for record in humanize.get_records(response):
            opac_record = humanize.get_record_content(record)
            bib_record_dict = opac_record \
                .get('taskSpecificParameters', {}) \
                .get('taskPackage', {}) \
                .get('targetPart', {}) \
                .get('itemRequest', {}) \
                .get('bibliographicRecord', {}) \
                .get('record', {})

            libcard = ''

            if bib_record_dict:
                libcard = junimarc.utils.beautify(unicode(transformers['libcard'](junimarc.ruslan_xml.record_to_xml(
                    junimarc.json_schema.record_from_json(bib_record_dict)))
                ))

            orders.append({
                'libcard': libcard,
                'opac': {
                    'statusOrErrorReport': opac_record
                        .get('taskSpecificParameters', {})
                        .get('taskPackage', {})
                        .get('targetPart', {})
                        .get('statusOrErrorReport', ''),
                    'taskStatus': opac_record.get('taskStatus', ''),
                    'creationDateTime': opac_record.get('creationDateTime', ''),
                    'targetReference': opac_record.get('targetReference', ''),
                },
            })
    orders.reverse()
    return {
        'orders': orders,
        'errors': errors,
    }


@login_required
def current_orders(request):
    ruslan_user = get_ruslan_user(request)
    errors = []

    if not ruslan_user:
        return HttpResponse(u'Вы не являетесь читателем')

    ruslan_client = client.HttpClient(API_ADDRESS, API_USERNAME, API_PASSWORD, auto_close=False)

    orders_response = _get_orders(
        ruslan_client=ruslan_client,
        ruslan_user=ruslan_user,
        database=ORDERS_DB,
    )

    ruslan_client.close_session()
    return render(request, 'ruslan_cabinet/frontend/orders.html', {
        'orders': orders_response['orders'],
        'errors': orders_response['errors']
    })


def holding_info(request):
    id = request.GET.get('id', None)
    database = request.GET.get('database', HOLDINGS_BASE)

    if not id:
        return HttpResponse(u'Не указан идентификатор записи')
    ruslan_client = client.HttpClient(API_ADDRESS, API_USERNAME, API_PASSWORD, auto_close=False)
    response = ruslan_client.get_records(id_list=[id], database=database, opac=True)
    ruslan_client.close_session()
    records = humanize.get_records(response)
    bib_record = None
    holding_groups = None

    if records:
        opac_content = humanize.get_record_content(records[0])
        bib_record = humanize.get_bib_record_from_opac(opac_content)
        holding_data = humanize.get_holdings_data_from_opac(opac_content)

        if holding_data:
            holding_groups = holdings.group_by_locations(holding_data)

    return render(request, 'ruslan_cabinet/frontend/holding_info.html', {
        'bib_record': bib_record,
        'holding_groups': holding_groups
    })


def make_order(request):
    return render(request, 'ruslan_cabinet/frontend/make_order.html')


def _to_relate_items_and_record(on_hand):
    record_ids = {}

    for bib_record in on_hand['bib_records']:
        record_id = _get_record_id(bib_record)
        if record_id:
            record_ids[record_id] = _build_record_title(bib_record)

    items = []
    for on_hand_item in on_hand['items']:
        attrs = on_hand_item.get('attrs', {})
        record_id = attrs.get('145', [u''])[0]
        title = record_ids.get(record_id, '')
        items.append({
            'attrs': attrs,
            'title': title
        })
    return items


def _get_record_id(record_dict):
    control_fields = record_dict.get('cf', [])
    for control_field in control_fields:
        if control_field.get('tag', '') == '001':
            return control_field.get('d', '')
    return ''


def _build_record_title(record_dict):
    title = _get_subfield(record_dict, '200', 'a')
    return title


def _get_subfield(*args):
    data = ''
    for data_field in args[0].get('df', []):
        if data_field.get('tag', '') == args[1]:
            if len(args) == 3:
                for subfield in data_field.get('sf', []):
                    if subfield.get('id', '') == args[2]:
                        data = subfield.get('d', '')
    return data



