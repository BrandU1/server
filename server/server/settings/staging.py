from .local import *

DEBUG = True

ALLOWED_HOSTS = [
    '*'
]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,

    'AUTH_HEADER_TYPES': ('Bearer',),
}

BASE_BACKEND_URL = 'http://192.168.0.2'

STATIC_URL = f'{BASE_BACKEND_URL}/static/'
MEDIA_URL = f'{BASE_BACKEND_URL}/media/'
