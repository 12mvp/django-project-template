import os
import sys
import logging.config

from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATES[0]['OPTIONS'].update({'debug': True})


# Turn off debug while imported by Celery with a workaround
# See http://stackoverflow.com/a/4806384

if "celery" in sys.argv[0]:
    DEBUG = False


# Django Debug apps
INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
]
   

# Additional middleware introduced by debug toolbar
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']


# Show emails to console in DEBUG mode
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Allow internal IPs for debugging
INTERNAL_IPS = [
    '127.0.0.1',
    '0.0.0.1',
]


# Log everything to the logs directory at the top
LOGFILE_ROOT = os.path.join(dirname(BASE_DIR), 'logs')

if not os.path.isdir(LOGFILE_ROOT):
    os.makedirs(LOGFILE_ROOT)


# Reset logging

LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'django_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGFILE_ROOT, 'django.log'),
            'formatter': 'verbose'
        },
        'proj_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGFILE_ROOT, 'project.log'),
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['django_log_file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'project': {
            'handlers': ['proj_log_file'],
            'level': 'DEBUG',
        },
    }
}

logging.config.dictConfig(LOGGING)

# HINT: logger = logging.getLogger("project")
