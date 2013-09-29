
###############################
#### Begin custom settings ####
###############################


import dj_database_url
import os

DEBUG = False if "PRODUCTION" in os.environ else True
TEMPLATE_DEBUG = DEBUG

# apply dirname twice to climb to the parent directory of this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Serve user-uploaded media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
MEDIA_URL = '/media/'

# Serve static files from Heroku
# https://devcenter.heroku.com/articles/django-assets
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Override static/media file settings using AWS S3 (in production)
# http://blog.doismellburning.co.uk/2012/06/25/django-and-static-files/
if not DEBUG:
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
    STATIC_URL = S3_URL + 'static/'
    MEDIA_URL = S3_URL + 'media/'

# Email settings: https://docs.djangoproject.com/en/1.5/topics/email/
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Production
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', '')

# Connect to a postgre database configured in .env file
db_default = os.getenv('DATABASE_URL', 'postgres://localhost/tesla_db')
DATABASES = {'default': dj_database_url.config(default=db_default)}

# Extending the User model:
# https://geekwentfreak-raviteja.rhcloud.com/2012/
#    12/custom-user-models-in-django-1-5/
# https://docs.djangoproject.com/en/1.5/topics/auth/
#    customizing/#auth-custom-user
AUTH_USER_MODEL = 'restAPI.User'
LOGIN_REDIRECT_URL = '/'

# Required by django-registration
ACCOUNT_ACTIVATION_DAYS = 7

# Use custom authentication
# Customizing authentication backends:
# https://docs.djangoproject.com/en/dev/topics/auth/customizing/
# http://justcramer.com/2008/08/23/logging-in-with-email-addresses-in-django/
AUTHENTICATION_BACKENDS = (
    'emailRegistration.auth.backends.CaseInsensitiveBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Enable request throttling in REST framework views
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '3/sec',
        'user': '10/sec'
    }
}

# automatically append slash and redirect to urls
APPEND_SLASH = True

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Change default 'example.com' using custom fixture:
# https://docs.djangoproject.com/en/1.5/howto/initial-data/
FIXTURE_DIRS = (
    (os.path.join(BASE_DIR, 'fixtures')),  # case sensitive on Heroku
)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates"
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)


###############################
##### End custom settings #####
###############################


ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'p83-9w_w^2si_%z5a9s4=k%*2bkz=)fjoif)+3f!bv1%n!z07-'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'teslascdemo.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'teslascdemo.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'teslascdemo',
    'rest_framework',
    'registration',
    'emailRegistration',
    'restAPI',
    'storages',  # AWS static file hosting
    'django_filters',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
