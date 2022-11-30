"""
Django settings for server project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

load_dotenv()


def get_env_variable(var_name):
    """ 환경 변수를 가져오거나 예외를 반환하는 함수 """
    try:
        return os.environ[var_name]
    except KeyError:
        error_message = f"Set the {var_name} environment variable"
        raise ImproperlyConfigured(error_message)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = eval(os.environ.get('DEBUG', 'True'))

ALLOWED_HOSTS = [
    'api.brandu.shop', 'themealways.com', '3.34.97.255', '127.0.0.1', 'localhost', '192.168.0.2'
]

# Application definition

INSTALLED_APPS = [
    # Django Default Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Django Third party Apps
    'storages',
    'drf_yasg',
    'rest_framework',
    'corsheaders',
    'django_extensions',
    'debug_toolbar',

    # Django Custom Apps
    'accounts.apps.AccountsConfig',
    'auths.apps.AuthsConfig',
    'products.apps.ProductsConfig',
    'search.apps.SearchConfig',
    'orders.apps.OrdersConfig',
    'events.apps.EventsConfig',
    'services.apps.ServicesConfig',
    'communities.apps.CommunitiesConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'server.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_variable('DATABASE_NAME' if not DEBUG else 'DEV_DATABASE_NAME'),
        'USER': get_env_variable('DATABASE_USER' if not DEBUG else 'DEV_DATABASE_USER'),
        'PASSWORD': get_env_variable('DATABASE_PASSWORD' if not DEBUG else 'DEV_DATABASE_PASSWORD'),
        'HOST': get_env_variable('DATABASE_HOST' if not DEBUG else 'DEV_DATABASE_HOST'),
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = 'accounts.User'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "core.exceptions.handler.custom_exception_handler",
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
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

# CORS_ORIGIN_WHITELIST = [
#     'http://127.0.0.1:8000'
#     'http://localhost:3000',
#     'https://brandu.shop',
# ]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

# SECURE_SSL_REDIRECT = True

# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

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

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}

if DEBUG:
    BASE_BACKEND_URL = 'http://localhost:8000'
    import socket

    # static files
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    # DEBUG TOOLBAR
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + '1' for ip in ips] + ['127.0.0.1', '10.0.2.2']

else:
    BASE_BACKEND_URL = 'https://api.brandu.shop'
    DEFAULT_FILE_STORAGE = 'server.storages.MediaStorage'
    STATICFILES_STORAGE = 'server.storages.StaticStorage'
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=get_env_variable('SENTRY_DSN'),
        integrations=[
            DjangoIntegration(),
        ],
        traces_sample_rate=1.0,
        send_default_pii=True
    )
