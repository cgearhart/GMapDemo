from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from registration import signals
from registration.models import RegistrationProfile
from registration.views import RegistrationView as BaseRegistrationView


class RegistrationView(BaseRegistrationView):
    """
    Modified class from django-registration app default backend that is
    agnostic to the username field (i.e. uses the Django 1.5+ `User` model
    conventions). The standard default backend fails if a username is not
    submitted as part of a POST request (by design) - but it also does not
    check the configuration settings for the USER_MODEL, which is where the
    validation enforcement should be focused (not on the *optional* literal
    `username` field, but on the mandatory USERNAME_FIELD).
    """

    def register(self, request, **cleaned_data):
        """
        Register new user account & send activation email.
        """
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password1')
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(username,
                                                                    email,
                                                                    password,
                                                                    site)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

    def registration_allowed(self, request):
        return getattr(settings, 'REGISTRATION_OPEN', True)

    def get_success_url(self, request, user):
        return ('registration_complete', (), {})


class AccountUpdateView():
    """
    Allow users to make changes to their profile:
    - change their email address (require reauthentication) by
    creating a new user account & then changing the creation date - then
    deactivating the original account.
    - disable (delete) their account.
    - change mailing list settings.
    """
    pass
