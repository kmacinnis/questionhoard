"""
Settings for deployment.
"""

from settings_base import *

# SECURITY SETTINGS
DEBUG = False
TEMPLATE_DEBUG = False
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dragon_db',
        'USER': 'dragon_user',
        'PASSWORD': 'boop77',
        'HOST': 'localhost',
        'PORT': '',                      # Set to empty string for default.
    }
}

STATIC_ROOT = '/webapps/dragon/static/'
