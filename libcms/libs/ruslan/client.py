import requests
import json


def dec(obj):
    if isinstance(obj, dict):
        for key in obj.keys():
            obj[key] = dec(obj[key])
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            obj[i] = dec(value)
    elif isinstance(obj, str):
        obj = obj.decode('utf-8')
    return obj

class DictUnicoder(object):
    @staticmethod
    def decode_value(value):
        if isinstance(value, str):
            return value.decode('utf-8')
        elif isinstance(value, dict):
            return DictUnicoder.decode_dict(value)
        elif isinstance(value, list):
            return DictUnicoder.decode_list(value)
        return value

    @staticmethod
    def decode_dict(dict_obj):
        for key, value in dict_obj.items():
            dict_obj[key] = DictUnicoder.decode_value(value)
        return dict_obj

    @staticmethod
    def decode_list(values):
        for i, value in enumerate(values):
            values[i] = DictUnicoder.decode_value(value)
        return value

    @staticmethod
    def decode(obj):
        return DictUnicoder.decode_value(obj)


class HttpClient(object):
    def __init__(
            self,
            base_url,
            username='',
            password='',
            auth_path='/auth',
            db_path='/db',
            finish_path='/finish',
            principal_path='/principal',
            ncip_path='/ncip',
            auto_close=True,
            timeout=60,
            verify_requests=False
    ):
        self._base_url = base_url.strip('/') + '/'
        self._auth_path = auth_path.strip('/')
        self._db_path = db_path.strip('/') + '/'
        self._finish_path = finish_path.strip('/') + '/'
        self._principal_path = principal_path.strip('/') + '/'
        self._ncip_path = ncip_path.strip('/') + '/'
        self._username = username
        self._password = password
        self._timeout = timeout
        self._auto_close = auto_close
        self._session = None
        self._verify_requests = verify_requests

    def search(self, database, query, start_record='', maximum_records='', query_type='pqf', accept='application/json'):
        params = {
            'query': query,
            'queryType': query_type,
        }

        if start_record:
            params['startRecord'] = start_record

        if maximum_records:
            params['maximumRecords'] = maximum_records

        response = self._make_request(
            method='get',
            url=self._base_url + self._db_path + database,
            params=params,
            headers={
                'Accept': accept
            }
        )

        response.raise_for_status()
        return response.json()

    def get_user(self, username, database='allusers'):
        return self.search(database, query='@attrset bib-1 @attr 1=100 "%s"' % '\\\\'.join(username.split('\\')))

    def principal(self):
        response = self._make_request(
            method='get',
            url=self._base_url + self._principal_path,
            headers={
                'Accept': 'application/json'
            }
        )
        response.raise_for_status()
        return response.json()

    def get_records(self, id_list, database, opac=False):
        accept = 'application/json'
        if opac:
            accept = 'application/opac+json'

        ids = [id.replace('\\', '\\\\') for id in set(id_list)]
        attrs = []

        for id in ids:
            attrs.append(u'@attr 1=12 "%s"' % id)

        query_condition = u' '.join(["@or" for x in xrange(len(attrs) - 1)]) + u' ' + u' '.join(attrs)

        return self.search(
            database=database,
            query='@attrset bib-1 %s' % query_condition,
            accept=accept
        )

    def create_grs(self, grs_record, database):
        record_json = json.dumps(dec(grs_record.to_dict()), ensure_ascii=False, encoding='utf-8').encode('utf-8')
        response = self._make_request(
            'put',
            self._base_url + self._db_path + database + '/0',
            data=record_json,
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            })
        response.raise_for_status()
        return response.json()

    def update_grs(self, grs_record, database, id):
        record_json = json.dumps(dec(grs_record.to_dict()), ensure_ascii=False, encoding='utf-8').encode('utf-8')
        response = self._make_request(
            'put',
            self._base_url + self._db_path + database + '/' + id,
            data=record_json,
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            })
        response.raise_for_status()
        return response

    def send_ncip_message(self, message_dict):
        response = self._make_request(
            'post',
            self._base_url + self._ncip_path,
            data=json.dumps(message_dict, ensure_ascii=False).encode('utf-8'),
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            })
        response.raise_for_status()
        return response

    def _make_request(self, method, url, params=None, data=None, headers=None, retrying=0):
        session = self._get_session()
        method_func = getattr(session, method)
        response = method_func(url, params=params, data=data, headers=headers, timeout=self._timeout)
        if response.status_code in [401, 403] and retrying == 0:
            self.close_session()
            response = self._make_request(method, url, params, data, headers, retrying=1)

        if self._auto_close:
            self.close_session()

        return response

    def _get_session(self):
        if not self._session:
            if self._username:
                self._session = self._auth()
            else:
                self._session = requests.Session()

        return self._session

    def close_session(self):
        if not self._session:
            return

        response = self._session.get(self._base_url + self._finish_path)
        response.raise_for_status()
        self._session = None

    def _auth(self):
        session = requests.Session()
        session.auth = (self._username, self._password)
        response = session.get(self._base_url + self._auth_path, timeout=self._timeout, verify=self._verify_requests)
        response.raise_for_status()
        return session
