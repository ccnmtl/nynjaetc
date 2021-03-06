# flake8: noqa
from settings_shared import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'lettuce.db',
        'HOST': '',
        'PORT': '',
        'USER': '',
        'PASSWORD': '',
        }
    }
if os.environ.get('SELENIUM_BROWSER', False):
    # it's handy to be able to set this from an
    # environment variable
    BROWSER = os.environ.get('SELENIUM_BROWSER')
