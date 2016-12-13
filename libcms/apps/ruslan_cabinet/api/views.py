# coding=utf-8
from django.core.urlresolvers import reverse
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from api import decorators as api_decorators, responses as api_responses, errors as api_errors
from ruslan import connection_pool
from sso_ruslan.models import get_ruslan_user
from . import forms

RUSLAN = getattr(settings, 'RUSLAN', {})
API_ADDRESS = RUSLAN.get('api_address', 'http://localhost/')
API_USERNAME = RUSLAN.get('username')
API_PASSWORD = RUSLAN.get('password')

ON_HAND_DB = 'circ'
ORDERS_DB = 'extd'
HOLDINGS_BASE = 'spstu'

ORG_CODES = RUSLAN.get('org_codes', {})

CAN_ORDER_BRANCHES = RUSLAN.get('can_order_branches', [])

ruslan_client = connection_pool.get_client(API_ADDRESS, API_USERNAME, API_PASSWORD)


@api_decorators.permission_required(['pages.create_page'], message=u'Доступ запрещен')
def index(request):
    return api_responses.response({
        'status': 'ok'
    })

@never_cache
@csrf_exempt
def holdings(request):
    record_id = request.GET.get('recordId', '')
    if not record_id:
        return api_responses.errors_response('recordId params does not exist')

    try:
        response = ruslan_client.get_records(id_list=[record_id], database=HOLDINGS_BASE, opac=True)
    except Exception as e:
        return api_responses.errors_response(e.message)

    return api_responses.response(response)


@login_required
@require_http_methods(['POST'])
@never_cache
@csrf_exempt
def make_reservation(request):
    ruslan_user = get_ruslan_user(request)
    if not ruslan_user:
        return api_responses.errors_response(u'Вы не являетесь читателем')

    if request.method == 'POST':
        make_reservation_form = forms.MakeReservationForm(request.POST)
        if make_reservation_form.is_valid():
            ncip_message = {
                "RequestItem": {
                    "UserId": {
                        "AgencyId": {
                            "value": ORG_CODES[make_reservation_form.cleaned_data['org']]
                        },
                        "UserIdentifierValue": ruslan_user.username
                    },
                    "BibliographicId": {
                        "BibliographicRecordId": {
                            "BibliographicRecordIdentifier": make_reservation_form.cleaned_data['record_id'],
                            "AgencyId": {
                                "value": ORG_CODES[make_reservation_form.cleaned_data['org']]
                            }
                        }
                    },
                    "RequestType": {
                        "value": u"Hold",
                        "Scheme": u"http://www.niso.org/ncip/v1_0/imp1/schemes/requesttype/requesttype.scm"
                    },
                    "RequestScopeType": {
                        "value": u"Bibliographic Item",
                        "Scheme": u"http://www.niso.org/ncip/v1_0/imp1/schemes/requestscopetype/requestscopetype.scm"
                    },
                    "PickupLocation": {
                        "value": u'%s/%s' % (make_reservation_form.cleaned_data['org'], make_reservation_form.cleaned_data['branch'])
                    }
                }
            }

            response = ruslan_client.send_ncip_message(ncip_message)
            response_dict = response.json()
            problem = response_dict.get('RequestItemResponse', {}).get('Problem', {})
            if problem:
                message = u'Ошибка при бронировании'
                problem_detail = response_dict.get('RequestItemResponse', {}).get('Problem', {}).get('ProblemDetail', '');
                if problem_detail.startswith('220'):
                    message = u'Превышен лимит заказов. Посмотреть текущие заказы можно в разделе "Мои заказы"'
                    return api_responses.error_response(api_errors.Error(code='220', message=message))
                return api_responses.error_response(api_errors.Error(code='0', message=message))
            return api_responses.response({
                'status': 'ok',
            })
        else:
            return api_responses.error_response(api_errors.FormError.from_form(name='make_reservation_form', django_form=make_reservation_form))


@never_cache
@csrf_exempt
def get_config(request):
    is_reader = False
    if get_ruslan_user(request):
        is_reader = True

    response = {
        'can_order_branches': CAN_ORDER_BRANCHES,
        'is_reader': is_reader,
        'urls': {
            'holdings': reverse('ruslan_cabinet:api:holdings'),
            'make_reservation': reverse('ruslan_cabinet:api:make_reservation')
        }
    }
    return api_responses.response(response)
