# flake8: noqa
from settings_shared import *
import os

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
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

AWS_STORAGE_BUCKET_NAME = "ccnmtl-nynjaetc-static-prod"
AWS_PRELOAD_METADATA = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'cacheds3storage.CompressorS3BotoStorage'
S3_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = 'https://%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_URL = STATIC_URL
DEFAULT_FILE_STORAGE = 'cacheds3storage.MediaRootS3BotoStorage'
MEDIA_URL = S3_URL + '/media/'
COMPRESS_STORAGE = 'cacheds3storage.CompressorS3BotoStorage'
AWS_QUERYSTRING_AUTH = False

SENTRY_SITE = 'nynjaetc'
SENTRY_SERVERS = ['http://sentry.ccnmtl.columbia.edu/sentry/store/']
ALLOWED_HOSTS = ['learn.nynjaetc.org']

if 'migrate' not in sys.argv:
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')

try:
    from local_settings import *
except ImportError:
    pass
