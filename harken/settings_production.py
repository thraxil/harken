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
DEBUG = False
TEMPLATE_DEBUG = DEBUG

SENTRY_SITE = 'harken'
SENTRY_SERVERS = ['http://sentry.ccnmtl.columbia.edu/sentry/store/']

import logging
from raven.contrib.django.handlers import SentryHandler
logger = logging.getLogger()
# ensure we havent already registered the handler
if SentryHandler not in map(type, logger.handlers):
    logger.addHandler(SentryHandler())

    # Add StreamHandler to sentry's default so you can catch missed exceptions
    logger = logging.getLogger('sentry.errors')
    logger.propagate = False
    logger.addHandler(logging.StreamHandler())

try:
    from local_settings import *
except ImportError:
    pass
