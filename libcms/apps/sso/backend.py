from django.contrib.auth.models import User



class SSOBackend(object):
    def authenticate(self, user_model):
        try:
            return User.objects.get(pk=user_model.pk)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
