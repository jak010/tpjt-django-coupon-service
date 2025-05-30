from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'coupon_event',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': '127.0.0.1',  # Or an IP Address that your DB is hosted on
        'PORT': '13306'
    }
}
