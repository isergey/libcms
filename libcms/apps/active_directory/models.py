# coding=utf-8
from django.db import models
from django.contrib.auth.models import User, Group


class AdUser(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    login = models.CharField(max_length=255, unique=True ,verbose_name=u'Имя пользователя в AD')

    @staticmethod
    def get_or_create(username, first_name=u'', last_name=u'', email=u'', is_active=True):
        (ad_user, created) = AdUser.objects.get_or_create(login=username)
        (user, created) = User.objects.get_or_create(
            username=u'%s@ad' % ad_user.pk, first_name=first_name,
            last_name=last_name, email=email, is_active=is_active
        )

        if created:
            ad_user.user = user
            ad_user.save()
            try:
                users_group = Group.objects.get(name='users')
                users_group.user_set.add(user)
            except Group.DoesNotExist:
                pass

        return (ad_user, user)

    def __unicode__(self):
        return unicode(self.login)

    class Meta:
        verbose_name = u'Пользователь AD'
        verbose_name_plural = u'Пользователи AD'