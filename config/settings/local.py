from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'coupon_event',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': '127.0.0.1',  # Or an IP Address that your DB is hosted on
        'PORT': '13306'
    },
    "test": {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'coupon_event',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': '127.0.0.1',  # Or an IP Address that your DB is hosted on
        'PORT': '13306'
    }
}


DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'sql': {
            '()': 'django_sqlformatter.SqlFormatter',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'sql',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}
