import os

SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE')

if not SETTINGS_MODULE or SETTINGS_MODULE == 'server.settings.local':
    from .local import *

elif SETTINGS_MODULE == 'server.settings.staging':
    from .staging import *

elif SETTINGS_MODULE == 'server.settings.production':
    from .production import *
