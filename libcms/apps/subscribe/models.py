# encoding: utf-8
import hashlib

from django.db import transaction
from django.utils import timezone
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models
from django.contrib.auth.models import User


SUBSCRIBE_FROM_EMAIL = getattr(settings, 'SUBSCRIBE_FROM_EMAIL', 'subscribe@localhost')
SITE_DOMAIN = getattr(settings, 'SITE_DOMAIN', 'localhost')
SECRET_KEY = getattr(settings, 'SECRET_KEY', '')

letter_template = get_template('subscribe/letter/base.html')


class Group(models.Model):
    name = models.CharField(verbose_name=u'Группа рассылок', max_length=255, unique=True)
    order = models.IntegerField(verbose_name=u'Порядок вывода группы', default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Группа расылок'
        verbose_name_plural = u'Группы рассылок'
        ordering = ['-order', 'name']


class Subscribe(models.Model):
    group = models.ForeignKey(Group, verbose_name=u'Группа рассылок', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(verbose_name=u'Название подписки', unique=True, max_length=255)
    code = models.SlugField(verbose_name=u'Код подписки', unique=True, max_length=32, db_index=True)
    description = models.TextField(verbose_name=u'Описание', max_length=20000, blank=True)
    is_active = models.BooleanField(verbose_name=u'Активна', default=True, db_index=True)
    order = models.IntegerField(verbose_name=u'Сортировка', db_index=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['order', 'name']
        verbose_name = u'Подписка'
        verbose_name_plural = u'Подписки'


CONTENT_FORMAT_CHOICES = (
    ('text', u"Текст"),
    ('html', u"HTML"),
)


SEX_CHOICES = (
    ('', 'не важно'),
    ('m', 'муж'),
    ('f', 'жен'),
)


class Letter(models.Model):
    subscribe = models.ForeignKey(Subscribe, verbose_name=u'Подписка')
    subject = models.CharField(verbose_name=u'Тема', max_length=255)
    content_format = models.CharField(verbose_name=u'Формат письма', max_length=16, choices=CONTENT_FORMAT_CHOICES)
    content = models.TextField(verbose_name=u'Содержимое')
    send_complated = models.BooleanField(verbose_name=u'Доставлено всем подписчикам', db_index=True, default=False)
    must_send_at = models.DateTimeField(verbose_name=u'Время отправки', db_index=True)
    age_from = models.PositiveIntegerField(verbose_name=u'Возраст от (включительно)', null=True)
    age_to = models.PositiveIntegerField(verbose_name=u'Возраст до (включительно)', null=True)
    sex = models.BooleanField(verbose_name=u'Пол', choices=SEX_CHOICES, max_length=1, blank=True, default=SEX_CHOICES[0][0])
    create_date = models.DateTimeField(verbose_name=u'Дата создания', db_index=True, auto_now_add=True)

    def __unicode__(self):
        return u'%s: %s' % (unicode(self.subscribe), self.subject)

    class Meta:
        verbose_name = u'Письмо'
        verbose_name_plural = u'Письма'


class Subscriber(models.Model):
    subscribe = models.ManyToManyField(Subscribe, verbose_name='Подписки')
    user = models.ForeignKey(User, blank=True, null=True)
    email = models.EmailField(verbose_name=u'Email', max_length=255, db_index=True, unique=True,
                              help_text=u'На этот адрес будут приходить письма рассылки')
    is_active = models.BooleanField(verbose_name=u'Активный', default=True, db_index=True)
    create_date = models.DateTimeField(verbose_name=u'Дата создания', db_index=True, auto_now_add=True)

    def __unicode__(self):
        return self.email

    class Meta:
        verbose_name = u'Подписчик'
        verbose_name_plural = u'Подписчики'


class SendStatus(models.Model):
    subscriber = models.ForeignKey(Subscriber, verbose_name=u'Подписчик')
    letter = models.ForeignKey(Letter, verbose_name=u'Письмо')
    is_sended = models.BooleanField(verbose_name=u'Отпарвлено', default=False, db_index=True)
    has_error = models.BooleanField(verbose_name=u'Ошибка при отправлении', default=False, db_index=True)
    error_message = models.CharField(verbose_name=u'Диагностика', max_length=255, blank=True)
    create_date = models.DateTimeField(verbose_name=u'Дата создания', db_index=True, auto_now_add=True)

    class Meta:
        verbose_name = u'Статус отправки письма'
        verbose_name_plural = u'Статусы отправки писем'
        unique_together = ('subscriber', 'letter')


# class SubscribeState(models.Model):
# subscribe_type = models.ForeignKey(S)
# last_letter_datetime = models.DateTimeField(verbose_name=u'Дата формирования последнего письма', db_index=True)
#     class Meta:
#         verbose_name = u'Форимрование последнего письма рассылки'
#         verbose_name_plural = u'Статусы отправки писем'
#         unique_together = ('subscriber', 'letter')


def generate_key(subscriber_id, email):
    return hashlib.md5((u'%s%s%s' % (SECRET_KEY, subscriber_id, email)).encode('utf-8')).hexdigest()


def _send_letter(letter):
    subscribers = Subscriber.objects.select_related('user').filter(
        subscribe=letter.subscribe_id,
        is_active=True
    )
    send_statuses = []

    for subscriber in subscribers.iterator():
        if len(send_statuses) > 20:
            SendStatus.objects.bulk_create(send_statuses)
            send_statuses = []
        if not SendStatus.objects.filter(subscriber=subscriber, letter=letter).exists():
            send_status = SendStatus(subscriber=subscriber, letter=letter)
            send_statuses.append(send_status)

    SendStatus.objects.bulk_create(send_statuses)
    return True


@transaction.atomic()
def send_letters():
    now = timezone.now()
    letters = Letter.objects.filter(must_send_at__lte=now, send_complated=False)
    for letter in letters:
        sended = _send_letter(letter)
        if sended:
            letter.send_complated = True
            letter.save()


def send_to_email():
    send_statuses = SendStatus.objects.select_related('subscriber', 'letter').filter(is_sended=False)
    for send_status in send_statuses.iterator():
        email_body = letter_template.render(Context({
            'title': send_status.letter.subject,
            'content': send_status.letter.content,
            'email': send_status.subscriber.email,
            'key': generate_key(send_status.subscriber_id, send_status.subscriber.email),
            'subscribe_id': send_status.letter.subscribe_id,
            'SITE_DOMAIN': SITE_DOMAIN
        }))
        message = EmailMessage(
            subject=send_status.letter.subject,
            body=email_body,
            from_email=SUBSCRIBE_FROM_EMAIL,
            to=[send_status.subscriber.email]
        )
        if send_status.letter.content_format == 'html':
            message.content_subtype = "html"

        try:
            message.send()
            send_status.is_sended = True
            send_status.save()
        except Exception as e:
            send_status.has_error = True
            send_status.error_message = unicode(e)
            send_status.save()


def clear_statuses():
    now = timezone.now()
    before_td = timezone.timedelta(days=3)
    before = now - before_td
    SendStatus.objects.filter(create_date__lte=before).delete()