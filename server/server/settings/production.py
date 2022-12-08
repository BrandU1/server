from datetime import timedelta

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    # For API Gateway Server
    'https://2zixy7e73k.execute-api.ap-northeast-2.amazonaws.com',
    'api.brandu.shop',
    '127.0.0.1',
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
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,

    'AUTH_HEADER_TYPES': ('Bearer',),
}

# S3 Storage
MEDIAFILES_LOCATION = 'media'
STATICFILES_LOCATION = 'static'

# AWS Access
AWS_S3_SECURE_URLS = True
AWS_S3_REGION_NAME = 'ap-northeast-2'
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_ADDRESSING_STYLE = 'virtual'

AWS_S3_ACCESS_KEY_ID = get_env_variable('AMAZON_S3_ACCESS_KEY')
AWS_S3_SECRET_ACCESS_KEY = get_env_variable('AMAZON_S3_SECRET')
AWS_STORAGE_BUCKET_NAME = get_env_variable('AMAZON_S3_BUCKET')

BASE_BACKEND_URL = 'https://api.brandu.shop'
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

SECURE_SSL_REDIRECT = True

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
