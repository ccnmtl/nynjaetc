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
STAGING_ENV = True

STATSD_PREFIX = 'nynjaetc-staging'
HRSA_ID_FIELD = 'question17'

if 'migrate' not in sys.argv:
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')

try:
    from local_settings import *
except ImportError:
    pass
    
    
    
    
