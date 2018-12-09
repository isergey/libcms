# -*- encoding: utf-8 -*-
from PIL import Image
import os
import binascii
from django.utils.translation import get_language
from django.dispatch import receiver
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from participants.models import Library
from core import image_utils

MEDIA_ROOT = settings.MEDIA_ROOT

AVATAR_MEDIA_SUFFIX = 'participant_photopolls/avatars/'
IMAGES_MEDIA_SUFFIX = 'participant_photopolls/images/'

AVATAR_THUMBNAIL_SIZE = (320, 240)

TMB_SUFFIX = 'tmb'


def get_avatar_file_name(instance, arg_filename):
    filename = arg_filename.lower()
    filename_hash = str(binascii.crc32(filename.encode('utf-8')) & 0xffffffff)
    return os.path.join(AVATAR_MEDIA_SUFFIX, filename_hash[0:2], filename_hash + '.jpg')


class Poll(models.Model):
    library = models.ForeignKey(Library)
    avatar = models.ImageField(max_length=255, upload_to=get_avatar_file_name, verbose_name=u'Аватар голосования')
    show_avatar = models.BooleanField(verbose_name=u"Показывать изображение события", default=False)

    start_date = models.DateTimeField(verbose_name=u"Дата начала голосования",
                                      null=False, blank=False, db_index=True)
    end_date = models.DateTimeField(verbose_name=u"Дата окончания голосования",
                                    null=False, blank=False, db_index=True)

    publicated = models.BooleanField(
        verbose_name=u'Опубликовано', default=False, db_index=True,
        help_text=u'Опубликовывайте фотоконкурс только после загрузки фотографий и полной подготовки описания'
    )

    multi_vote = models.BooleanField(
        verbose_name=u'Возможность проголосовать за несколько вариантов', default=False,
        help_text=u'Пользователь получит возможность проголосовать сразу за несколько фотографий'
    )

    show_after_end = models.BooleanField(
        verbose_name=u'Отображать голосование после окончания срока', default=False,
        help_text=u'После окончания срока голосования, оно будет отображаться на сайе'
    )

    show_results_after_end = models.BooleanField(
        verbose_name=u'Отображать результаты голосование после окончания срока', default=False,
    )

    show_results_before_end = models.BooleanField(
        verbose_name=u'Отображать результаты голосование до окончания срока', default=False,
    )
    show_results_after_vote = models.BooleanField(
        verbose_name=u'Отображать результаты после отдачи голоса', default=False
    )

    only_auth = models.BooleanField(verbose_name=u'Могут голосовать только авторизированные пользователи',
                                    default=False)
    premoderate_comments = models.BooleanField(verbose_name=u'Премодерация комментариев', default=True)
    create_date = models.DateTimeField(auto_now_add=True, db_index=True)

    def get_cur_lang_content(self):
        cur_language = get_language()
        try:
            content = PollContent.objects.get(poll=self, lang=cur_language[:2])
        except PollContent.DoesNotExist:
            content = None
        return content

    class Meta:
        ordering = ['-create_date']


class PollContent(models.Model):
    poll = models.ForeignKey(Poll)
    lang = models.CharField(verbose_name=u"Язык", db_index=True, max_length=2, choices=settings.LANGUAGES)
    title = models.CharField(verbose_name=u'Заглавие', max_length=512)
    teaser = models.CharField(verbose_name=u'Тизер', max_length=512)
    content = models.TextField(verbose_name=u'Описание')

    class Meta:
        unique_together = (('poll', 'lang'),)


def get_image_file_name(instance, arg_filename):
    filename = arg_filename.lower()
    filename_hash = str(binascii.crc32(filename.encode('utf-8')) & 0xffffffff)
    return os.path.join(IMAGES_MEDIA_SUFFIX, filename_hash[0:2], filename_hash + '.jpg')


class PollImage(models.Model):
    poll = models.ForeignKey(Poll)
    image = models.ImageField(max_length=255, upload_to=get_image_file_name,
                              verbose_name=u'Изображение фотоматериалов новости')
    order = models.IntegerField(default=0, verbose_name=u'Порядок')
    is_show = models.BooleanField(default=True, verbose_name=u'Показывать фото')

    def get_tmb_path(self):
        image_path = unicode(self.image)
        return os.path.dirname(image_path) + u'/' + TMB_SUFFIX + u'/' + os.path.basename(image_path)

    def get_cur_lang_content(self):
        cur_language = get_language()
        try:
            content = PollImageContent.objects.get(poll_image=self, lang=cur_language[:2])
        except PollImageContent.DoesNotExist:
            content = None
        return content

    class Meta:
        ordering = ['-order']


class PollImageContent(models.Model):
    poll_image = models.ForeignKey(PollImage)
    lang = models.CharField(verbose_name=u"Язык", db_index=True, max_length=2, choices=settings.LANGUAGES)
    title = models.CharField(verbose_name=u'Название фото', max_length=1024, blank=True)
    description = models.TextField(verbose_name=u"Описание фото", blank=True, max_length=100000)

    class Meta:
        unique_together = (('poll_image', 'lang'),)


class Vote(models.Model):
    poll_image = models.ForeignKey(PollImage)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    ip = models.CharField(max_length=255, db_index=True)
    vote_date = models.DateTimeField(db_index=True, auto_now_add=True)


class Comment(models.Model):
    poll_image = models.ForeignKey(PollImage)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    comment = models.TextField(max_length=10000, verbose_name=u'Текст комментария')
    create_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-create_date']


@receiver(models.signals.post_save, sender=Poll)
def resize_poll_avatar(sender, **kwargs):
    instance = kwargs['instance']
    image_path = os.path.join(MEDIA_ROOT, unicode(instance.avatar))
    im = Image.open(image_path).convert('RGB')
    tumbnail = image_utils.image_crop_center(im)
    tumbnail.save(image_path, "JPEG", quality=95, optimize=True, progressive=True)


@receiver(models.signals.post_save, sender=PollImage)
def resize_poll_image(sender, **kwargs):
    maximum_width = 1920
    maximum_height = 1440
    instance = kwargs['instance']
    image_path = os.path.join(MEDIA_ROOT, unicode(instance.image))
    im = Image.open(image_path).convert('RGB')

    resized_im = image_utils.adjust_image(im, [maximum_width, maximum_height])
    resized_im.save(image_path, "JPEG", quality=95, optimize=True, progressive=True)

    tumbnail = image_utils.image_crop_center(resized_im)

    dir_name = os.path.dirname(image_path)
    file_name = os.path.basename(image_path)
    tumbnail_dir = os.path.join(dir_name, TMB_SUFFIX)
    tumbnail_path = os.path.join(tumbnail_dir, file_name)
    if not os.path.exists(tumbnail_dir):
        os.makedirs(tumbnail_dir)
    tumbnail.save(tumbnail_path, "JPEG", quality=95, optimize=True, progressive=True)


@receiver(models.signals.post_delete, sender=Poll)
def delete_poll_avatar(sender, **kwargs):
    instance = kwargs['instance']
    image_path = os.path.join(MEDIA_ROOT, unicode(instance.avatar))
    if os.path.isfile(image_path) and os.access(image_path, os.W_OK):
        os.remove(image_path)


@receiver(models.signals.post_delete, sender=PollImage)
def delete_poll_image(sender, **kwargs):
    instance = kwargs['instance']
    image_path = os.path.join(MEDIA_ROOT, unicode(instance.image))
    if os.path.isfile(image_path) and os.access(image_path, os.W_OK):
        os.remove(image_path)
