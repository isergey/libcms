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