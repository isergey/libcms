# -*- encoding: utf-8 -*-
from PIL import Image
import os
import binascii
from datetime import datetime
from django.dispatch import receiver
from django.shortcuts import urlresolvers
from django.conf import settings
from django.db import models
from participants.models import Library
from attacher.frontend.views import delete_content_attaches
from core import image_utils
MEDIA_ROOT = settings.MEDIA_ROOT

AVATAR_MEDIA_SUFFIX = 'participant_news/news_images/'
AVATAR_THUMBNAIL_SIZE = (320, 240)
TMB_SUFFIX = 'tmb'


class News(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    show_avatar = models.BooleanField(verbose_name=u"Показывать аватарку", default=False)
    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"Дата создания", db_index=True)
    order = models.IntegerField(default=0, verbose_name=u'Приоритет', db_index=True, help_text=u'Новости сортируются по приоритету, далее - по дате создания. 0 - по умолчанию.')
    publicated = models.BooleanField(verbose_name=u'Опубликовано?', default=True, db_index=True)
    avatar_img_name = models.CharField(max_length=512, blank=True)
    lang = models.CharField(
        verbose_name=u"Язык", db_index=True, max_length=2, choices=settings.LANGUAGES, default=settings.LANGUAGES[0],
        help_text=u'Новость на сайте появится при соответствующем языке'
    )
    title = models.CharField(verbose_name=u'Заглавие', max_length=512)
    teaser = models.CharField(verbose_name=u'Тизер', max_length=512, help_text=u'Краткое описание новости')
    content = models.TextField(verbose_name=u'Содержание новости')

    def get_absolute_url(self):
        return urlresolvers.reverse('participant_news:frontend:show', args=[self.library.code, self.id])

    class Meta:
        ordering = ['order', '-create_date']


def get_image_file_name(instance, arg_filename):
    filename= arg_filename.lower()
    filename_hash = str(binascii.crc32(filename.encode('utf-8')) & 0xffffffff)
    return  os.path.join(AVATAR_MEDIA_SUFFIX, filename_hash[0:2], filename_hash + '.jpg')


class NewsImage(models.Model):
    news = models.ForeignKey(News)
    image = models.ImageField(max_length=255, upload_to=get_image_file_name, verbose_name=u'Изображение фотоматериалов новости')
    order = models.IntegerField(default=0, verbose_name=u'Порядок')
    is_show = models.BooleanField(default=True, verbose_name=u'Показывать фото')
    title = models.CharField(verbose_name=u'Название фото', max_length=1024, blank=True)
    description = models.TextField(verbose_name=u"Описание фото", blank=True, max_length=100000)

    def get_tmb_path(self):
        image_path = unicode(self.image)
        return os.path.dirname(image_path) + u'/' + TMB_SUFFIX + u'/' + os.path.basename(image_path)

    class Meta:
        ordering = ['-order']






@receiver(models.signals.post_save, sender=NewsImage)
def resize_news_image(sender, **kwargs):
    maximum_width =  1920
    maximum_height = 1440
    instance = kwargs['instance']
    image_path = MEDIA_ROOT + unicode(instance.image)
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



@receiver(models.signals.post_delete, sender=NewsImage)
def delete_news_image(sender, **kwargs):
    instance = kwargs['instance']
    image_path = MEDIA_ROOT + unicode(instance.image)
    if os.path.isfile(image_path) and os.access(image_path, os.W_OK):
        os.remove(image_path)


@receiver(models.signals.post_delete, sender=News)
def remove_attachments(sender, **kwargs):
    delete_content_attaches('participant_news', str(kwargs['instance'].id))
    pass

