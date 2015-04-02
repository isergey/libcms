# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class UserOrderTimes(models.Model):
    """
    Фиксация пользователя и время заказа
    Необходимо для оганичения заказов в течении промежутка времени
    """
    user = models.ForeignKey(User)
    order_time = models.DateTimeField(verbose_name=u"Время заказа",
        auto_now_add=True,
        db_index=True)
    order_manager_id = models.CharField(verbose_name=u'Идентификатор организации',
        max_length=32,
        db_index=True)
    order_type = models.CharField(verbose_name=u'Тип заказа',
        max_length=16,
        db_index=True)