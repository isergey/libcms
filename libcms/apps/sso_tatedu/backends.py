from django.contrib.auth import get_user_model


class OauthUserBackend(object):
    def authenticate(self, user_model=None):
        if not user_model:
            return None

        return user_model

    def get_user(self, id):
        User = get_user_model()
        try:
            return User.objects.get(pk=id)
        except:
            return None