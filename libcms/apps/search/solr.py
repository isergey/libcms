# encoding: utf-8
import logging
from django.conf import settings
import requests
import json
import titles

SOLR_SERVER = getattr(settings, 'SEARCH', {}).get('solr', {}).get('host', 'http://localhost:8983/solr/')
COLLECTION = getattr(settings, 'SEARCH', {}).get('solr', {}).get('collection')

logger = logging.getLogger('')

def index_docs(docs=list(), collection=COLLECTION):
    json_docs = json.dumps(docs, ensure_ascii=False).encode('utf-8')
    response = requests.post(SOLR_SERVER + collection + '/update/json', data=json_docs, params={'commit': 'true'})
    response.raise_for_status()


def delete_docs(ids=list(), collection=COLLECTION):
    json_docs = json.dumps({'delete': ids}, ensure_ascii=False).encode('utf-8')
    response = requests.post(SOLR_SERVER + collection + '/update/json', data=json_docs, params={'commit': 'true'})
    response.raise_for_status()


def luke(collection=COLLECTION):
    response = requests.get(SOLR_SERVER + collection + '/admin/luke', params={
        'wt': 'json'
    })

    result = {}
    try:
        response.raise_for_status()
        response_dict = response.json()
    except Exception as e:
        result['error'] = {
            'code': response.status_code,
            'message': e.message
        }
        return  result

    fields = []
    response_fields = response_dict.get('fields', {})
    for field in response_fields.keys():
        if field in ['_version_', 'id']:
            continue
        fields.append({
            'name': field,
            'type': response_fields.get(field, {}).get('type')
        })

    result['fields'] = fields
    return result

def search(query,
           fields=list(['id']), offset=0, limit=10, sort=list(), facets=list(),
           highlighting=list(),
           facet_offset=0, facet_limit=15, facet_sort='count', facet_range=None, collection=COLLECTION):
    params={
        'wt': 'json',
        'q': query,
        'start': offset,
        'rows': limit,
        'fl': fields
    }

    if facets:
        params['facet'] = 'true'
        params['facet.field'] = facets
        params['facet.mincount'] = '1'

    if facet_sort:
        params['facet.sort'] = facet_sort

    if facet_offset:
        params['facet.offset'] = facet_offset

    if facet_limit:
        params['facet.limit'] = facet_limit

    if facet_range:
        params['facet'] = 'true'
        params['facet.mincount'] = '1'
        params['facet.range'] = facet_range['field']
        params['facet.range.start'] = facet_range['start']
        params['facet.range.end'] = facet_range['end']
        params['facet.range.gap'] = facet_range['gap']

    if sort:
        params['sort'] = u','.join(sort)

    if highlighting:
        params['hl'] = 'true'
        params['hl.fl'] = u','.join(highlighting)
    response = requests.get(SOLR_SERVER + collection + '/select', params=params)

    error = {}
    try:
        response_dict = json.loads(response.text)
        if 'error' in response_dict:
            error['code'] = response_dict.get('error', {}).get('code', u'')
            error['message'] = response_dict.get('error', {}).get('msg', u'')
        else:
            response.raise_for_status()
    except Exception as e:
        error['code'] = response.status_code
        error['message'] = u'Error of search request'
        logger.error(u'Error while search in solr: %s' % e.message)
        response_dict = {}


    result = {}
    if error:
        result['error'] = error
    result['docs'] = response_dict.get('response', {}).get('docs', [])
    result['total'] = int(response_dict.get('response', {}).get('numFound', '0'))
    result['offset'] = int(response_dict.get('response', {}).get('start', '0'))
    result['facets'] = {}


    response_facets = response_dict.get('facet_counts', {}).get('facet_fields', {})

    for facet_key in response_facets.keys():
        result['facets'][facet_key] = []
        facet = result['facets'][facet_key]
        facet_values = response_facets[facet_key]

        if len(facet_values) % 2 != 0:
            raise Exception("Wrong length of facet values list")

        i = 0
        while i < len(facet_values):
            facet.append({
                'value': facet_values[i],
                'count': facet_values[i+1]
            })
            i += 2

    result['facet_ranges'] = {}
    response_facets = response_dict.get('facet_counts', {}).get('facet_ranges', {})
    for facet_key in response_facets.keys():
        result['facet_ranges'][facet_key] = []
        facet = result['facet_ranges'][facet_key]
        facet_values = response_facets[facet_key]['counts']
        if len(facet_values) % 2 != 0:
            raise Exception("Wrong length of facet values list")

        i = 0
        while i < len(facet_values):
            facet.append({
                'value': facet_values[i],
                'count': facet_values[i+1]
            })
            i += 2

    highlighting = response_dict.get('highlighting', {})
    if highlighting:
        result['highlighting'] = highlighting
    return Results(result)


class Results(object):
    def __init__(self, solr_dict=dict()):
        self.__solr_dict = solr_dict

    def count(self):
        return self.__solr_dict.get('total', 9999)

    def get(self, *args):
        return self.__solr_dict.get(*args)

    def __getitem__(self, item):
        s_item = unicode(item)
        attr = getattr(self, s_item, None)
        if attr != None:
            return attr
        return self.__solr_dict.get(s_item)

class SearchCriteria:

    def __init__(self, operator):
        """
        Init
        :param operator: String AND|OR
        :return:
        """
        self.operator = operator
        self.query = []

    def add_attr(self, key, value, priority=0):
        """
        :param criteria_part: CriteriaPart object
        :return:
        """
        k = key
        if priority:
            k = key + '^' + str(priority)
        self.query.append({
            'k': key,
            'v': u'%s' % value
        })

    def add_search_criteria(self, search_criteria):
        """
        :param search_criteria: SearchCriteria object
        :return:
        """
        self.query.append(search_criteria)

    def to_lucene_query(self):
        query_string_parts = [u"("]

        for i, query_part in enumerate(self.query):
            if isinstance(query_part, dict):
                query_string_parts.append(u'%s:%s' % (query_part['k'], query_part['v']))
            elif isinstance(query_part, SearchCriteria):
                query_string_parts.append(query_part.to_lucene_query())
            if i < len(self.query) - 1:
                query_string_parts.append(u' ' + self.operator + u' ')
        query_string_parts.append(u')')
        return u''.join(query_string_parts)

    def to_dict(self):
        dict_criteria = {
            'op': self.operator,
            'query': []
        }
        for i, query_part in enumerate(self.query):
            if isinstance(query_part, dict):
                dict_criteria['query'].append(query_part)
            elif isinstance(query_part, SearchCriteria):
                dict_criteria['query'].append(query_part.to_dict())

        return dict_criteria

    @staticmethod
    def from_dict(dict_criteria):
        try:
            sc = SearchCriteria(dict_criteria['op'])
            for query_part in dict_criteria['query']:
                if 'k' in query_part and 'v' in query_part:
                    sc.add_attr(query_part['k'], query_part['v'])
                else:
                    sc.add_search_criteria(SearchCriteria.from_dict(query_part))
            return sc
        except KeyError as e:
            raise ValueError(u'Wrong dict_criteria %s. Error:' % (unicode(dict_criteria), unicode(e)))

    def to_human_read(self, parent=None, lang=u'ru'):
        operators_title = {
            u'AND': {
                u'ru': u'И'
            },
            u'OR': {
                u'ru': u'ИЛИ'
            },
            u'NOT': {
                u'ru': u'НЕ'
            },
        }
        query_string_parts = []
        if parent:
            query_string_parts.append(u'(')

        for i, query_part in enumerate(self.query):
            if isinstance(query_part, dict):
                query_string_parts.append(u'%s:"%s"' % ( titles.get_attr_title(query_part['k']), query_part['v']))
            elif isinstance(query_part, SearchCriteria):
                query_string_parts.append(query_part.to_human_read(parent=True, lang=lang))
            if i < len(self.query) - 1:

                try:
                    operator_title = operators_title[self.operator][lang]
                except KeyError:
                    operator_title = self.operator

                query_string_parts.append(u' ' + operator_title + u' ')
        if parent:
            query_string_parts.append(u')')
        return u''.join(query_string_parts)


def escape(string):
    special = [
        u'\\',
        u'+',
        u'-',
        u'&&',
        u'||',
        u'!',
        u'(',
        u')',
        u'{',
        u'}',
        u'[',
        u']',
        u'^',
        u'"',
        u'~',
        u'?',
        u':'
    ]
    for s in special:
        string = string.replace(s,'\\'+s)
    return string