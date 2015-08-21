# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from django.db import models


class GroupTitle(models.Model):
    group = models.OneToOneField(Group, unique=True)
    title = models.CharField(
        verbose_name=u'Название группы',
        unique=True,
        max_length=255,
        help_text=u'Человекочитаемое название группы'
    )


# class Permissions(User):
#     """
#     Класс для создания прав достпа
#     """
#     class Meta:
#         proxy = True
#         permissions = (
#             ("view_users", "Can view users list"),
#             ("view_groups", "Can view groups list"),
#         )

class RegConfirm(models.Model):
    hash = models.CharField(max_length=32, db_index=True, null=False, blank=False)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True, db_index=True)


class Password(models.Model):
    user = models.OneToOneField(User, related_name=u'user_password')
    password = models.CharField(max_length=1024, blank=True)


def create_or_update_password(user, password):
    try:
        user_password = Password.objects.get(user=user)
        user_password.password = password
    except Password.DoesNotExist:
        user_password = Password(user=user, password=password)

    user_password.save()
    return user_password
