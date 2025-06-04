DEBUG = True

import logging

# Redis 로깅 활성화
logging.basicConfig(level=logging.DEBUG)
# 또는 Django 설정에 로깅 추가
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'redis': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'coupon_event',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': '127.0.0.1',  # Or an IP Address that your DB is hosted on
        'PORT': '13306',
        # Pool settings
        'CONN_MAX_AGE': 600,  # Django가 자동 유지하지 않도록
    }
}

from redis.backoff import ExponentialBackoff
from redis.retry import Retry

retry = Retry(
    ExponentialBackoff(), 10
)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",  # ✅ 이 설정이 되어 있어야 함
        "LOCATION": "redis://127.0.0.1:16379/1",  # 또는 unix socket 등
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
            # "REDIS_CLIENT_KWARGS": {
            #     "retry": retry,
            #     "retry_on_error": [
            #         Exception
            #     ],
            # }

            # "REDIS_CLIENT_KWARGS": {
            #     "retry": retry,
            #     "retry_on_timeout": 10
            # }
        }
    }
}

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'sql': {
#             '()': 'django_sqlformatter.SqlFormatter',
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'sql'
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         }
#     }
# }

SPECTACULAR_SETTINGS = {
    'TITLE': '',  # OpenAPI 3.0 페이지 타이틀,
    'DESCRIPTION': '',  # OpenAPI 3.0 페이지 설명,
    'VERSION': '1.0.0',  # 버전 정보
    'SERVE_INCLUDE_SCHEMA': False,
    'SORT_OPERATION_PARAMETERS': False,  # 이걸 추가하면 parameter를 class에 정의한 필드 순서대로 Swagger에 노출 시킬 수 있음
}

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
