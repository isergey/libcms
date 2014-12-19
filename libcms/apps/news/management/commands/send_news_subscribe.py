# encoding: utf-8
from django.conf import settings
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from django.utils import translation
from django.template.loader import get_template
from django.template import Context

from ...models  import News
from apps.subscribe.models import Letter, SubscribeType


class Command(BaseCommand):
    help = 'Send news to subscribe'

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        news_type = u'main'
        subscribe_type_code = u'main_news'
        now = datetime.now()
        before = now - timedelta(days=1)
        try:
            subscribe_type = SubscribeType.objects.get(code=subscribe_type_code)
        except SubscribeType.DoesNotExist:
            self.stderr.write(u"%s Subscribe type %s is not exist" % (unicode(now), unicode(subscribe_type_code)))
            return

        news_candidates = News.objects.filter(type=news_type,create_date__year=before.year, create_date__month=before.month, create_date__day=before.day)
        if not news_candidates:
            return

        template = get_template('news/subscribe/letter.html')


        letter_text = template.render(Context({
            "news_list": news_candidates,
            "date": before,
            "SITE_DOMAIN": settings.SITE_DOMAIN
        }))
        letter =  Letter(
            subscribe_type=subscribe_type,
            title=u'Новости СИЦ за %s.' % (unicode(before.strftime('%d.%m.%Y')),),
            content=letter_text
        )

        letter.save()
        self.stdout.write(u"%s Letter with subscribe type %s is sucsessfull build \n" % (unicode(before.strftime('%d %h %Y')), unicode(subscribe_type_code)))