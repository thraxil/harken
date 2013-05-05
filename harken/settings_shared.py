# Django settings for harken project.
import os.path
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'harken',
        'HOST': '',
        'PORT': 5432,
        'USER': '',
        'PASSWORD': '',
        }
}

if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'HOST': '',
            'PORT': '',
            'USER': '',
            'PASSWORD': '', }}

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=harken',
]


USE_TZ = True
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
MEDIA_ROOT = "/var/www/harken/uploads/"
MEDIA_URL = '/uploads/'
STATIC_URL = '/media/'
SECRET_KEY = ')ng#)ef_u@_^zvvu@dxm7ql-yb^_!a6%v3v^j3b(mp+)l+5%@h'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
     'django.contrib.auth.context_processors.auth',
     'django.core.context_processors.debug',
     'django.core.context_processors.request',
    )

MIDDLEWARE_CLASSES = (
    'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
)

ROOT_URLCONF = 'harken.urls'

TEMPLATE_DIRS = (
    "/var/www/harken/templates/",
    os.path.join(os.path.dirname(__file__), "templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'staticmedia',
    'django.contrib.admin',
    'munin',
    'south',
    'django_nose',
    'compressor',
    'django_statsd',
    'bootstrapform',
    'lettuce.django',
    'harken.main',
    'smoketest',
    'djcelery',
)

LETTUCE_APPS = (
    'harken.main',
)


STATSD_CLIENT = 'statsd.client'
STATSD_PREFIX = 'harken'
STATSD_HOST = '127.0.0.1'
STATSD_PORT = 8125
STATSD_PATCHES = ['django_statsd.patches.db', ]

SENTRY_REMOTE_URL = 'http://sentry.ccnmtl.columbia.edu/sentry/store/'
# remember to set the SENTRY_KEY in a local_settings.py
# as documented in the wiki
SENTRY_SITE = 'harken'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
SOUTH_TESTS_MIGRATE = False

THUMBNAIL_SUBDIR = "thumbs"
EMAIL_SUBJECT_PREFIX = "[harken] "
EMAIL_HOST = 'localhost'
SERVER_EMAIL = "harken@thraxil.org"
DEFAULT_FROM_EMAIL = SERVER_EMAIL

# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', 'sitemedia'),
)

COMPRESS_URL = "/site_media/"
COMPRESS_ROOT = "media/"

# WIND settings

AUTHENTICATION_BACKENDS = (
     'djangowind.auth.WindAuthBackend',
     'django.contrib.auth.backends.ModelBackend',)
WIND_BASE = "https://wind.columbia.edu/"
WIND_SERVICE = "cnmtl_full_np"
WIND_PROFILE_HANDLERS = ['djangowind.auth.CDAPProfileHandler']
WIND_AFFIL_HANDLERS = [
     'djangowind.auth.AffilGroupMapper',
     'djangowind.auth.StaffMapper',
     'djangowind.auth.SuperuserMapper']
WIND_STAFF_MAPPER_GROUPS = ['tlc.cunix.local:columbia.edu']
WIND_SUPERUSER_MAPPER_GROUPS = ['anp8', ]

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = True

SOLR_BASE = "http://tardar.thraxil.org:8080/solr/"

BROKER_URL = "amqp://guest:guest@localhost:5672//harken"
CELERYD_CONCURRENCY = 4
import djcelery
djcelery.setup_loader()
