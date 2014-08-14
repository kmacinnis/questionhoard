"""
Django settings for questionbank project.
This is meant to be called from `settings_local.py`, 
which has settings that vary for production and development.

"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b1pw-i7)8+zhxibkmaq=l-%0_g#oh&m5l6+9j4@kufh9hlizgs'


ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'south',
    'questions',
    'organization',
    'practicedocs',
    'exams',
    'zother',
    'simplified',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'questionbank.urls'

WSGI_APPLICATION = 'questionbank.wsgi.application'

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# DEBUG_TOOLBAR_CONFIG = {
#     'SHOW_TEMPLATE_CONTEXT': True,
# }
#
# # Necessary for Django-Debug-Toolbar:
# DEBUG_TOOLBAR_PATCH_SETTINGS = False
# INTERNAL_IPS = ['127.0.0.1', '::1', '72.179.33.203']
#