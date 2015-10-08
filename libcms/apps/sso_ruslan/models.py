# encoding: utf-8
from django.db import models
from django.contrib.auth.models import User


class RuslanUser(models.Model):
    user = models.OneToOneField(User)
    username = models.CharField(verbose_name=u'Логин', max_length=255, db_index=True)
    password = models.CharField(verbose_name=u'Пароль', max_length=255, db_index=True)

    class Meta:
        verbose_name = u'Пользователь RUSLAN'
        verbose_name_plural = u'Пользователи RUSLAN'


def get_ruslan_user(request):
    if not request.user.is_authenticated():
        return None
    try:
        return RuslanUser.objects.get(user=request.user)
    except RuslanUser.DoesNotExist:
        return None