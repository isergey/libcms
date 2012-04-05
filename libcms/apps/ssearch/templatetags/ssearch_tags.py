# -*- encoding: utf-8 -*-
import datetime
from django.template import Library

register = Library()

@register.filter
def date_from_isostring(isostring):
    try:
        return datetime.datetime.strptime(isostring, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return None


facet_titles = {
    'title': u'Заглавие',
    'author': u'Автор',
    'content-type': u'Тип материала',
    'date-of-publication': u'Год публикации',
    'subject-heading': u'Тематика',
    'anywhere': u'Везде',
    'code-language': u'Язык'
}

@register.filter
def facet_title(code):
    return facet_titles.get(code, code)

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
    return content_type_titles.get(code, code)


#"""
#rus
#ger
#tar
#eng
#fre
#ara
#spa
#bak
#tus
#cze
#jap
#tur
#hun
#ita
#pol
#rum
#bul
#kaz
#lat
#tib
#aze
#fiu
#per
#dut
#hin
#kaa
#por
#swe
#uzb
#chv
#mul
#ukr
#urd
#bel
#gre
#scc
#shu
#alt
#arm
#grc
#hau
#kir
#kom
#mis
#oss
#pus
#rud
#rur
#slx
#tat
#tsr
#tut
#tаr
#yor
#гар
#
#"""