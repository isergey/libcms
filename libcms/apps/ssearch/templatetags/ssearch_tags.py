# -*- encoding: utf-8 -*-
from lxml import etree
import socket
from django.conf import settings
import sunburnt
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import Library
from django.utils.translation import get_language
from django.core.cache import cache
from ..models import Collection, Record

from ..frontend.views import get_collections, replace_doc_attrs, xml_doc_to_dict
from common.xslt_transformers import xslt_transformer, xslt_marc_dump_transformer, xslt_bib_draw_transformer

register = Library()


@register.inclusion_tag('ssearch/tags/participant_income.html')
def participant_income(sigla):

    solr = sunburnt.SolrInterface(settings.SOLR['local_records_host'])
    if sigla:
        query = solr.Q(**{'holder-sigla_s': sigla})
    else:
        query = solr.Q(**{'*': '*'})

    solr_searcher = solr.query(query)
    solr_searcher = solr_searcher.field_limit(['id', 'record-create-date_dts'])

    solr_searcher = solr_searcher.sort_by('-record-create-date_dts')

    paginator = Paginator(solr_searcher, 10)  # Show 25 contacts per page


        # If page is not an integer, deliver first page.
    results_page = paginator.page(1)


    docs = []

    for row in results_page.object_list:
        print row
        docs.append(replace_doc_attrs(row))

    doc_ids = []
    for doc in docs:
        doc_ids.append(doc['id'])

    records_dict = {}
    records = list(Record.objects.using('local_records').filter(gen_id__in=doc_ids))
    for record in records:
        records_dict[record.gen_id] = etree.tostring(
            xslt_bib_draw_transformer(etree.XML(record.content), abstract='false()'), encoding='utf-8')

    for doc in docs:
        doc['record'] = records_dict.get(doc['id'])

    return {
        #'results_page': results_page,
        'docs': docs,
        'sigla': sigla
    }




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
    'record-create-date': {
        'ru':u'Дата поступления',
        'en':u'Incoming date',
        'tt':u'Дата поступления'
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
    try:
        title = facet_titles[code][lang]
    except KeyError:
        title = code
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
    'i': u'статистические данные',
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
    'u': u'неизвестно',
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
    'lat':u"Латинский",
    'lav':u"Латышский",
    'lit':u"Литовский",
    'mac':u"Македонский",
    'chm':u"Марийский",
    'mon':u"Монгольский",
    'mul':u"Многоязычный",
    'ger':u"Немецкий",
    'nor':u"Норвежский",
    'per':u"Персидский",
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


@register.filter
def fond_title(code):
    #collections_dicts = cache.get('ssearch.collections')
    collections_dicts = None
    if not collections_dicts:
        collections_dicts  = get_collections()
        #cache.set('ssearch.collections', collections_dicts, 120)

    for collection_dict in collections_dicts:
        if code == collection_dict['persistant-number'][0]:
            return collection_dict['title'][0]
    return code