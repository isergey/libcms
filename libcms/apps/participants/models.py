# encoding: utf-8
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

#
#class Country(models.Model):
#    name = models.CharField(verbose_name=u'Страна', max_length=32, unique=True, db_index=True)
#
#    def __unicode__(self):
#        return self.name
#
#    class Meta:
#        verbose_name = u"Страна"
#        verbose_name_plural = u"Страны"
#
#
#class City(models.Model):
#    country = models.ForeignKey(Country, verbose_name=u'Страна')
#    name = models.CharField(verbose_name=u'Город', max_length=32, unique=True, db_index=True)
#
#    def __unicode__(self):
#        return u'%s: %s' % (self.country.name, self.name)
#
#    class Meta:
#        unique_together = ("country", "name"),
#        verbose_name = u"Город"
#        verbose_name_plural = u"Города"
#
#
class District(models.Model):
    name = models.CharField(verbose_name=u'Район', max_length=32, db_index=True, unique=True)

    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        verbose_name = u"Район"
        verbose_name_plural = u"Районы"


class LibraryType(models.Model):
    name = models.CharField(verbose_name=u"Тип библиотеки", max_length=64, unique=True)
    def __unicode__(self):
        return self.name



class Library(MPTTModel):
    parent = TreeForeignKey(
        'self',
        verbose_name=u'ЦБС или библиотека верхнего уровня',
        null=True,
        blank=True,
        related_name='children',
    )
    name = models.CharField(max_length=255, verbose_name=u'Название')
    code = models.CharField(verbose_name=u'Сигла', max_length=32, db_index=True, unique=True)
    types = models.ManyToManyField(LibraryType, verbose_name=u'Тип библиотеки', blank=True, null=True)

#    country = models.ForeignKey(Country, verbose_name=u'Страна', db_index=True, blank=True, null=True)
#    city = models.ForeignKey(City, verbose_name=u'Город', db_index=True, blank=True, null=True)
    district = models.ForeignKey(District, verbose_name=u'Район', db_index=True, blank=True, null=True)
#    letter = models.CharField(verbose_name=u"Первая буква алфавита", help_text=u'Укажите первую букву, которой будет соответвовать фильтрация по алфавиту', max_length=1)

    profile = models.TextField(verbose_name=u'Профиль', max_length=10000, blank=True)
    phone = models.CharField(max_length=64, verbose_name=u'Телефон', blank=True)
    plans = models.TextField(verbose_name=u'Расписание работы', max_length=512, blank=True)
    postal_address = models.TextField(verbose_name=u'Адрес', max_length=512, blank=True)


    http_service = models.URLField(max_length=255, verify_exists=False, verbose_name=u'Адрес сайта', blank=True)
    z_service = models.CharField(max_length=255, verbose_name=u'Адрес Z сервера', blank=True, help_text=u'Укажите адрес Z сревера в формате host:port (например localhost:210)')
    ill_service = models.EmailField(max_length=255, verbose_name=u'Адрес ILL сервиса', blank=True)
    edd_service = models.EmailField(max_length=255, verbose_name=u'Адрес ЭДД сервиса', blank=True)
    mail = models.EmailField(max_length=255, verbose_name=u'Адрес электронной почты', blank=True, null=True)
    mail_access = models.CharField(max_length=255, verbose_name=u'Адрес сервера электронной почты', blank=True)

    latitude = models.FloatField(db_index=True, blank=True, null=True, verbose_name=u'Географическая широта')
    longitude = models.FloatField(db_index=True, blank=True, null=True, verbose_name=u'Географическая долгота')

    weight = models.IntegerField(verbose_name=u'Порядок вывода в списке', default=100, db_index=True)

    def __unicode__(self):
        if self.is_root_node():
            return self.name
        return self.name

#    def clean(self):
#        if Library.objects.filter(code=self.code).count():
#            raise ValidationError(u'Номер сиглы уже занят')

    class Meta:
        verbose_name = u"Библиотека"
        verbose_name_plural = u"Библиотеки"

    class MPTTMeta:
        order_insertion_by=['weight']

class UserLibrary(models.Model):
    library = models.ForeignKey(Library)
    user = models.ForeignKey(User, unique=True)

    def __unicode__(self):
        return self.user.username

    def clean(self):
        from django.core.exceptions import ValidationError
        try:
            library = self.library
        except Library.DoesNotExist:
            raise ValidationError(u'Укажите организацию к которой принадлежит пользователь.')
        if not library.ill_service:
            raise ValidationError(u'У библиотеки нет ill адреса, она не сможет получать заказы. ill адрес необходимо узнать у администратора службы МБА и присвоить его библиотеке.')

    class Meta:
        verbose_name = u"Пользователь библиотеки"
        verbose_name_plural = u"Пользователи библиотеки"


