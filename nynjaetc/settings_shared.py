import os.path
from ccnmtlsettings.shared import common

project = 'nynjaetc'
base = os.path.dirname(__file__)

locals().update(
    common(
        project=project,
        base=base,
    ))

PROJECT_APPS = [
    'nynjaetc.main',
    'nynjaetc.analytics',
    'nynjaetc.treatment_activity',
]

USE_TZ = True
SECRET_KEY = ')ng#)ef_u@_^zvvu@dxm7ql-yb^_!a6%v3v^j3b(mp+)l+5%@h'

INSTALLED_APPS += [  # noqa
    'sorl.thumbnail',
    'bootstrapform',
    'django_extensions',
    'django_fields',  # this needs to be defined before nynjaetc.main
    'nynjaetc.main',
    'pagetree',
    'pageblocks',
    'quizblock',
    'registration',
    'nynjaetc.treatment_activity',
    'treebeard',
    'nynjaetc.analytics',
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

ACCOUNT_ACTIVATION_DAYS = 7

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

ENCRYPT_EMAIL_ADDRESSES = True
ENCRYPT_HRSA_IDS = True
ENCRYPT_KEY = 'DUMMY DUMMY DUMMY DUMMY.'  # overridden by local_settings.py

# nasty hard-coded ids and slugs
HRSA_ID_FIELD = 'question88'
PRETEST_PREF_SLUG = 'pre-test'
ENDURING_MATERIALS_SECTION_ID = 110
QUIZZES_TO_REPORT = [61, 46]
