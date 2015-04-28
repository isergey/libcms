from django.contrib.auth import get_user_model


class OauthUserBackend(object):
    def authenticate(self, oauth_user):
        if not oauth_user:
            return

        user = None
        username = self.clean_username(oauth_user)

        UserModel = get_user_model()

        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            pass
        return user

    def clean_username(self, username):
        return username

    def configure_user(self, user):
        return user

    def get_user(self, id):
        User = get_user_model()
        try:
            return User.objects.get(pk=id)
        except:
            return None