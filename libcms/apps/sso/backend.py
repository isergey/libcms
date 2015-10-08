from django.contrib.auth.models import User
from . import models


class SSOBackend(object):
    def authenticate(self, external_username, auth_source):
        return models.find_external_user(external_username, auth_source)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
