# -*- coding: utf-8 -*-
import cStringIO as StringIO
import json

from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.shortcuts import HttpResponse, resolve_url

import unicodecsv
from api.decorators import api, login_required_ajax
from api.exceptions import WrongArguments, ApiException
from .. import models


class ApiUser(object):
    def __init__(self, id=None, username=None, first_name=None, last_name=None, email=None, phone=None,
                 date_joined=None):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.date_joined = date_joined

    def to_dict(self):
        dict = {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
        }
        if self.date_joined:
            dict['date_joined'] = self.date_joined.isoformat()

        return dict

    @classmethod
    def from_model(cls, model):
        api_user = cls(
            id=model.id,
            username=model.username,
            first_name=model.first_name,
            last_name=model.last_name,
            email=model.email,
            date_joined=model.date_joined
        )
        return api_user


class ApiLibrary(object):
    def __init__(
            self,
            id=None,
            parent_id=None,
            name=None,
            code=None,
            # country=None,
            #            city=None,
            district=None,
            phone=None,
            plans=None,
            postal_address=None,
            http_service=None,
            ill_service=None,
            edd_service=None,
            mail=None,
            mail_access=None,
            latitude=None,
            longitude=None):

        self.id = id
        self.parent_id = parent_id
        self.name = name
        self.code = code

        # self.country = country
        #        self.city = city
        self.district = district

        self.phone = phone
        self.plans = plans
        self.postal_address = postal_address

        self.http_service = http_service
        self.ill_service = ill_service
        self.edd_service = edd_service
        self.mail = mail
        self.mail_access = mail_access

        self.latitude = latitude
        self.longitude = longitude

    def to_dict(self):
        dict = {
            'id': self.id,
            'parent_id': self.parent_id,
            'name': self.name,
            'code': self.code,
            # 'country': self.country,
            #            'city': self.city,
            'district': self.district,
            'phone': self.phone,
            'plans': self.plans,
            'postal_address': self.postal_address,
            'http_service': self.http_service,
            'ill_service': self.ill_service,
            'edd_service': self.edd_service,
            'mail': self.mail,
            'mail_access': self.mail_access,
            'latitude': self.latitude,
            'longitude': self.longitude,
        }
        return dict

    @classmethod
    def from_model(cls, model):
        api_library = cls(
            id=model.id,
            parent_id=model.parent_id,
            name=model.name,
            code=model.code,
            phone=model.phone,
            plans=model.plans,
            postal_address=model.postal_address,
            http_service=model.http_service,
            ill_service=model.ill_service,
            edd_service=model.edd_service,
            mail=model.mail,
            mail_access=model.mail_access,
            latitude=model.latitude,
            longitude=model.longitude,
        )
        if model.parent_id:
            api_library.parent_id = model.parent_id
        #
        # if model.country_id:
        #            api_library.country=model.country.name
        #
        #        if model.city_id:
        #            api_library.city=model.city.name

        if model.district_id:
            api_library.district = model.district.name

        return api_library


def index(request):
    return HttpResponse(u'Api ok')


@api
# @login_required_or_403
def auth_user(request):
    username = request.GET.get('username', None)
    password = request.GET.get('password', None)
    if not username or not password:
        raise WrongArguments()

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return {}

    if not user.check_password(password):
        return {}

    return ApiUser.from_model(user).to_dict()


@api
# @login_required_or_403
def get_user_orgs(request):
    id = request.GET.get('id', None)
    lazy = request.GET.get('lazy', False)

    if not id:
        raise WrongArguments()

    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        raise ApiException(u'unknown user id')

    user_libraries = models.UserLibrary.objects.filter(user=user)

    libraries_ids = []

    for user_library in user_libraries:
        libraries_ids.append(user_library.library_id)

    # содержатся только уникальные идентификаторы
    libraries_ids = list(set(libraries_ids))

    libraries_list = []

    if not lazy:
        libraries = models.Library.objects.select_related().filter(id__in=libraries_ids)

        for library in libraries:
            api_library = ApiLibrary.from_model(library)

            libraries_list.append(api_library.to_dict())
    else:
        libraries_list = libraries_ids

    return libraries_list


@api
# @login_required_or_403
def get_org(request):
    id = request.GET.get('id', None)
    code = request.GET.get('code', None)

    if not id and not code:
        raise WrongArguments()

    if id:
        try:
            id = int(id)
        except ValueError:
            raise ApiException(u'Wrong id value')

    try:
        if id:
            library = models.Library.objects.get(id=id)
        elif code:
            library = models.Library.objects.get(code=code)
    except models.Library.DoesNotExist:
        return {}

    return ApiLibrary.from_model(library).to_dict()


@api
def find_orgs(request):
    name = request.GET.get('name', None)
    ill_service = request.GET.get('ill_service', None)
    edd_service = request.GET.get('edd_service', None)
    mail = request.GET.get('mail', None)

    if name:
        libraries = models.Library.objects.filter(name__iexact=name)
    elif ill_service:
        if ill_service == '*':
            libraries = models.Library.objects.filter(ill_service__gt=0)
        else:
            libraries = models.Library.objects.filter(ill_service__icontains=ill_service)
    elif edd_service:
        libraries = models.Library.objects.filter(edd_service__icontains=edd_service)
    elif mail:
        libraries = models.Library.objects.filter(mail__icontains=mail)
    else:
        raise WrongArguments()

    libraries_list = []
    for library in libraries:
        libraries_list.append(ApiLibrary.from_model(library).to_dict())

    return libraries_list


@api
# @login_required_or_403
def get_user(request):
    id = request.GET.get('id', None)

    username = request.GET.get('username', None)

    if not id and not username:
        raise WrongArguments()

    if id:
        try:
            id = int(id)
        except ValueError:
            raise ApiException(u'Wrong id value')

    try:
        if id:
            user = User.objects.get(id=int(id))
        elif username:
            user = User.objects.get(username=username)
    except User.DoesNotExist:
        return {}

    return ApiUser.from_model(user).to_dict()


from collections import OrderedDict
from django.core.serializers import xml_serializer
from django.core.serializers import json as json_serializer


def _get_org_site(org, host=''):
    return host + resolve_url('participant_site:frontend:index', library_code=org.code)


class XmlSerializer(xml_serializer.Serializer):
    def __init__(self, host='', *args, **kwargs):
        self.__host = host
        super(XmlSerializer, self).__init__(*args, **kwargs)

    def end_object(self, obj):
        """
        Called after handling all fields for an object.
        """
        self.indent(2)
        self.xml.startElement("field", OrderedDict([
            ("name", 'site'),
            ("type", 'CharField'),
        ]))
        self.xml.characters(_get_org_site(obj, host=self.__host))
        self.xml.endElement("field")
        self.indent(1)
        self.xml.endElement("object")


class JsonSerializer(json_serializer.Serializer):
    def __init__(self, host='', *args, **kwargs):
        self.__host = host
        super(JsonSerializer, self).__init__(*args, **kwargs)

    def end_object(self, obj):
        # self._current has the field data
        indent = self.options.get("indent")
        if not self.first:
            self.stream.write(",")
            if not indent:
                self.stream.write(" ")
        if indent:
            self.stream.write("\n")
        dumped_obj = self.get_dump_object(obj)
        dumped_obj.get('fields', {})['site'] = _get_org_site(obj, host=self.__host)
        json.dump(
            dumped_obj, self.stream,
            cls=json_serializer.DjangoJSONEncoder, **self.json_kwargs)
        self._current = None


@api
def export_orgs(request):
    host = request.META.get('HTTP_HOST', '')

    if request.is_secure():
        host = 'https://' + host
    else:
        host = 'http://' + host

    scheme = request.GET.get('scheme', 'xml')
    schemes = ['xml', 'json', 'csv']

    if scheme not in schemes:
        scheme = 'xml'

    orgs = list(models.Library.objects.all())
    data = u''

    if scheme == 'csv' and orgs:
        iodata = StringIO.StringIO()
        fieldnames = model_to_dict(orgs[0]).keys() + ['site']
        writer = unicodecsv.DictWriter(iodata, fieldnames=fieldnames)
        writer.writeheader()
        for org in orgs:
            org_dict = model_to_dict(org)
            org_dict['site'] = _get_org_site(org, host=host)
            writer.writerow(org_dict)
        data = iodata.getvalue()
    elif scheme == 'json':
        ser = JsonSerializer(host=host)
        data = ser.serialize(orgs)
    else:
        ser = XmlSerializer(host=host)
        data = ser.serialize(orgs)

    return HttpResponse(data, content_type='application/' + scheme)

@api
def export_ora_conns(request):
    scheme = request.GET.get('scheme', 'xml')
    schemes = ['xml', 'json']

    if scheme not in schemes:
        scheme = 'xml'

    connections = models.OracleConnection.objects.all()

    ser = xml_serializer.Serializer()
    if scheme == 'json':
        ser = json_serializer.Serializer()

    data = ser.serialize(connections)
    return HttpResponse(data, content_type='application/' + scheme)

@api
def export_int_conns(request):
    scheme = request.GET.get('scheme', 'xml')
    schemes = ['xml', 'json']

    if scheme not in schemes:
        scheme = 'xml'

    connections = models.InternetConnection.objects.all()

    ser = xml_serializer.Serializer()
    if scheme == 'json':
        ser = json_serializer.Serializer()

    data = ser.serialize(connections)
    return HttpResponse(data, content_type='application/' + scheme)




@login_required_ajax
def user_organizations(request):
    orgs = models.user_organizations(request.user)
    return HttpResponse(json.dumps(orgs, ensure_ascii=False), content_type='application/json')


@login_required_ajax
def personal_cabinet_links(request):
    return HttpResponse(json.dumps(models.personal_cabinet_links(request), ensure_ascii=False),
                        content_type='application/json')



