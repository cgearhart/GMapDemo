
from random import choice

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager as BaseUserManager
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

from django.core.signals import request_started
from django.dispatch import receiver


class UserManager(BaseUserManager):
    """
    UserManager subclasses the default django UserManager class to handle
    user account creation
    """

    def create_user(self,
                    username=None,
                    email=None,
                    password=None,
                    **extra_fields):
        """
        Create a new `User` instance using the supplied email address as
        the USERNAME_FIELD, and ignoring the `username` argument. The supplied
        `username` argument is only included in the method prototype so that
        the manager is compatible with forms and views that do not correctly
        implement the Django v1.5+ `User` model and require a username field.
        """
        if not email:
            raise ValueError('Accounts require an email address.')
        email = self.normalize(email)  # force email addresses lowercase
        user = self.model(email=email,
                          is_staff=False,
                          is_active=True,
                          is_superuser=False)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create a new `User` and set admin permissions."""
        su = self.create_user(email=email,
                              password=password,
                              **extra_fields)
        su.is_staff = True
        su.is_active = True
        su.is_superuser = True
        su.save(using=self._db)
        return su

    def normalize(self, field):
        """Force strings to lowercase & strip leading/trailing whitespace."""
        return field.lower().strip()


class User(AbstractBaseUser, PermissionsMixin):
    """
    `User` extends the default Django `User` model to use an email address as
    account username and add app-specific fields.

    https://geekwentfreak-raviteja.rhcloud.com/2012/
        12/custom-user-models-in-django-1-5/

    Custom User objects are not completely supported by the django-regsitration
    v1.0 module `default` backend implementation.
    """
    # Set dynamic username lookup field
    USERNAME_FIELD = 'email'

    # Link to the model handler that should be used as the interface to the db
    objects = UserManager()

    email = models.EmailField(_('E-mail Address'),
                              max_length=254,
                              unique=True,
                              )
    is_staff = models.BooleanField(_('Staff'),
                                   default=False,
                                   help_text="Designates whether the user has \
                                             admin privileges.",
                                   )
    is_active = models.BooleanField(_('Active Status'),
                                    default=True,
                                    )
    date_joined = models.DateTimeField(_('Date Joined'),
                                       auto_now_add=True,
                                       )
    mailing_list = models.BooleanField(_('Receive E-mail Updates'),
                                       default=True,
                                       )

    def _set_username(self):
        return getattr(self, User.USERNAME_FIELD)

    def _get_username(self, value):
        pass

    # Adding a false `username` field ensures compatibility with apps that
    # expect a default Django `User` model instance
    username = property(_get_username, _set_username)

    # Required for permissions
    def get_full_name(self):
        return self.email

    # Required for permissions
    def get_short_name(self):
        name_parts = self.email.partition('@')
        return name_parts[0]

    # Required for sending actiavtion email
    def email_user(self, subject, message, from_email=None):
        """Initiates sending an email to the specified user."""
        send_mail(subject, message, from_email, [self.email])


class Station(models.Model):

    STATUS = (
        ('OP', 'Operational'),  # green
        ('SM', 'Scheduled Maintenance'),  # blue
        ('US', 'Unscheduled Maintenance'),  # yellow
        ('OS', 'Out of Service'),  # red
        )

    # User-defined fields
    lat = models.FloatField(_("Latitutde"),
                            blank=False,
                            )
    lon = models.FloatField(_("Longitude"),
                            blank=False,
                            )
    stat = models.CharField(_("Status"),
                            max_length=150,
                            choices=STATUS,
                            blank=False,
                            )


@receiver(request_started)
def randomize_stat(sender, **kwargs):
    """
    Randomize status of each station on requests
    """
    station = choice(Station.objects.all())
    station.stat = choice(Station.STATUS)[0]
    station.save()
