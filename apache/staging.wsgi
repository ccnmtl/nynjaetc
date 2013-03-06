import os, sys, site

# enable the virtualenv
site.addsitedir('/var/www/nynjaetc/nynjaetc/ve/lib/python2.7/site-packages')

# paths we might need to pick up the project's settings
sys.path.append('/var/www/nynjaetc/nynjaetc/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'nynjaetc.settings_staging'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
