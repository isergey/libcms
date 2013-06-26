# -*- encoding: utf-8 -*-
import socket
from django.conf import settings
import sunburnt
import datetime
from django.template import Library
from django.utils.translation import get_language

register = Library()

@register.filter
def date_from_isostring(isostring):
    try:
        return datetime.datetime.strptime(isostring, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return None


facet_titles = {
    'fond': {
        'ru':u'Коллекция',
        'en':u'Collection',
        'tt':u'Коллекция'
    },
    'title': {
        'ru':u'Заглавие',
        'en':u'Title',
        'tt':u'Исем'
    },
    'author': {
        'ru':u'Автор',
        'en':u'Author',
        'tt':u'Автор'
    },
    'content-type':{
        'ru':u'Тип содержания',
        'en':u'Content type',
        'tt':u'Эчтәлек тибы'
    },
    'date-of-publication': {
        'ru':u'Год публикации',
        'en':u'Publication year',
        'tt':u'Бастырып чыгару елы'
    },
    'subject-heading': {
        'ru':u'Тематика',
        'en':u'Subject',
        'tt':u'Темасы'
    },
    'anywhere': {
        'ru':u'Везде',
        'en':u'Subject',
        'tt':u'Hәр урында'
    },
    'code-language': {
        'ru':u'Язык',
        'en':u'Language',
        'tt':u'Тел'
    },
    'text': {
        'ru':u'Везде',
        'en':u'Anywhere',
        'tt':u'Везде'
    },
    'full-text': {
        'ru':u'Полный текст',
        'en':u'Full text',
        'tt':u'Hәр урында'
        },
}

@register.filter
def facet_title(arg_code):
    code = u''.join(arg_code.split('_')[:1])
    lang=get_language()[:2]
    title = facet_titles.get(code, code)
    return title


content_type_titles = {
    'a': u'библиографическое издание',
    'b': u'каталог',
    'c': u'указатель',
    'd': u'реферат',
    'e': u'словарь',
    'f': u'энциклопедия',
    'g': u'справочное издание',
    'h': u'описание проекта',
    'j': u'учебник',
    'k': u'патент',
    'l': u'стандарт',
    'm': u'диссертация',
    'n': u'законы',
    'o': u'словарь',
    'p': u'технический отчет',
    'q': u'экзаменационный лист',
    'r': u'литературный обзор/рецензия',
    's': u'договоры',
    't': u'карикатуры или комиксы',
    'w': u'религиозные тексты',
    'z': u'другое',
}

@register.filter
def content_type_title(code):
    return content_type_titles.get(code.lower(), code)
#

language_titles = {
    'rus':u"Русский",
    'eng':u"Английский",
    'tat':u"Татарский",
    'tar':u"Татарский",
    'aze':u"Азербайджанский",
    'amh':u"Амхарский",
    'ara':u"Арабский",
    'afr':u"Африкаанс",
    'baq':u"Баскский",
    'bak':u"Башкирский",
    'bel':u"Белорусский",
    'bal':u"Белуджский",
    'bul':u"Болгарский",
    'bua':u"Бурятский",
    'hun':u"Венгерский",
    'vie':u"Вьетнамский",
    'dut':u"Голландский",
    'gre':u"Греческий",
    'geo':u"Грузинский",
    'dan':u"Датский",
    'dra':u"Дравидийские",
    'grc':u"Древнегреческий",
    'egy':u"Египетский",
    'heb':u"Иврит",
    'ind':u"Индонезийский",
    'ira':u"Иранские",
    'ice':u"Исландский",
    'spa':u"Испанский",
    'ita':u"Итальянский",
    'kaz':u"Казахский",
    'cat':u"Каталанский",
    'kir':u"Киргизский",
    'chi':u"Китайский",
    'kor':u"Корейский",
    'cpe':u"Креольские",
    'cam':u"Кхмерский",
    'khm':u"Кхмерский",
    'lav':u"Латышский",
    'lit':u"Литовский",
    'mac':u"Македонский",
    'chm':u"Марийский",
    'mon':u"Монгольский",
    'ger':u"Немецкий",
    'nor':u"Норвежский",
    'pol':u"Польский",
    'por':u"Португальский",
    'rum':u"Румынский",
    'sla':u"Славянский",
    'slo':u"Словацкий",
    'tib':u"Тибетский",
    'tur':u"Турецкий",
    'tus':u'Tускарора',
    'uzb':u"Узбекский",
    'ukr':u"Украинский",
    'fin':u"Финский",
    'fiu':u"Финно-угорские",
    'fre':u"Французский",
    'hin':u"Хинди",
    'che':u"Чеченский",
    'cze':u"Чешский",
    'chv':u"Чувашский",
    'swe':u"Шведский",
    'est':u"Эстонский",
    'epo':u"Эсперанто",
    'esp':u"Эсперанто",
    'eth':u"Эфиопский",
    'gez':u"Эфиопский",
    'jpn':u"Японский",
    'jap':u"Японский",

}

@register.filter
def language_title(code):
    return language_titles.get(code, code)



@register.inclusion_tag('ssearch/tags/count.html')
def ssearch_all_count():
    try:
        solr = sunburnt.SolrInterface(settings.SOLR['host'])
        responce = solr.query(**{'*':'*'}).field_limit("id").execute()
    except socket.error:
        return {
            'count': 0
        }
    return {
        'count': responce.result.numFound
    }
