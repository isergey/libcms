# encoding: utf-8
import re
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User, Group
from mptt.models import MPTTModel, TreeForeignKey

MAC_REGEXP = re.compile('^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$')


#
# class Country(models.Model):
# name = models.CharField(verbose_name=u'Страна', max_length=32, unique=True, db_index=True)
#
# def __unicode__(self):
# return self.name
#
# class Meta:
# verbose_name = u"Страна"
# verbose_name_plural = u"Страны"
#
#
# class City(models.Model):
# country = models.ForeignKey(Country, verbose_name=u'Страна')
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
    hidden = models.BooleanField(default=False, verbose_name='Не выводит в списке на портале', db_index=True)
    name = models.CharField(max_length=255, verbose_name=u'Название')
    code = models.CharField(
        verbose_name=u'Сигла',
        max_length=32,
        db_index=True,
        unique=True,
        validators=[RegexValidator(regex=r'^[/_\-0-9A-Za-z]+$', message=u'Допускаются цифры, _, -, латинские буквы')]
    )
    sigla = models.CharField(
        verbose_name=u'Сигла из подполя 999b',
        max_length=32, db_index=True, blank=True,
        unique=True)
    republican = models.BooleanField(verbose_name=u'Руспубликанская библиотека', default=False, db_index=True)
    types = models.ManyToManyField(LibraryType, verbose_name=u'Тип библиотеки', blank=True)

    #    country = models.ForeignKey(Country, verbose_name=u'Страна', db_index=True, blank=True, null=True)
    #    city = models.ForeignKey(City, verbose_name=u'Город', db_index=True, blank=True, null=True)
    district = models.ForeignKey(District, verbose_name=u'Район', db_index=True, blank=True, null=True)
    #    letter = models.CharField(verbose_name=u"Первая буква алфавита", help_text=u'Укажите первую букву, которой будет соответвовать фильтрация по алфавиту', max_length=1)

    profile = models.TextField(verbose_name=u'Профиль', max_length=10000, blank=True)
    phone = models.CharField(max_length=64, verbose_name=u'Телефон', blank=True)
    plans = models.TextField(verbose_name=u'Расписание работы', max_length=512, blank=True)
    postal_address = models.TextField(verbose_name=u'Адрес', max_length=512, blank=True)

    http_service = models.URLField(max_length=255, verbose_name=u'Альтернативный адрес сайта', blank=True)
    z_service = models.CharField(max_length=255, verbose_name=u'Адрес Z сервера', blank=True,
                                 help_text=u'Укажите адрес Z сревера в формате host:port (например localhost:210)')
    ill_service = models.EmailField(max_length=255, verbose_name=u'Адрес ILL сервиса', blank=True)
    edd_service = models.EmailField(max_length=255, verbose_name=u'Адрес ЭДД сервиса', blank=True)
    mail = models.EmailField(max_length=255, verbose_name=u'Адрес электронной почты', blank=True, null=True)
    mail_access = models.CharField(max_length=255, verbose_name=u'Адрес сервера электронной почты', blank=True)

    latitude = models.FloatField(db_index=True, blank=True, null=True, verbose_name=u'Географическая широта')
    longitude = models.FloatField(db_index=True, blank=True, null=True, verbose_name=u'Географическая долгота')

    weight = models.IntegerField(verbose_name=u'Порядок вывода в списке', default=100, db_index=True)

    def __unicode__(self):
        return self.name

    #    def clean(self):
    #        if Library.objects.filter(code=self.code).count():
    #            raise ValidationError(u'Номер сиглы уже занят')

    class Meta:
        verbose_name = u"Библиотека"
        verbose_name_plural = u"Библиотеки"
        permissions = (
            ("add_cbs", "Can create cbs"),
            ("change_cbs", "Can change cbs"),
            ("delete_cbs", "Can delete cbs"),
        )

    class MPTTMeta:
        order_insertion_by = ['weight']


class Department(MPTTModel):
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    parent = TreeForeignKey(
        'self',
        verbose_name=u'Отдел верхнего уровня',
        null=True,
        blank=True,
        related_name='children',
    )
    name = models.CharField(verbose_name=u'Название', max_length=255)

    class Meta:
        unique_together = ('parent', 'name')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __unicode__(self):
        return self.name


class UserLibraryPosition(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'Должность')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = u'Должность сотрудника'
        verbose_name_plural = u'Должности сотрудников'


class UserLibrary(models.Model):
    library = models.ForeignKey(Library)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    middle_name = models.CharField(verbose_name=u'Отчество', max_length=255)
    birth_date = models.DateField(verbose_name=u'Дата рождения', null=True, help_text='Формат дд.мм.гггг', blank=True)
    department = TreeForeignKey(Department, verbose_name=u'Отдел')
    position = models.ForeignKey(UserLibraryPosition, verbose_name=u'Должность')
    phone = models.CharField(verbose_name=u'Телефон', max_length=32)
    descendants_rights = models.BooleanField(
        verbose_name=u'Может управлять дочерними организациями',
        default=False
    )
    is_active = models.BooleanField(
        verbose_name=u'Активен', default=True,
        help_text=u'Активизация полномочий ролей'
    )

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = u"Пользователи организации"
        verbose_name_plural = u"Пользователи организаций"
        unique_together = ('library', 'user')


class LibraryContentEditor(models.Model):
    library = models.ForeignKey(Library)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.user.username

    def clean(self):
        from django.core.exceptions import ValidationError

        try:
            library = self.library
        except Library.DoesNotExist:
            raise ValidationError(u'Укажите организацию к которой принадлежит пользователь.')

        if self.library.parent_id:
            raise ValidationError(u'Привязка осуществляется только к ЦБС')

    class Meta:
        verbose_name = u"Редактор контента ЦБС"
        verbose_name_plural = u"Редакторы контента ЦБС"
        unique_together = ('library', 'user')


WIFI_POINT_STATUSES = (
    ('enabled', u'активна'),
    ('disabled', u'неактивна'),
)


class WiFiPoint(models.Model):
    library = models.ForeignKey(Library)
    mac = models.CharField(
        max_length=17,
        verbose_name=u'MAC адрес',
        help_text=u'Пример: 84:80:2d:2b:be:b0',
        db_index=True,
        unique=True,
        validators=[validators.MinLengthValidator(limit_value=17)]
    )
    status = models.CharField(
        max_length=16,
        verbose_name=u'Статус',
        choices=WIFI_POINT_STATUSES,
        default=WIFI_POINT_STATUSES[0][0],
        db_index=True
    )
    comments = models.TextField(max_length=10 * 1024, verbose_name=u'Комментарии', blank=True)

    def clean(self):
        self.mac = self.mac.strip().lower()
        if not MAC_REGEXP.match(self.mac):
            raise ValidationError({'mac': u'Неправильный фортам MAC адреса'})


IS_CONNECTION_EXIST_CHOICES = (
    ('none', u'нет'),
    ('gist', u'ГИСТ'),
    ('other', u'прочее'),
)

CONNECTION_TYPE_CHOICES = (
    ('adsl', u'ADSL'),
    ('vols', u'ВОЛС'),
    ('3g5g', u'3G-4G'),
)


class InternetConnection(models.Model):
    library = models.ForeignKey(Library)
    is_exist = models.CharField(
        verbose_name=u'Наличие подключения',
        max_length=16,
        choices=IS_CONNECTION_EXIST_CHOICES,
        db_index=True
    )
    connection_type = models.CharField(
        verbose_name=u'Тип подключения',
        max_length=16,
        db_index=True,
        choices=CONNECTION_TYPE_CHOICES
    )
    incoming_speed = models.IntegerField(
        verbose_name=u'Входящая скорость (Мб/сек)',
        default=0
    )
    outbound_speed = models.IntegerField(
        verbose_name=u'Исходящая скорость (Мб/сек)',
        default=0
    )


class OracleConnection(models.Model):
    library = models.ForeignKey(Library)
    active = models.BooleanField(verbose_name=u'Активно', default=True)
    connection_string = models.CharField(verbose_name=u'Строка подключения', max_length=1024)
    schema = models.CharField(
        verbose_name=u'Схема данных',
        max_length=64
    )
    username = models.CharField(verbose_name=u'Имя пользователя', max_length=64, blank=True)
    password = models.CharField(
        verbose_name=u'Пароль',
        max_length=64,
        blank=True,
        help_text=u'Если оставить пустым, будет действовать старый'
    )
    bib_databases = models.TextField(
        verbose_name=u'Список библиографических баз данных',
        max_length=1024,
        help_text=u'Имя базы с новой строки'
    )


def get_role_groups(user=None):
    if user:
        return user.groups.filter(name__startswith='role_')
    return Group.objects.filter(name__startswith='role_')


def personal_cabinet_links(request):
    links = []

    if not request.user.is_authenticated():
        return links

    user_orgs = UserLibrary.objects.filter(user=request.user)

    user_groups = [group.name for group in request.user.groups.all()]

    if 'role_mba_manager' in user_groups:
        links.append({
            'title': u'АРМ МБА',
            'href': u'http://ill.kitap.tatar.ru',
            'target': u'_blank'
        })

    if 'role_it_manager' in user_groups:
        links.append({
            'title': u'Управление сотрудниками',
            'href': _reverse(request, 'participants:administration:library_user_list')
        })

    def can_manage_site():
        site_manage_modules = [
            'participant_site',
            'participant_banners',
            'participant_events',
            'participant_menu',
            'participant_news',
            'participant_pages',
            'participant_photopolls',
            'participant_site'
        ]
        for site_manage_module in site_manage_modules:
            if request.user.has_module_perms(site_manage_module):
                return True

        return False

    if can_manage_site() and user_orgs:
        links.append({
            'title': u'Управление сайтом',
            'href': _reverse(request, 'participant_site:administration:index', args=[user_orgs[0].library.code])
        })

    if request.user.has_perms('statistics.view_all_statistic') or user_orgs:
        links.append({
            'title': u'Статистика',
            'href': _reverse(request, 'statistics:frontend:index')
        })

    return links


def user_organizations(user):
    user_libraries = UserLibrary.objects.filter(user=user)

    orgs = []

    def make_org_item(library):
        return {
            'id': library.id,
            'code': library.code,
            'sigla': library.sigla,
            'name': library.name,
            'ancestors': []
        }

    for user_library in user_libraries:
        orgs_item = make_org_item(user_library.library)
        if user_library.library.parent_id:
            ancestors = user_library.library.get_ancestors()
            for ancestor in ancestors:
                orgs_item['ancestors'].append(make_org_item(ancestor))
        orgs.append(orgs_item)

    return orgs


def get_org_by_ap_mac(ap_mac):
    try:
        wifi_point = WiFiPoint.objects.get(mac=ap_mac)
        return wifi_point.library
    except WiFiPoint.DoesNotExist:
        return None


def _reverse(request, url, args=[]):
    return u'%s://%s%s' % (request.scheme, request.get_host(), reverse(url, args=args))
