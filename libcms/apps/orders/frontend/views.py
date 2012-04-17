# -*- coding: utf-8 -*-
import datetime
from lxml import etree
import urllib2
from django.conf import settings
from django.shortcuts import HttpResponse, render, get_object_or_404, Http404, redirect, urlresolvers
from django.contrib.auth.decorators import login_required

from zgate.models import ZCatalog
from zgate import zworker

from urt.models import LibReader
from participants.models import Library
from common import ThreadWorker




xslt_bib_draw = etree.parse('libcms/xsl/full_document.xsl')
xslt_bib_draw_transformer = etree.XSLT(xslt_bib_draw)

@login_required
def index(request):
    links = LibReader.objects.select_related('library').filter(user=request.user)
    return render(request, 'orders/frontend/index.html',{
        'links':links,
    })



@login_required
def lib_orders(request, id):
    library = get_object_or_404(Library, id=id)
    if not library.z_service:
        return HttpResponse(u'Отсутвуют параметры связи с базой заказаов библиотеки. Если Вы видите это сообщение, пожалуйста, сообщите администратору портала.')

    ruslan_order_urls = settings.RUSLAN_ORDER_URLS

    lib_reader = get_object_or_404(LibReader, library=library, user=request.user)

    urls = [
        ruslan_order_urls['orders'] % (lib_reader.lib_login, lib_reader.lib_password, library.z_service ,lib_reader.lib_login),
        ruslan_order_urls['books'] % (lib_reader.lib_login, lib_reader.lib_password, library.z_service, lib_reader.lib_login),
    ]
    results = ThreadWorker(_get_content,urls).do()
    for result in results:
        if isinstance(result, BaseException):
            raise result
#    print results[0].value
    orders = _get_orders(results[1].value)
    books = _get_books(results[0].value)

    return render(request, 'orders/frontend/lib_orders.html',{
        'orders':orders,
        'books': books,
        'library':library
    })

@login_required
def zorder(request, library_id):

    record_id = request.GET.get('id', None)
    if not record_id:
        raise Http404()
    library = get_object_or_404(Library, id=library_id)

    # проверяем, привязан ли zgate к библиотеке чтобы можно было перенаправить на него
    try:
        zcatalog = ZCatalog.objects.get(latin_title=library.code)
    except ZCatalog.DoesNotExist:
        return HttpResponse(u'Библиотека не может принимать электронные заказы')

    # ищем связь пользователя с библиотекой, чтобы автоматически авторизовать для заказа
    # иначе перенаправляем для установления связи

    try:
        lib_reader = LibReader.objects.get(user=request.user, library=library)
    except LibReader.DoesNotExist:
        back =  request.get_full_path()
        return redirect(urlresolvers.reverse('urt:frontend:auth',args=[library_id])+'?back='+back)


    (zgate_form, cookies) = zworker.get_zgate_form(
        zgate_url=zcatalog.url,
        xml=zcatalog.xml,
        xsl=zcatalog.xsl,
        cookies=request.COOKIES,
        username=lib_reader.lib_login,
        password=lib_reader.lib_password,
    )
    session_id = zworker.get_zgate_session_id(zgate_form)
    form_params =  zworker.get_form_dict(zgate_form)
    del(form_params['scan']) # удаляем, иначе происходит сканирование :-)
    form_params['use_1']='12:1.2.840.10003.3.1'
    form_params['term_1']= record_id
    result = zworker.request(zcatalog.url, data=form_params, cookies=cookies)

    # анализируем полученный html на содержание текса с идентификатором записи - значит нашли
    if  result[0].decode('utf-8').find(u'id="%s' % (record_id,)) >= 0:
    #        link = reverse('zgate_index', args=(catalog.id,)) + '?zstate=preorder+%s+1+default+1+1.2.840.10003.5.28+rus' % session_id
        link = zcatalog.url + '?preorder+%s+1+default+1+1.2.840.10003.5.28+rus' % session_id
        return redirect(link)

    return HttpResponse(u'Zgate order')




def _get_content(url):
    # необходимо чтобы функция имела таймаут
    uh = urllib2.urlopen(url, timeout=10)
    result = uh.read()
#    print result
    return result


def _get_orders(xml):
#    url='http://www.unilib.neva.ru/cgi-bin/zurles?z39.50r://%s:%s@ruslan.ru/ir-extend-1?8003330' % (lib_login, lib_password)
#    opener = urllib2.build_opener()
#    result = opener.open(url)
#    results = result.read()
    print 'xml', xml
    try:
        orders_root = etree.XML(xml)
    except etree.XMLSyntaxError:
        return []

    order_trees = orders_root.xpath('/result/eSTaskPackage')
    orders = []
    for order_tree in order_trees:
        order = {}
        record_tree = order_tree.xpath('taskSpecificParameters/targetPart/itemRequest/record')
        if record_tree:
            try:
                bib_record = xslt_bib_draw_transformer(record_tree[0],abstract='false()')
                order['record'] = etree.tostring(bib_record, encoding='utf-8').replace('<b/>', '')
            except etree.XSLTApplyError as e:
                order['record'] = e.message

        status_or_error_report =  order_tree.xpath('taskSpecificParameters/targetPart/statusOrErrorReport')
        if status_or_error_report:
            order['status_or_error_report'] = status_or_error_report[0].text
        else:
            order['status_or_error_report'] = u'undefined'

        target_reference =  order_tree.xpath('targetReference')
        if target_reference:
            order['target_reference'] = target_reference[0].text
        else:
            order['target_reference'] = u'undefined'

        task_status =  order_tree.xpath('taskStatus')
        if task_status:
            status_titles = {
                '0': u'Не выполнен',
                '1': u'Отказ',
                '2': u'Выполнен',
                '3': u'Выдан'
            }
            order['task_status'] = status_titles.get(task_status[0].text,task_status[0].text)
        else:
            order['task_status'] = u'undefined'

        creation_date_time =  order_tree.xpath('creationDateTime')
        if creation_date_time:
            try:
                date =  datetime.datetime.strptime(creation_date_time[0].text, '%Y%m%d%H%M%S')
            except ValueError:
                date = u'value error'
            order['creation_date_time'] = date
        else:
            order['creation_date_time'] = u'undefined'


        orders.append(order)
    return orders

def _get_books(xml):
#    url='http://www.unilib.neva.ru/cgi-bin/zurlcirc?z39.50r://%s:%s@ruslan.ru/circ?8003330' % (lib_login, lib_password)
#    opener = urllib2.build_opener()
#    result = opener.open(url)
#    results = result.read()
    try:
        rcords_root = etree.XML(xml)
    except etree.XMLSyntaxError:
        return []
    books = []
    record_trees = rcords_root.xpath('/records/*')
    for record_tree in record_trees:
        book = {}
        try:
            bib_record = xslt_bib_draw_transformer(record_tree, abstract='false()')
            book['record'] = etree.tostring(bib_record, encoding='utf-8')
        except etree.XSLTApplyError as e:
            book['record'] = e.message

        description_tree = record_tree.xpath('field[@id="999"]/subfield[@id="z"]')
        if description_tree:
            book['description'] = description_tree[0].text
        else:
            book['description'] = u''
        books.append(book)
    return books
