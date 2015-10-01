# flake8: noqa
from settings_shared import *
from ccnmtlsettings.staging import common

locals().update(
    common(
        project=project,
        base=base,
        INSTALLED_APPS=INSTALLED_APPS,
        STATIC_ROOT=STATIC_ROOT,
    ))

STATSD_PREFIX = 'nynjaetc-staging'
HRSA_ID_FIELD = 'question17'

try:
    from local_settings import *
except ImportError:
    pass
    
    
    
    
