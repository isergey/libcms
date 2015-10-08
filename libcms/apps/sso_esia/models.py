import json
from django.db import models


class EsiaUser(models.Model):
    oid = models.CharField(max_length=32, db_index=True, unique=True)
    user_attrs = models.TextField(max_length=101024)
    trusted = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    create_data = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


def create_or_update_esia_user(oid, user_attrs, trusted=False, deleted=False, active=True):
    user_attrs_json = user_attrs

    if isinstance(user_attrs, object):
        user_attrs_json = json.dumps(user_attrs, ensure_ascii=False, encoding='utf-8').decode('utf-8')

    try:
        esia_user = EsiaUser.objects.get(oid=oid)
    except EsiaUser.DoesNotExist:
        esia_user = EsiaUser(oid=oid, user_attrs=user_attrs_json, trusted=trusted, active=active, deleted=deleted)
        esia_user.save()
        return esia_user

    need_update = False

    if esia_user.user_attrs != user_attrs_json:
        esia_user.user_attrs = user_attrs_json
        need_update = True

    if esia_user.trusted != trusted:
        esia_user.trusted = trusted
        need_update = True

    if esia_user.active != active:
        esia_user.active = active
        need_update = True

    if esia_user.deleted != deleted:
        esia_user.deleted = deleted
        need_update = True

    if need_update:
        esia_user.save()

    return esia_user
