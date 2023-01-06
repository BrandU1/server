from datetime import timedelta

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    # For API Gateway Server
    "localhost",
    'api.brandu.shop',
    '127.0.0.1',
    '172.31.37.121'
]

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_variable('DATABASE_NAME'),
        'USER': get_env_variable('DATABASE_USER'),
        'PASSWORD': get_env_variable('DATABASE_PASSWORD'),
        'HOST': get_env_variable('DATABASE_HOST'),
        'PORT': '5432',
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,

    'AUTH_HEADER_TYPES': ('Bearer',),
}

# S3 Storage
MEDIAFILES_LOCATION = 'media'
STATICFILES_LOCATION = 'static'

# AWS Access
# AWS_S3_SECURE_URLS = True

# AWS_S3_SIGNATURE_VERSION = 's3v4'
# AWS_S3_ADDRESSING_STYLE = 'virtual'

AWS_S3_ACCESS_KEY_ID = get_env_variable('AMAZON_S3_ACCESS_KEY')
AWS_S3_SECRET_ACCESS_KEY = get_env_variable('AMAZON_S3_SECRET')
AWS_S3_REGION_NAME = 'ap-northeast-2'
AWS_STORAGE_BUCKET_NAME = get_env_variable('AMAZON_S3_BUCKET')
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_S3_SECURE_URLS = False
AWS_QUERYSTRING_AUTH = False
# AWS_DEFAULT_ACL = 'public-read'

# BASE_BACKEND_URL = 'https://api.brandu.shop'
DEFAULT_FILE_STORAGE = 'server.storages.MediaStorage'
STATICFILES_STORAGE = 'server.storages.StaticStorage'

sentry_sdk.init(
    dsn=get_env_variable('SENTRY_DSN'),
    integrations=[
        DjangoIntegration(),
    ],
    traces_sample_rate=1.0,
    send_default_pii=True
)

CORS_ALLOW_CREDENTIALS = True

# SECURE_SSL_REDIRECT = True

CORS_ORIGIN_WHITELIST = [
    # For Development Server
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://192.168.0.10:3000',

    # For Frontend Server
    'https://www.brandu.shop',
    'https://brandu.shop',
    'https://release.d2b6y657jebxiq.amplifyapp.com',

    # For Staging Server
    'https://staging.brandu.shop',
    'https://staging.d2b6y657jebxiq.amplifyapp.com',

    # For Mobile Server
    'https://m.brandu.shop',
]

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse',
#         },
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         },
#     },
#     'formatters': {
#         'django.server': {
#             '()': 'django.utils.log.ServerFormatter',
#             'format': '[{server_time}] {message}',
#             'style': '{',
#         },
#         'standard': {
#             'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#         },
#         'django.server': {
#             'level': 'INFO',
#             'class': 'logging.StreamHandler',
#             'formatter': 'django.server',
#         },
#         'mail_admins': {
#             'level': 'ERROR',
#             'filters': ['require_debug_false'],
#             'class': 'django.utils.log.AdminEmailHandler'
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console', 'mail_admins'],
#             'level': 'INFO',
#         },
#         'django.server': {
#             'handlers': ['django.server'],
#             'level': 'INFO',
#             'propagate': False,
#         },
#         "django.db.backends": {
#             "handlers": ["console"],
#             "level": "DEBUG",
#         },
#     }
# }
