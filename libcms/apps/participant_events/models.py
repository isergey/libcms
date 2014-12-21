# -*- encoding: utf-8 -*-
from datetime import datetime, timedelta
import os
import binascii
from PIL import Image
from django.conf import settings
from attacher.frontend.views import delete_content_attaches
from django.dispatch import receiver
from django.db import models

from django.contrib.auth.models import User

from participants.models import Library

MEDIA_ROOT = settings.MEDIA_ROOT

AVATAR_MEDIA_SUFFIX = 'participant_events/event_avatars/'
AVATAR_THUMBNAIL_SIZE = (320, 240)


class AgeCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'Назавание', unique=True)

    class Meta:
        verbose_name = u'Возрастная категория'
        verbose_name_plural = u'Возрастные категории'
        ordering = ['name']


    def __unicode__(self):
        return self.name


class EventType(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'Назавание', unique=True)

    class Meta:
        verbose_name = u'Направление'
        verbose_name_plural = u'Направления'
        ordering = ['name']

    def __unicode__(self):
        return self.name


def get_avatar_file_name(instance, arg_filename):
    filename = arg_filename.lower()
    filename_hash = str(binascii.crc32(filename.encode('utf-8')) & 0xffffffff)
    return os.path.join(AVATAR_MEDIA_SUFFIX, filename_hash[0:2], filename_hash + '.jpg')


class Event(models.Model):
    library = models.ForeignKey(Library)
    avatar = models.ImageField(max_length=255, upload_to=get_avatar_file_name, verbose_name=u'Изображение события')
    show_avatar = models.BooleanField(verbose_name=u"Показывать изображение события", default=False)

    age_category = models.ManyToManyField(AgeCategory, verbose_name=u'Возрастная категория')
    event_type = models.ManyToManyField(EventType, verbose_name=u'Направление события')

    start_date = models.DateTimeField(verbose_name=u"Дата начала",
                                      null=False, blank=False, db_index=True)
    end_date = models.DateTimeField(verbose_name=u"Дата окончания",
                                    null=False, blank=False, db_index=True)
    address = models.CharField(verbose_name=u"Место проведения",
                               max_length=512, blank=True)

    active = models.BooleanField(verbose_name=u"Активно",
                                 default=True, db_index=True)

    create_date = models.DateTimeField(auto_now=True, verbose_name=u"Дата создания", db_index=True)

    class Meta:
        verbose_name = u"мероприятие"
        verbose_name_plural = u"мероприятия"
        ordering = ['-start_date']


class EventContent(models.Model):
    event = models.ForeignKey(Event)
    lang = models.CharField(verbose_name=u"Язык", db_index=True, max_length=2, choices=settings.LANGUAGES)
    title = models.CharField(verbose_name=u'Заглавие', max_length=512)
    teaser = models.CharField(verbose_name=u'Тизер', max_length=512)
    content = models.TextField(verbose_name=u'Описание события')

    class Meta:
        unique_together = (('event', 'lang'),)


class FavoriteEvent(models.Model):
    user = models.ForeignKey(User, related_name='favorite_event_user', verbose_name=u"Пользователь")
    event = models.ForeignKey(Event, verbose_name=u"Мероприятие")


    class Meta:
        verbose_name = u"отмеченное мероприятие"
        verbose_name_plural = u"отмеченные мероприятия"


TIME_ITEMS = (
    ('min', u'мин.'),
    ('hour', u'ч.'),
    ('day', u'дн.'),
)


class EventNotification(models.Model):
    event = models.ForeignKey(Event)
    email = models.EmailField(verbose_name=u'email', max_length=255,
                              help_text=u'На этот адрес будет выслано напоминание')
    items_count = models.PositiveIntegerField(verbose_name=u'Напомнить за', default=1)
    time_item = models.CharField(verbose_name=u'Интервал', max_length=16, choices=TIME_ITEMS, default='day')
    notification_time = models.DateTimeField(verbose_name=u'Время отправки сообшения', db_index=True)
    is_notificated = models.BooleanField(default=False, db_index=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'email', 'items_count', 'time_item')


    def make_notification_time(self):
        if self.time_item == 'min':
            td = timedelta(minutes=self.items_count)
        elif self.time_item == 'hour':
            td = timedelta(hours=self.items_count)
        else:
            td = timedelta(days=self.items_count)

        self.notification_time = self.event.start_date - td


class EventComment(models.Model):
    event = models.ForeignKey(Event, verbose_name=u"Мероприятие")
    user = models.ForeignKey(User, related_name='comment_user', verbose_name=u"Пользователь")
    text = models.CharField(verbose_name=u"Текст комментария (макс. 1024 символа)",
                            max_length=1024, null=False, blank=False)
    post_date = models.DateTimeField(verbose_name=u"Дата отправления",
                                     auto_now_add=True)

    class Meta:
        verbose_name = u"комментарий"
        verbose_name_plural = u"комментарии"


class EventSubscribe(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    age_category = models.ManyToManyField(AgeCategory, verbose_name=u'Возрастная категория')
    event_type = models.ManyToManyField(EventType, verbose_name=u'Направление события')
    library = models.ForeignKey(Library)
    email = models.EmailField(verbose_name=u'Email адрес', max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)


@receiver(models.signals.post_save, sender=Event)
def remove_attachments(sender, **kwargs):
    delete_content_attaches('participant_events' + str(kwargs['instance'].library_id), str(kwargs['instance'].id))


@receiver(models.signals.post_save, sender=Event)
def resize_avatar(sender, **kwargs):
    instance = kwargs['instance']
    image_path = MEDIA_ROOT + unicode(instance.avatar)
    im = Image.open(image_path)
    image_width = im.size[0]
    image_hight = im.size[1]
    image_ratio = float(image_width) / image_hight

    box = [0, 0, 0, 0]
    if image_ratio <= 1:
        new_hight = int(image_width / 1.333)
        vert_offset = int((image_hight - new_hight) / 2)
        box[0] = 0
        box[1] = vert_offset
        box[2] = image_width
        box[3] = vert_offset + new_hight
    else:
        new_width = image_hight * 1.333
        if new_width > image_width:
            new_width = image_width
            new_hight = int(new_width / 1.333)
            vert_offset = int((image_hight - new_hight) / 2)
            box[0] = 0
            box[1] = vert_offset
            box[2] = new_width
            box[3] = vert_offset + new_hight
        else:
            gor_offset = int((image_width - new_width) / 2)
            box[0] = gor_offset
            box[1] = 0
            box[2] = int(gor_offset + new_width)
            box[3] = image_hight

    im = im.crop(tuple(box))

    final_hight = 110
    image_ratio = float(im.size[0]) / im.size[1]
    final_width = int((image_ratio * final_hight))
    im = im.resize((final_width, final_hight), Image.ANTIALIAS)
    im.save(image_path, "JPEG", quality=90, optimize=True, progressive=True)


@receiver(models.signals.post_delete, sender=Event)
def delete_avatar(sender, **kwargs):
    instance = kwargs['instance']
    image_path = MEDIA_ROOT + unicode(instance.avatar)
    if os.path.isfile(image_path) and os.access(image_path, os.W_OK):
        os.remove(image_path)
