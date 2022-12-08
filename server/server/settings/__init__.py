import os

SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE')

if not SETTINGS_MODULE or SETTINGS_MODULE == 'server.settings':
    from .local import *

elif SETTINGS_MODULE == 'server.settings.production':
    from .production import *
