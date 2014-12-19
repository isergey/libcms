# coding=utf-8
import json
from lxml import etree
from django.utils import timezone
from django.conf import settings
from django.utils import translation
from django.db.models import Q
from django.template.loader import get_template
from django.template import Context, Template
from django_cron import CronJobBase, Schedule
from frontend import views
from . import rusmarc_template
from . import solr
from . import titles
from . import junimarc
from . import models
from apps.subscribe.models import Subscribe, Letter


SITE_DOMAIN = getattr(settings, 'SITE_DOMAIN', 'localhost')
translation.activate(settings.LANGUAGE_CODE)


class GenerateSubscribeLetter(CronJobBase):
    RUN_AT_TIMES = '11:00'
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'search.subscribe_job'

    def do(self):

        now = timezone.now()
        # now = timezone.datetime(year=2014, month=9, day=9)
        now_str = now.strftime('%Y%m%d')
        catalogs = [
            'BOOKS',
            'DEP',
            'ND',
            'VIDEO',
        ]

        # Книги, Раритеты, Видео, Неопубликованные документы
        for catalog in catalogs:
            title = titles.get_attr_value_title('catalog', catalog)
            (subscribe, is_created) = Subscribe.objects.get_or_create(code='income_subscribe_' + catalog, defaults={
                'name': title,
                'description': u'Ежедневная рассылка новых поступлений',
            })
            if not subscribe.is_active:
                continue

            subject = Template(u'Информация Библиотеки').render(Context({
                'catalog': title,
                'date': now
            }))

            records = get_records(now_str, catalog)
            if not records:
                continue

            send_letter(now, title, subject, subscribe, records)

        # Выпуски  журналов
        send_issues(now, now_str)

        # Статьи  журналов
        send_articles(now, now_str)

        # Новости издательств
        send_novosti_izdatelstv(now, now_str)

        # Новые книги за рубежом
        send_novye_knigi_za_rubezhom(now, now_str)

        # Все поступления
        send_all(now, now_str)


# Выпуски  журналов
def send_issues(date, str_date):
    subject = Template(u'Информация Библиотеки').render(Context({
        'date': date
    }))
    title = u'Журналы'
    (subscribe, is_created) = Subscribe.objects.get_or_create(code='income_subscribe_issues', defaults={
        'name': title,
        'description': u'Выпуски журналов',
    })

    if subscribe.is_active:
        records = get_issues(str_date)
        if records:
            send_letter(date, title, subject, subscribe, records)


def send_articles(date, str_date):
    subject = Template(u'Информация Библиотеки').render(Context({
        'date': date
    }))
    title = u'Статьи'
    (subscribe, is_created) = Subscribe.objects.get_or_create(code='income_articles', defaults={
        'name': title,
        'description': u'Статьи из журналов',
    })

    if subscribe.is_active:
        records = get_articles(str_date)
        if records:
            send_letter(date, title, subject, subscribe, records)


def send_novosti_izdatelstv(date, str_date):
    subject = Template(u'Новости издательств').render(Context({
        'date': date
    }))
    title = u'Новости издательств'
    (subscribe, is_created) = Subscribe.objects.get_or_create(code='income_novosti_izd', defaults={
        'name': title,
        'description': u'Новости издательств',
    })

    if subscribe.is_active:
        records = get_novosti_izdatelstv(str_date)
        if records:
            send_letter(date, title, subject, subscribe, records)


def send_novye_knigi_za_rubezhom(date, str_date):
    subject = Template(u'Новости издательств').render(Context({
        'date': date
    }))
    title = u'Новые киги за рубежом'
    (subscribe, is_created) = Subscribe.objects.get_or_create(code='income_novye_knigi_za_rubezhom', defaults={
        'name': title,
        'description': u'Новые книги за рубежом',
    })

    if subscribe.is_active:
        records = get_novye_knigi_za_rubezhom(str_date)
        if records:
            send_letter(date, title, subject, subscribe, records)


# Все поступления
def send_all(date, str_date):
    subject = Template(u'Информация библиотеки').render(Context({
        'date': date
    }))
    title = u'Все поступления'
    (subscribe, is_created) = Subscribe.objects.get_or_create(code='income_all', defaults={
        'name': title,
        'description': u'Все поступления',
    })

    if subscribe.is_active:
        records = []
        records += get_records(str_date, 'BOOKS')
        records += get_records(str_date, 'ND')
        records += get_issues(str_date)
        records += get_articles(str_date)
        records += get_records(str_date, 'VIDEO')

        if records:
            send_letter(date, title, subject, subscribe, records)


def create_letter(str_date, catalog=None):
    records = get_records(str_date, catalog)
    if not records:
        return None
    return records


def send_letter(date, title, subject, subscribe, records):
    template = get_template('search/subscribe/letter.html')

    html = template.render(Context({
        'title': title,
        'records': records,
        'SITE_DOMAIN': SITE_DOMAIN,
        'date': date
    }))

    Letter(
        subscribe=subscribe,
        subject=subject,
        content_format='html',
        content=html,
        must_send_at=date,
        create_date=date
    ).save()


def get_records(str_date, catalog=None):
    time_field = 'date_time_of_income_s'
    query = '%s:%s' % (time_field, str_date)

    if catalog:
        query = '%s:%s AND catalog_s:%s' % (time_field, str_date, catalog)

    return extract_records(query)


def get_issues(str_date):
    time_field = 'date_time_of_income_s'
    query = '%s:%s AND catalog_s:(MAG_F OR MAG_R) AND material_type_s:issues' % (time_field, str_date)
    return extract_records(query)


def get_articles(str_date):
    time_field = 'date_time_of_income_s'
    query = '%s:%s AND catalog_s:(MAG_F OR MAG_R) AND material_type_s:articles_reports' % (time_field, str_date)
    return extract_records(query)


def get_novosti_izdatelstv(str_date):
    time_field = 'date_time_of_income_s'
    query = '%s:%s AND linked_record_number_s:"RU/ГПНТБ России/sic/N864430"' % (time_field, str_date)
    return extract_records(query)


def get_novye_knigi_za_rubezhom(str_date):
    time_field = 'date_time_of_income_s'
    query = '%s:%s AND linked_record_number_s:"RU/ГПНТБ России/sic/N864431"' % (time_field, str_date)
    return extract_records(query)


def extract_records(query):
    result = solr.search(query, limit=100, offset=0)
    ids = []
    for doc in result.get('docs', []):
        ids.append(doc['id'])
    records_content = models.get_records(ids)
    jrecords = []
    for i, record_content in enumerate(records_content):
        record_obj = junimarc.json_schema.record_from_json(record_content.content)
        record_tree = junimarc.ruslan_xml.record_to_xml(record_obj)
        libcard = rusmarc_template.beautify(
            etree.tostring(views.transformers['libcard'](record_tree), encoding="utf-8"))
        record_dict = views.make_record_dict(views.transformers['record_dict'](record_tree, abstract='1'))
        result_row = {
            # 'item_info': _get_item_info(record_obj),
            # 'title': title,
            # 'row_number': offset + 1 + i,
            'model': record_content,
            'libcard': libcard,
            'dict': record_dict,
            # 'urls': rusmarc_template.get_full_text_url(record_obj),
            # 'highlighting': result.get('highlighting', {}).get(record_content.record_id, {})
        }
        jrecords.append(result_row)
    return jrecords