# -*- encoding: utf-8 -*-
import json
from lxml import etree
from lxml import etree as ET
#import xml.etree.cElementTree as ET
import time
import pymorphy

from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlquote
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render, Http404
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from guardian.core import ObjectPermissionChecker

from participants.models import Library
#catalogs = settings.ZGATE['catalogs']

from models import ZCatalog, SavedRequest, SavedDocument
import zworker
from common import humanquery

def json_error(error):
    return json.dumps({'status': 'error',
                             'error': error},
        ensure_ascii=False)

full_xslt_root = etree.parse('libcms/xsl/full_document.xsl')
full_transform = etree.XSLT(full_xslt_root)

short_xslt_root = etree.parse('libcms/xsl/short_document.xsl')
short_transform = etree.XSLT(short_xslt_root)

xslt_root = etree.parse('libcms/xsl/record_in_search.xsl')
xslt_transformer = etree.XSLT(xslt_root)

def set_cookies_to_response(cookies, response):
    for key in cookies:
        response.set_cookie(key, cookies[key])
    return response

def render_search_result(request, catalog, zresult=''):
    cookies = {}
    if zresult == '':
        url = catalog.url
        new_get = []
        for key in request.GET:
            if key == 'zstate': continue
            new_get.append(urlquote(key) + '=' + urlquote(request.GET[key]))

        new_get = '&'.join(new_get)

        if request.GET['zstate'] == 'action':
            url = url + '?' + new_get
        else:
            url = url + '?' + request.GET['zstate'].replace(' ', '+')

        (zresult, cookies) = zworker.request(url, cookies=request.COOKIES)
    try:
        zresults_body_element = zworker.get_body_element(zresult)
        zresults_body_element = zworker.change_form_action(zresults_body_element)

        zresults_body_element = zworker.change_links_href(zresults_body_element)
    except Exception:
        return HttpResponse(u'Некорректный url')
    result = zworker.make_html_body_content(zresults_body_element)

    response = render(request, 'zgate/search_results.html', {
        'catalog_title': catalog.title,
        'search_results': result
    })

    return  set_cookies_to_response(cookies, response)


def render_form(request, zresult, catalog):
    zworker.entry_point = reverse("zgate_index", args=[catalog.id])
    page_body = zworker.get_body_element(zresult)
    page_body = zworker.change_links_href(page_body)
    page_body = zworker.change_form_action(page_body)
    page_body = zworker.make_html_body_content(page_body)

    return render(request, 'zgate/search_form.html',
            {'catalog_title': catalog.title,
             'search_form': page_body,
             'catalog': catalog})


def help(request, catalog_id='', slug=''):
    if catalog_id:
        catalog = get_object_or_404(ZCatalog, id=catalog_id)
    if slug:
        catalog = get_object_or_404(ZCatalog, latin_title=slug)

    return render(request, 'zgate/help.html', {
        'catalog': catalog
    })


def render_detail(request, catalog):
    zvars = request.GET['zstate'].split(' ')
    zstate = request.GET['zstate'].replace(' ', '+')
    zgate_url = catalog.url

    (zresult, cookies) = zworker.request(zgate_url + '?' + zstate, cookies=request.COOKIES)
    zresults_body_element = zworker.get_body_element(zresult)
    zresults_body_element = zworker.change_links_href(zresults_body_element)

    #забираем xml представление записи
    (xml_record, cookies) = zworker.request(zgate_url + '?' + zstate.replace('1+F', '1+X'), cookies=request.COOKIES)
    owners = []
    record_id = '0'
    st = request.GET['zstate']
    zsession = zvars[1]
    zoffset = zvars[3]
    save_document = False
    doc = None
    try:
        xml_record = ET.XML(xml_record)
        record_tree = xml_record.xpath('/record/bibliographicRecord/*')
        if record_tree:
            doc = xslt_transformer(record_tree[0])
            doc = doc_tree_to_dict(doc)

#        owners = get_document_owners(xml_record)
#        record_id = get_record_id(xml_record)
        save_document = True
    except SyntaxError as e:
        pass #не будем добавлять держателей


    result = zworker.make_html_body_content(zresults_body_element)
    response =  render(request, 'zgate/search_results.html', {
        'doc': doc,
        'catalog_title': catalog.title,
        'search_results': result,
#        'owners': owners,
        'record_id': record_id,
        'zsession': zsession,
        'zoffset': zoffset,
        'catalog': catalog,
        'save_document': save_document,
    })
    return set_cookies_to_response(cookies, response)

@login_required
def save_requests(request, catalog):
    query = ''
    human_query = ''
    zurls = ''
    if 'TERM' in request.GET and request.GET['TERM']:
        query = request.GET['TERM']
        try:
            human_query = humanquery.HumanQuery(query).convert()
        except Exception as e:
            if settings.DEBUG:
                raise  e

    else:
        return HttpResponse(u'Неверные параметры запроса. Не указаны поисковые параметры.')

    if 'DB' in request.GET and request.GET['DB']:
        zurls = request.GET['DB']
    else:
        return HttpResponse(u'Неверные параметры запроса, Не указаны параметры баз данных.')

    saved_request = SavedRequest(zcatalog=catalog, user=request.user, zurls=zurls, query=query, human_query=human_query)
    saved_request.save()
    return render(request, 'zgate/save_request.html', {
        'saved_request': saved_request,
        'module':'zgate'
    })

def save_document(request):
    if request.method != 'POST':
        return HttpResponse('Only post requests')


    expiry_date = None
    if request.user.is_authenticated():
        owner_id = request.user.username
    elif request.session.session_key:
        owner_id = request.session.session_key
        expiry_date = request.session.get_expiry_date()
    else:
        return HttpResponse(json_error(u'Документ не может быть сохранен, возможно в Вашем браузере отключены cookies.'))

    catalog = get_object_or_404(ZCatalog, latin_title=request.POST['catalog_id'])
    zgate_url = catalog.url

    zstate = 'present+' + request.POST['zsession'] +\
             '+default+' + request.POST['zoffset'] +\
             '+1+X+1.2.840.10003.5.28+'+catalog.default_lang

    (xml_record, cookies) = zworker.request(zgate_url + '?' + zstate)

    try:
        tree = ET.XML(xml_record)
    except SyntaxError as e:
        return HttpResponse(json_error(u'Заказ не выполнен. Возможно, время сессии истекло'))

    comments = None
    if 'comments' in request.POST and request.POST['comments']:
        comments = request.POST['comments']

    try:
        doc = etree.XML(xml_record)
        result_tree = full_transform(doc)
        full_document = unicode(result_tree)

        result_tree = short_transform(doc)
        short_document = unicode(result_tree)
    except Exception, e:
        raise e

    saved_document = SavedDocument(
        zcatalog=catalog,
        owner_id=owner_id,
        document=xml_record,
        comments=comments,
        expiry_date=expiry_date,
        full_document=full_document,
        short_document=short_document
    )

    saved_document.save()

    response =  HttpResponse(json.dumps({'status': 'ok'}, ensure_ascii=False))
    return response


import uuid
from models import SearchRequestLog
morph = pymorphy.get_morph(settings.PROJECT_PATH + 'data/pymorphy/ru/cdb', 'cdb')
def log_search_request(request, catalog):

    def clean_term(term):
        """
        Возвращает кортеж из ненормализованног и нормализованного терма
        """
        terms = term.strip().lower().split()
        nn_term = u' '.join(terms)

        n_terms = []
        #нормализация
        for t in terms:
            n_term = morph.normalize(t.upper())
            if isinstance(n_term, set):
                n_terms.append(n_term.pop().lower())
            elif isinstance(n_term, unicode):
                n_terms.append(n_term.lower())

        n_term = u' '.join(n_terms)
        return (nn_term, n_term)


    search_request_id =  uuid.uuid4().hex
    term_groups = []


    term = request.POST.get('TERM_1', None)
    if term:
        forms = clean_term(term)
        term_groups.append({
            'nn': forms[0],
            'n':  forms[1],
            'use': request.POST.get('USE_1',u'not defined'),

        })

    term = request.POST.get('TERM_2', None)
    if term:
        forms = clean_term(term)
        term_groups.append({
            'nn': forms[0],
            'n':  forms[1],
            'use': request.POST.get('USE_2',u'not defined'),

        })

    term = request.POST.get('TERM_3', None)
    if term:
        forms = clean_term(term)
        term_groups.append({
            'nn': forms[0],
            'n':  forms[1],
            'use': request.POST.get('USE_3',u'not defined'),

        })

    for group in term_groups:
        SearchRequestLog(
            catalog=catalog,
            search_id=search_request_id,
            use=group['use'],
            normalize=group['n'],
            not_normalize=group['nn'],
        ).save()


@csrf_exempt
def draw_order(request, catalog_id='', slug=''):
    catalog = None
    if catalog_id:
        catalog = get_object_or_404(ZCatalog, id=catalog_id)
    elif slug:
        catalog = get_object_or_404(ZCatalog, latin_title=slug)
    else:
        raise Http404()

    id = request.GET.get('id', None)
    if not id:
        raise Http404()
    print id


    (zgate_form, cookies) = zworker.get_zgate_form(
        zgate_url=catalog.url,
        xml=catalog.xml,
        xsl=catalog.xsl,
        cookies=request.COOKIES,
        username='5881-12',
        password='AAsa5YFs',
    )
    session_id = zworker.get_zgate_session_id(zgate_form)
    form_params =  zworker.get_form_dict(zgate_form)
    del(form_params['scan'])
    form_params['use_1']='12:1.2.840.10003.3.1'
    form_params['term_1']= id
    result = zworker.request(catalog.url, data=form_params, cookies=cookies)

    if  result[0].decode('utf-8').find(u'id="%s' % (id,)) >= 0:
        link = catalog.url + '?preorder+%s+1+default+1+1.2.840.10003.5.28+rus' % session_id
        return redirect(link)
    return HttpResponse(u'Ok')

@csrf_exempt
def index(request, catalog_id='', slug=''):
    catalog = None
    if catalog_id:
        catalog = get_object_or_404(ZCatalog, id=catalog_id)
    elif slug:
        catalog = get_object_or_404(ZCatalog, latin_title=slug)
    else:
        raise Http404()


    checker = ObjectPermissionChecker(request.user)
    if not checker.has_perm('view_zcatalog', catalog):
        return HttpResponse(u'Доступ запрещен')

    if not catalog.can_search:
        return HttpResponse(u"Каталог не доступен для поиска.")

    zgate_url = catalog.url
    if request.method == 'POST' and 'SESSION_ID' in request.POST:

        log_search_request(request, catalog)
        (result, cookies) = zworker.request(zgate_url, data=request.POST, cookies=request.COOKIES)
        response =  render_search_result(request, catalog, zresult=result, )
        return set_cookies_to_response(cookies,response)

    else:
        if 'zstate' in request.GET: #а тут пользователь уже начал щелкать по ссылкам

            if 'ACTION' in request.GET and request.GET['ACTION'] == 'pq':
                return save_requests(request, catalog)

            url = zgate_url + '?' + request.GET['zstate'].replace(' ', '+')

            vars = request.GET['zstate'].split(' ')
            cookies = {}
            if vars[0] == 'form':

                try:
                    (zresult, cookies) = zworker.request(url, cookies=request.COOKIES)
                except Exception:
                    return HttpResponse(u'Получен некорретный ответ. Попробуйте осуществить поиск еще раз.')

                response = render_form(request, zresult=zresult, catalog=catalog)
                return set_cookies_to_response(cookies, response)

            elif vars[0] == 'present':
                if vars[4] == '1' and vars[5] == 'F':

                    try:
                        response = render_detail(request, catalog)
                    except Exception:
                        return HttpResponse(u'Сервер не может корректно отобразить результат. Повторите запрос еще раз.')

                    return set_cookies_to_response(cookies,response)

                response = render_search_result(request, catalog)
                return set_cookies_to_response(cookies,response)
            else:
                response = render_search_result(request, catalog)
                return set_cookies_to_response(cookies, response)
        else: #значит только инициализация формы
        #            if not catalog.can_search:
        #                return Htt

            (zgate_form, cookies) = zworker.get_zgate_form(
                zgate_url=zgate_url,
                xml=catalog.xml,
                xsl=catalog.xsl,
                cookies=request.COOKIES
            )

            response = render_form(request, zgate_form, catalog)
            return set_cookies_to_response(cookies, response)



def saved_document_list(request):
    owner_id = ''
    if request.user.is_authenticated():
        owner_id = request.user.username
    elif request.session.session_key:
        owner_id = request.session.session_key

    saved_documents = SavedDocument.objects.filter(owner_id=owner_id).order_by('-add_date')

    format = 'full'
    if 'format' in request.GET and request.GET['format'] == 'short':
        format = 'short'

    return render(request, 'zgate/saved_documents_list.html',
            {'saved_documents': saved_documents,
             'format': format,
             'module':'zgate'})



def load_documents(request):
    response = HttpResponse(content_type='application/txt')
    response['Content-Disposition'] = 'attachment; filename=documents.txt'
    if request.method == 'POST':
        owner_id = ''
        if request.user.is_authenticated():
            owner_id = request.user.username
        elif request.session.session_key:
            owner_id = request.session.session_key

        documents = []

        if 'download' in request.POST and isinstance(request.POST.getlist('download'), list) and len(request.POST.getlist('download')):
            save_requests = SavedDocument.objects.filter(pk__in=request.POST.getlist('download'), owner_id=owner_id)

            for save_request in save_requests:
                documents.append(save_request.short_document)

            response.write('\r\n'.join(documents))
        else:
            save_requests = SavedDocument.objects.filter(owner_id=owner_id)
            for save_request in save_requests:
                documents.append(save_request.short_document)

            response.write('\r\n'.join(documents))
    return response


def delete_saved_document(request, document_id=''):
    owner_id = ''
    if request.user.is_authenticated():
        owner_id = request.user.username
    elif request.session.session_key:
        owner_id = request.session.session_key

    saved_document = get_object_or_404(SavedDocument,id=document_id, owner_id=owner_id)
    saved_document.delete()
    return redirect(reverse('zgate_saved_document_list'))


@login_required
def saved_requests_list(request):

    saved_requests = SavedRequest.objects.filter(user=request.user).order_by('-add_date').select_related()
    paginator = Paginator(saved_requests, 20)
    try:

        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        saved_requests_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        saved_requests_list = paginator.page(paginator.num_pages)

    return render(request, 'zgate/saved_requests_list.html',  {
        'saved_requests_list': saved_requests_list,
        'module':'zgate'
    })



@login_required
def make_saved_request(request, request_id=''):
    saved_request = get_object_or_404(SavedRequest,id=request_id, user = request.user)


    (zgate_form, cookies) = zworker.get_zgate_form(
        zgate_url=saved_request.zcatalog.url,
        xml=saved_request.zcatalog.xml,
        xsl=saved_request.zcatalog.xsl,
        cookies=request.COOKIES
        #        username=username,
        #        password=password
    )
    session_id = zworker.get_zgate_session_id(zgate_form)
    get_params = []
    get_params.append(urlquote('zstate') + '=' + urlquote('action'))
    get_params.append(urlquote('ACTION') + '=' + urlquote('SEARCH'))
    get_params.append(urlquote('SESSION_ID') + '=' + urlquote(session_id))
    get_params.append(urlquote('LANG') + '=' + urlquote(saved_request.zcatalog.default_lang))
    get_params.append(urlquote('DBNAME') + '=' + urlquote(saved_request.zurls))
    get_params.append(urlquote('TERM_1') + '=' + urlquote(saved_request.query))
    get_params.append(urlquote('ESNAME') + '=' + urlquote('B'))
    get_params.append(urlquote('MAXRECORDS') + '=' + urlquote('20'))
    get_params.append(urlquote('CHAR_SET') + '=' + urlquote('UTF-8'))
    get_params.append(urlquote('RECSYNTAX') + '=' + urlquote('1.2.840.10003.5.28'))

    link = reverse('zgate:zgate_index', args=(saved_request.zcatalog.id,)) + '?' + '&'.join(get_params)

    response = redirect(link)
    return set_cookies_to_response(cookies, response)

@login_required
def delete_saved_request(request, request_id=''):
    saved_request = get_object_or_404(SavedRequest,id=request_id, user = request.user)
    saved_request.delete()
    return redirect(reverse('zgate_saved_requests'))
"""
xml_record ETreeElement
return list of owners
"""

def get_document_owners(xml_record):
    owner_trees = xml_record.xpath('/record/bibliographicRecord/record/field[@id="999"]/subfield[@id="a"]')
    owners = []
    for owner_tree in owner_trees:
        owners.append(owner_tree.text)

#    print etree.tostring(owners[0], encoding='utf-8')
#    def get_subfields(field_code, subfield_code):
#        subfields = []
#        fields = xml_record.findall('field')
#        for field in fields:
#            if field.attrib['id'] == field_code:
#                subfileds = field.findall('subfield')
#                for subfiled in subfileds:
#                    if subfiled.attrib['id'] == subfield_code:
#                        if subfiled.text:
#                            subfields.append(subfiled.text) # сиглы организаций (code)
#                            break
#        return subfields
#
#    #сперва ищем держателей в 850 поле
#    owners =  get_subfields('999', 'a')
#    if not owners:
#        owners =  get_subfields('899', 'a')
        #если нет то в 899

    owners_dicts = []
    if owners:
        libraries = Library.objects.filter(code__in=owners)
        for org in libraries:
            owners_dicts.append({
                'code':org.code,
                'name': org.name
            })
    return owners_dicts

"""
xml_record ETreeElement
return record id string or None if record not have id
"""

def get_record_id(xml_record):
    fields = xml_record.findall('field')
    for field in fields:
        if field.attrib['id'] == '001':
            if field.text:
                return field.text
    return None

def doc_tree_to_dict(doc_tree):
    doc_dict = {}
    for element in doc_tree.getroot().getchildren():
        attrib = element.attrib['name']
        value = element.text
        #если поле пустое, пропускаем
        if not value: continue
        #        value = beautify(value)
        values = doc_dict.get(attrib, None)
        if not values:
            doc_dict[attrib] = [value]
        else:
            values.append(value)
    return doc_dict