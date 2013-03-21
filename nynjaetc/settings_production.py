# flake8: noqa
from settings_shared import *

TEMPLATE_DIRS = (
    "/var/www/nynjaetc/nynjaetc/nynjaetc/templates",
)

MEDIA_ROOT = '/var/www/nynjaetc/uploads/'
# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/nynjaetc/nynjaetc/sitemedia'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'nynjaetc',
        'HOST': '',
        'PORT': 6432, #see /etc/pgbouncer/pgbouncer.ini
        'USER': '',
        'PASSWORD': '',
        }
}

COMPRESS_ROOT = "/var/www/nynjaetc/nynjaetc/media/"
DEBUG = False
TEMPLATE_DEBUG = DEBUG

SENTRY_SITE = 'nynjaetc'
SENTRY_SERVERS = ['http://sentry.ccnmtl.columbia.edu/sentry/store/']

if 'migrate' not in sys.argv:
    INSTALLED_APPS.append('raven.contrib.django')

    import logging
    from raven.contrib.django.handlers import SentryHandler
    logger = logging.getLogger()
    # ensure we havent already registered the handler
    if SentryHandler not in map(type, logger.handlers):
        logger.addHandler(SentryHandler())
        logger = logging.getLogger('sentry.errors')
        logger.propagate = False
        logger.addHandler(logging.StreamHandler())

try:
    from local_settings import *
except ImportError:
    pass
