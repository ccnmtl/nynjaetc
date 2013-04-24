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


ENCRYPT_EMAIL_ADDRESSES = True
ENCRYPT_HRSA_IDS = True
ENCRYPT_KEY = 'DUMMY DUMMY DUMMY DUMMY.' #overridden by local_settings.py



COMPRESS_ROOT = "/var/www/nynjaetc/nynjaetc/media/"
DEBUG = False
TEMPLATE_DEBUG = DEBUG
STAGING_ENV = True

STATSD_PREFIX = 'nynjaetc-staging'
SENTRY_SITE = 'nynjaetc-staging'
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
    
    
    
    
