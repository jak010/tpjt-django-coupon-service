from .base import *

DEBUG = True

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

LOGGING = {
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
            'formatter': 'sql'
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}

SPECTACULAR_SETTINGS = {
    'TITLE': '',  # OpenAPI 3.0 페이지 타이틀,
    'DESCRIPTION': '',  # OpenAPI 3.0 페이지 설명,
    'VERSION': '1.0.0',  # 버전 정보
}
