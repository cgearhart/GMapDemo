
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User


class CaseInsensitiveBackend(object):
    """
    Custom user authentication backend to force email addresses lowercase
    before authentication.

    Customizing authentication backends:
    https://docs.djangoproject.com/en/dev/topics/auth/customizing/
    http://justcramer.com/2008/08/23/logging-in-with-email-addresses-in-django/
    """

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(**{User.USERNAME_FIELD:
                                       User.objects.normalize(username)})
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
