# -*- coding: utf-8 -*-

from django.conf import settings

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s [%(module)s|%(lineno)s] - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'django_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': settings.LOGGING_FILE,
            'formatter': 'simple'
        },
    },

    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['django_log'],
            'propagate': False,
        },
        'labrador': {
            'level': 'DEBUG',
            'handlers': ['django_log'],
            'propagate': False,
        }
    },
}
