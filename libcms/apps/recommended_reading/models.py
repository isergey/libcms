# -*- encoding: utf-8 -*-
from PIL import Image
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from core import image_utils

MEDIA_ROOT = settings.MEDIA_ROOT

ITEM_SECTIONS = (
    ('school', u'Школьная литература'),
    ('recommended', u'Рекомендуемая литература')
)

ITEM_SCHOOL_CLASSES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
    (11, 11),
)


class Item(models.Model):
    section = models.CharField(
        verbose_name='Раздел',
        max_length=32,
        db_index=True,
        choices=ITEM_SECTIONS
    )

    cover = models.ImageField(
        verbose_name=u'Обложка',
        upload_to='recommended_reading/covers/%Y/%m',
        blank=True
    )

    title = models.CharField(
        verbose_name=u'Заглавие',
        max_length=2048,
    )

    author = models.CharField(
        verbose_name=u'Автор',
        max_length=2048,
        help_text=u'Если авторов несколько, то указывать через запятую',
        blank=True
    )

    date_of_publication = models.IntegerField(
        verbose_name=u'Год публикации',
        null=True,
        blank=True
    )

    publisher = models.CharField(
        verbose_name=u'Издатель',
        max_length=2048,
        blank=True
    )

    annotation = models.TextField(
        verbose_name=u'Аннотация',
        max_length=10 * 1024,
        blank=True
    )

    school_class = models.IntegerField(
        verbose_name=u'Класс',
        null=True,
        blank=True,
        choices=ITEM_SCHOOL_CLASSES,
        help_text=u'Если издание рекомендуется школьникам - указать класс'
    )

    record_id = models.CharField(
        verbose_name=u'Идентификатор записи в каталоге',
        max_length=128,
        blank=True
    )

    published = models.BooleanField(
        verbose_name=u'Опубликовано',
        default=False,
        db_index=True
    )

    created = models.DateTimeField(
        verbose_name=u'Дата создания',
        auto_now_add=True,
        db_index=True,
    )

    updated = models.DateTimeField(
        verbose_name=u'Дата Обновления',
        auto_now=True,
        db_index=True,
    )

    class Meta:
        verbose_name = u'Издание'
        verbose_name_plural = u'Рекомендуемая литература'

    def clean(self):
        if self.section == 'school' and not self.school_class:
            raise ValidationError({
                'school_class': 'Небходимо выбрать класс'
            })

        self.record_id = self.record_id.strip()


ITEM_ATTACHMENT_TYPE_CHOICES = (
    ('pdf', 'pdf'),
    ('fb2', 'fb2'),
    ('epub', 'epub'),
)

ALLOWED_EXTENSIONS = ['pdf', 'fb2', 'epub']


def attachment_path(instance, filename):
    now = datetime.now()
    return u'recommended_reading/attachments/{0}/{1}/{2}_{3}'.format(now.year, now.month, instance.item_id, filename)


class ItemAttachment(models.Model):
    item = models.ForeignKey(Item)
    type = models.CharField(
        verbose_name=u'Тип файла',
        max_length=16,
        choices=ITEM_ATTACHMENT_TYPE_CHOICES,
        editable=False
    )
    title = models.CharField(
        verbose_name=u'Название',
        max_length=256,
        blank=True,
    )
    file = models.FileField(
        verbose_name=u'Файл',
        upload_to=attachment_path,
        help_text=u'Только файлы с расширение .pdf .fb2 .epub'
    )

    class Meta:
        verbose_name = u'Файл'
        verbose_name_plural = u'Файлы'

    def clean(self):
        cleaned_file = unicode(self.file).lower().strip()

        allowed = False
        for allow_extension in ALLOWED_EXTENSIONS:
            if cleaned_file.endswith('.' + allow_extension):
                allowed = True
                break

        if not allowed:
            raise ValidationError({
                'file': u'Файл имеет недопустимый формат'
            })

        cleaned_file = unicode(self.file).lower().strip()
        for choice in ITEM_ATTACHMENT_TYPE_CHOICES:
            if cleaned_file.endswith('.' + choice[0]):
                self.type = choice[0]
                break


ITEM_ATTRIBUTE_TYPE = (
    ('string', u'Строка'),
    ('number', u'Число'),
)


class ItemAttribute(models.Model):
    code = models.SlugField(
        verbose_name=u'Код',
        max_length=64,
        unique=True,
        help_text=u'Толькл прописные буквы латинского алфавита'
    )

    title = models.CharField(
        verbose_name=u'Название',
        max_length=256,
        help_text=u'Человекочитаемое название атрибута'
    )

    type = models.CharField(
        verbose_name=u'Тип',
        max_length=16,
        choices=ITEM_ATTRIBUTE_TYPE,
        default=ITEM_ATTRIBUTE_TYPE[0][0]
    )

    def clean(self):
        self.code = self.code.lower().strip()
        self.title = self.title.strip()

    class Meta:
        verbose_name = u'Атрибут'
        verbose_name_plural = u'Атрибуты'


class ItemAttributeValue(models.Model):
    item = models.ForeignKey(Item)
    attribute = models.ForeignKey(ItemAttribute, verbose_name=u'Атрибут')
    value = models.CharField(
        verbose_name=u'Значение',
        max_length=1024
    )

    def clean(self):
        self.value = self.value.strip()

    class Meta:
        verbose_name = u'Значение атрибута'
        verbose_name_plural = u'Значения атрибутов'


@receiver(models.signals.post_save, sender=Item)
def compress_item_cover(sender, **kwargs):
    instance = kwargs['instance']
    cover = unicode(instance.cover)
    if not cover:
        return

    image_path = MEDIA_ROOT + unicode(instance.cover)

    im = Image.open(image_path).convert('RGB')
    im = image_utils.image_crop_center(im, crop_height=600, ratio=0.67)
    im.save(image_path, "JPEG", quality=95, optimize=True, progressive=True)
