import os.path
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'nynjaetc',
        'HOST': '',
        'PORT': 5432,
        'USER': '',
        'PASSWORD': '',
        'ATOMIC_REQUESTS': True,
    }
}

if 'test' in sys.argv or 'jenkins' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'HOST': '',
            'PORT': '',
            'USER': '',
            'PASSWORD': '',
            'ATOMIC_REQUESTS': True,
        }
    }

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
)

# BY CONTRAST, anything in this list will be tested by Jenkins,
# otherwise the build will fail.
PROJECT_APPS = [
    'nynjaetc.main',
    'nynjaetc.analytics',
    'nynjaetc.treatment_activity',
]

ALLOWED_HOSTS = ['localhost', '.ccnmtl.columbia.edu']

USE_TZ = True
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
MEDIA_ROOT = "/var/www/nynjaetc/uploads/"
MEDIA_URL = '/uploads/'
STATIC_URL = '/media/'
SECRET_KEY = ')ng#)ef_u@_^zvvu@dxm7ql-yb^_!a6%v3v^j3b(mp+)l+5%@h'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.template.context_processors.static',
    'django.template.context_processors.media',
    'stagingcontext.staging_processor',
    'djangowind.context.context_processor',
)

MIDDLEWARE_CLASSES = [
    'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'impersonate.middleware.ImpersonateMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'waffle.middleware.WaffleMiddleware',
]

ROOT_URLCONF = 'nynjaetc.urls'

TEMPLATE_DIRS = (
    "/var/www/nynjaetc/templates/",
    os.path.join(os.path.dirname(__file__), "templates"),
    os.path.join(os.path.dirname(__file__),
                 "../ve/lib/python2.7/site-packages/treebeard/templates")
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'sorl.thumbnail',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'compressor',
    'django_statsd',
    'bootstrapform',
    'debug_toolbar',
    'waffle',
    'django_jenkins',
    'smoketest',
    'django_extensions',
    'django_fields',  # this needs to be defined before nynjaetc.main
    'nynjaetc.main',
    'pagetree',
    'pageblocks',
    'quizblock',
    'impersonate',
    'registration',
    'nynjaetc.treatment_activity',
    'treebeard',
    'nynjaetc.analytics',
    'django_markwhat',
]

AUTH_PROFILE_MODULE = "main.UserProfile"

PAGEBLOCKS = [
    'pageblocks.TextBlock',
    'pageblocks.HTMLBlock',
    'pageblocks.PullQuoteBlock',
    'pageblocks.ImageBlock',
    'pageblocks.ImagePullQuoteBlock',
    'quizblock.Quiz',
    'treatment_activity.TreatmentActivityBlock',
    'treatment_activity.GenotypeActivityBlock'
]

LETTUCE_APPS = (
    'nynjaetc.main',
)
LETTUCE_SERVER_PORT = 7000

INTERNAL_IPS = ('127.0.0.1', )
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
)

STATSD_CLIENT = 'statsd.client'
STATSD_PREFIX = 'nynjaetc'
STATSD_HOST = '127.0.0.1'
STATSD_PORT = 8125

THUMBNAIL_SUBDIR = "thumbs"
EMAIL_SUBJECT_PREFIX = "[nynjaetc] "
EMAIL_HOST = 'localhost'
SERVER_EMAIL = "nynjaetc@ccnmtl.columbia.edu"
DEFAULT_FROM_EMAIL = SERVER_EMAIL

# One-week activation window; you may, of course, use a different value.
ACCOUNT_ACTIVATION_DAYS = 7

STATIC_URL = "/media/"
STATICFILES_DIRS = ("media/",)
STATIC_ROOT = "/tmp/nynjaetc/static"
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_URL = "/media/"
COMPRESS_ROOT = "media/"

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

# WIND settings

AUTHENTICATION_BACKENDS = ('djangowind.auth.SAMLAuthBackend',
                           'django.contrib.auth.backends.ModelBackend', )
CAS_BASE = "https://cas.columbia.edu/"
WIND_PROFILE_HANDLERS = ['djangowind.auth.CDAPProfileHandler']
WIND_AFFIL_HANDLERS = ['djangowind.auth.AffilGroupMapper',
                       'djangowind.auth.StaffMapper',
                       'djangowind.auth.SuperuserMapper']
WIND_STAFF_MAPPER_GROUPS = ['tlc.cunix.local:columbia.edu']
WIND_SUPERUSER_MAPPER_GROUPS = [
    'anp8', 'jb2410', 'zm4', 'egr2107',
    'sld2131', 'amm8', 'mar227', 'lrw2128']

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = True
LOGIN_REDIRECT_URL = "/"

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

ENCRYPT_EMAIL_ADDRESSES = True
ENCRYPT_HRSA_IDS = True
ENCRYPT_KEY = 'DUMMY DUMMY DUMMY DUMMY.'  # overridden by local_settings.py

# nasty hard-coded ids and slugs
HRSA_ID_FIELD = 'question88'
PRETEST_PREF_SLUG = 'pre-test'
ENDURING_MATERIALS_SECTION_ID = 110
QUIZZES_TO_REPORT = [61, 46]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}
