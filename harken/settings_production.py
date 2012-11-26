from settings_shared import *

TEMPLATE_DIRS = (
    "/var/www/harken/harken/harken/templates",
)

MEDIA_ROOT = '/var/www/harken/uploads/'
# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/harken/harken/sitemedia'),
)

COMPRESS_ROOT = "/var/www/harken/harken/media/"
DEBUG = True
TEMPLATE_DEBUG = DEBUG

SENTRY_SITE = 'harken'
SENTRY_SERVERS = ['http://sentry.ccnmtl.columbia.edu/sentry/store/']

try:
    from local_settings import *
except ImportError:
    pass
