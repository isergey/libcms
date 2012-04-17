# -*- coding: utf-8 -*-
import re

operator_title = {
    'AND': u'И',
    'NOT': u'И НЕ',
    'ANDNOT': u'ИЛИ',
}

attr_title = {
    '1':{
        'name': u'Точка доступа',
        '4': u'Заглавие',
        '1003': u'Автор',
        '21': u'Тематика'
    },
    '2':{
        'name': u'Отношение',
        '1': u'мньше',
        '2': u'меньше или равно',
        '3': u'равно',
        '4': u'больше или равно',
        '5': u'больше',
        '6': u'не равно',
        '100': u'фонетическое совпадение',
        '101': u'Stem',
        '102': u'релевантно',
        '103': u'AlwaysMatches',
    },
    '3':{
        'name': u'Позиция',
        '1': u'првое в поле',
        '2': u'первое в подполе',
        '3': u'любая',
    },
    '4':{
        'name': u'Структура',
        '1': u'фраза',
        '2': u'слово',
        '3': u'ключ',
        '4': u'год',
        '5': u'дата (нормализованная)',
        '6': u'список слов',
        '100': u'Date (un-normalized)',
        '101': u'Name (normalized)',
        '102': u'Name (un-normalized)',
        '103': u'структура',
        '104': u'Urx',
        '105': u'текст в свободной форме',
        '106': u'Document-text',
        '107': u'Local-number',
        '108': u'String',
        '109': u'Numeric string',
    },
    '5':{
        'name': u'Усечение',
        '1': u'справа',
        '2': u'слева',
        '3': u'справа и слева',
        '100': u'не обрезать',
        '101': u'Process # in search term',
        '102': u'RegExpr-1',
        '103': u'RegExpr-2',
    },
    '6':{
        'name': u'Completeness',
        '1': u'Incomplete subfield',
        '2': u'Complete subfield',
        '3': u'Complete field',
    }
}
attr_systems = {
    '1.2.840.10003.3.1': 'Bib-1'
}

class HumanQuery(object):
    def __init__(self, arm_query):
        if isinstance(arm_query, unicode) == False:
            raise TypeError('arm_query must be unicode')
        self.arm_query = arm_query

    def convert(self):
        opps_regx = re.compile(ur"(\w+)\(", re.UNICODE)
        aributes_regx = re.compile(r"(\d+),(\d+):([\d.]+)", re.UNICODE)
        #terms_regx = re.compile(ur"[\(,]?([\w\s\[\]s,~!@#$%\^&\*=-_/\\{}`\?]+)(\[[\d,:.]+\])", re.UNICODE)
        terms_regx = re.compile(ur"[\(,]?([^\[()]+)(\[[\d,:.]+\])", re.UNICODE)
        operators = re.findall(opps_regx, self.arm_query)
        terms = re.findall(terms_regx, self.arm_query)
        terms_list = [] # список поисковых термов
        terms_aributes = [] # список атрибутов, соответвующих термам
        if len(terms) != (len(operators)+1):
            raise ValueError('in arm_query number of terms and their operators do not match')
        if len(terms):
            for (term, attr_string) in terms:
                terms_list.append(term)
                aributes = re.findall(aributes_regx, attr_string)
                terms_aributes.append(aributes)
        else:
            raise ValueError('arm_query no have search term')

        if len(terms_aributes) == len(terms):
            terms_aributes.append(aributes)
        else:
            raise ValueError('in arm_query number of terms and their attributes do not match')        

        request_map = []
        index = 0
        op_index = len(operators)
        for term in terms_list:
            op_index -=1
            if terms_aributes[index]:
                (attribute, point, system) = terms_aributes[index][0]
            else:
                continue
            params = {'main':'', 'additional':''}
            if attribute in attr_title and point in attr_title[attribute]:
                params['main'] = u"%s: %s " % (attr_title[attribute][point], term)
            else:
                params['main'] = u"%s: %s " % (attribute+'='+point, term)
            additional = []
            for (attribute, point, system) in terms_aributes[index][1:]:
                if attribute in attr_title and point in attr_title[attribute]:
                    additional.append(u"%s — %s" % (attr_title[attribute]['name'], attr_title[attribute][point]))
                else:
                    additional.append(u"%s=%s" % ('Unknown atribute '+attribute, point))
            params['additional'] = '; '.join(additional)
            request_map.append(params)
            if op_index > -1:
                    request_map.append(operators[op_index])
            #print attribute, point, system
            index += 1
        buil_strings = []
        for item in request_map:
            if isinstance(item, dict):
                buil_strings.append(item['main'])#, u'Доп. условия: ', item['additional']
            else:
                buil_strings.append(operator_title[item])

        #print join(buil_strings)
        return '\n'.join(buil_strings)
