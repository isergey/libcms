# coding=utf-8
from django.utils import timezone
from django.conf import settings
from django.utils import translation
from django.db.models import Q
from django.template.loader import get_template
from django.template import Context, Template
from django_cron import CronJobBase, Schedule

from .models import News
from apps.subscribe.models import Subscribe, Letter


SITE_DOMAIN = getattr(settings, 'SITE_DOMAIN', 'localhost')
translation.activate(settings.LANGUAGE_CODE)

NEWS_LIMIT_COUNT = 10
MAXIMUM_LAST_DAYS = 7


class GenerateSubscribeLetter(CronJobBase):
    RUN_EVERY_MINS = 60
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'news.subscribe_job'

    def do(self):
        now =  timezone.now()
        before = (now - timezone.timedelta(days=MAXIMUM_LAST_DAYS)).replace(hour=0, minute=0, second=0)

        (subscribe, is_created) = Subscribe.objects.get_or_create(code='news_subscribe', defaults={
            'name': u'Новости',
            'description': u'Ежедневная рассылка новостей',
        })
        if not subscribe.is_active:
            return
        news_criteria = Q(create_date__lt=now, publicated=True)
        last_letters = Letter.objects.filter(subscribe=subscribe).order_by('-create_date')[:1]

        if last_letters:
            before = last_letters[0].create_date

        news_criteria &= Q(create_date__gte=before)

        news_count = News.objects.filter(news_criteria).count()
        if news_count > NEWS_LIMIT_COUNT:
            news_count = NEWS_LIMIT_COUNT

        if news_count == 0:
            return

        subject = Template(u'Новости за {{ date|date:"j E Y" }}').render(Context({
            'date': now
        }))

        news = News.objects.filter(news_criteria).order_by('-create_date')[:news_count]

        if news:
            template = get_template('news/subscribe/letter.html')
            html = template.render(Context({
                'news_list': news,
                'SITE_DOMAIN': SITE_DOMAIN,
                'date': now
            }))
            Letter(
                subscribe=subscribe,
                subject=subject,
                content_format='html',
                content=html,
                must_send_at=now,
                create_date=now
                ).save()


