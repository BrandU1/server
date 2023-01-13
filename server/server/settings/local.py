from datetime import timedelta

from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    '*'
]

INSTALLED_APPS += [
    'drf_yasg',
    'django_extensions',
    'debug_toolbar',
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
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
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,

    'AUTH_HEADER_TYPES': ('Bearer',),
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

MEDIAFILES_LOCATION = 'media'
STATICFILES_LOCATION = 'static'

CORS_ORIGIN_ALLOW_ALL = True

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

SECURE_SSL_REDIRECT = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        },
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis-dev:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
