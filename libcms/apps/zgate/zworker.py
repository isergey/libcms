# -*- coding: utf-8 -*-
import urllib, urllib2
from lxml import etree
import lxml.html
from django.utils.http import urlquote
import Cookie

entry_point = ''

def request(url, data={}, cookies={}):
    opener = urllib2.build_opener()
    cc = []
    for key in  cookies:
        cc.append( '%s=%s' % (key, cookies[key]))
    cc = '; '.join(cc)

    opener.addheaders.append(('Cookie', cc))
    if len(data):
        mrequest = data.copy()
        r = []
        #если поисковые термы не пустые, добавляем * в конец терма
        if 'TERM_1' in mrequest and len(mrequest['TERM_1']) != 0:
            mrequest['TERM_1'] += '*'
        if 'TERM_2' in mrequest and len(mrequest['TERM_2']) != 0:
            mrequest['TERM_2'] += '*'
        if 'TERM_3' in mrequest and len(mrequest['TERM_3']) != 0:
            mrequest['TERM_3'] += '*'

        if type(mrequest) == dict:
            cgi_post_params = []
            for key in  mrequest:
                cgi_post_params.append(key + '=' + urlquote(mrequest[key]))
            mrequest = '&'.join(cgi_post_params)

        else:
            mrequest = mrequest.urlencode()
        result = opener.open(url, data=mrequest)
    else:
        result = opener.open(url)
    cookies1 = []
    if 'Set-Cookie' in result.headers:
        cookies1 = Cookie.SimpleCookie(result.headers['Set-Cookie'])

    for key in cookies1:
        cookies[key]=cookies1.get(key).value

    results = result.read()
    return (results, cookies)


def get_zgate_form(zgate_url, xml, xsl, lang='rus',cookies=dict(), username=None, password=None):
#    data = {
#        'FORM_HOST_PORT': '%s,%s' % (xml, xsl),
#        'LANG': lang,
#        'ACTION': 'init',
#        }
    url =  zgate_url +'?init+%s,%s+rus' %(xml, xsl)
    if username and password:
        url += '+%s+%s' % (username, password)
    return request(url, cookies=cookies)


def get_zgate_session_id(html_string):
    """
    return None if session_id not found
    """
    tree = lxml.html.document_fromstring(html_string)
    inputs = tree.xpath('//form/input[@name="SESSION_ID"][1]')
    if len(inputs):
        return tree.xpath('//form/input[@name="SESSION_ID"][1]')[0].get('value')
    return None


def get_form_dict(html_string):
    """
    return None if session_id not found
    """
    dict = {}
    tree = lxml.html.document_fromstring(html_string)
    inputs = tree.xpath('//input')
    for input in inputs:
        name = input.get('name')
        if name:
            dict[name.lower()] = input.get('value')

    inputs = tree.xpath('//select[@name="DBNAME"]/*')
    if inputs:
        dict['dbnames'] = []
        for input in inputs:
            dict['dbnames'].append(input.get('value'))

    return dict


def is_not_founded(html_string):
    """
    return None if result containt record with calss w
    """
    tree = lxml.html.document_fromstring(html_string)
    inputs = tree.xpath('//span[@class="warn"][0]')
    return None


def get_body_element(html_string):
    """
    return body Elemnt
    """
    tree = lxml.html.document_fromstring(html_string)
    return getattr(tree, 'body', None)



def element_to_html(element):
    tree = etree.ElementTree(element)
    return etree.tostring(tree, method="html", encoding='UTF-8', )



def make_html_body_content(body_element):
    html_lines = []

    for element in list(body_element):
        html_lines.append(element_to_html(element))
    return '\n'.join(html_lines)


def href_change_list(old_href):
    if old_href:
        result = old_href.replace('zgate?form', entry_point + '?zstate=form')
        result = result.replace('zgate?present', '?zstate=present')
        result = result.replace('zgate?ACTION', '?zstate=action&ACTION')
        #result = result.replace('zgate?ACTION=SEARCH', 'show?ACTION=SEARCH')
        result = result.replace('/z3950/gateway.html', entry_point)
        return result
    return ''


def change_links_href(body_element):
    links = body_element.xpath('//a')
    for link in links:
        link.set('href', href_change_list(link.get('href')))
    return body_element


def change_form_action(body_element):
    form = body_element.xpath('//form')
    if form:
        form[0].set('action', '')
    return body_element