# coding=utf-8
import os
import binascii
from PIL import Image
from django.conf import settings
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db import models
from participants.models import Library
from django.contrib.auth.models import User

MEDIA_ROOT = settings.MEDIA_ROOT

AVATAR_MEDIA_SUFFIX = 'participant_site/lib_avatars/'
AVATAR_THUMBNAIL_SIZE = (320, 240)


class LibrarySiteCard(models.Model):
    class Meta:
        permissions = [
            ['view_library_card', u'Can view library site info card'],
        ]

# class ContentManager(models.Model):
#     user = models.ForeignKey(User)
#     library = models.ForeignKey(Library)
#     can_manage_children = models.BooleanField(
#         verbose_name=u'Может управлять дочерними организациями выбранно библиотеки',
#         default=False
#     )
#
#     def clean(self):
#         if self.library.parent_id:
#             ancestors = self.library.get_ancestors().values('id')
#             if ContentManager.objects.filter(user=self.user, library__in=ancestors, can_manage_children=True).exists():
#                 raise ValidationError(u'Пользователь уже унаследовал роль менеджера от вышестоящих библиотек')
#
#     class Meta:
#         verbose_name = u'Менеджер контента библиотеки'
#         verbose_name_plural = u'Менеджеры контента библиотек'
#         unique_together = (('library', 'user'))


def get_managers(user, library):
    if user.is_superuser:
        return True

    if ContentManager.objects.filter(user=user, library=library).exists():
        return True
    # проверка случая, если пользователь унаследовал права менеджера от вышестоящей библиотеки
    if not library.parent_id:
        return False

    ancestors = library.get_ancestors().values('id')
    return ContentManager.objects.filter(user=user, library__in=ancestors, can_manage_children=True).exists()


def get_avatar_file_name(instance, arg_filename):
    filename = arg_filename.lower()
    filename_hash = str(binascii.crc32(filename.encode('utf-8')) & 0xffffffff)
    return os.path.join(AVATAR_MEDIA_SUFFIX, filename_hash[0:2], filename_hash + '.jpg')


class LibraryAvatar(models.Model):
    library = models.OneToOneField(Library, unique=True)
    avatar = models.ImageField(
        verbose_name=u'Изображение библиотеки',
        upload_to=get_avatar_file_name,
        width_field='width',
        height_field='height',
        max_length=255
    )
    width = models.IntegerField(default=0, verbose_name=u'Ширина изображения аватарки')
    height = models.IntegerField(default=0, verbose_name=u'Высота изображения аватарки')


@receiver(models.signals.post_save, sender=LibraryAvatar)
def resize_avatar(sender, **kwargs):
    instance = kwargs['instance']
    image_path = MEDIA_ROOT + unicode(instance.avatar)
    im = Image.open(image_path)
    im.thumbnail(AVATAR_THUMBNAIL_SIZE)
    im.save(image_path, "JPEG", quality=90, optimize=True, progressive=True)


@receiver(models.signals.post_delete, sender=LibraryAvatar)
def delete_avatar(sender, **kwargs):
    instance = kwargs['instance']
    image_path = MEDIA_ROOT + unicode(instance.avatar)
    if os.path.isfile(image_path) and os.access(image_path, os.W_OK):
        os.remove(image_path)
