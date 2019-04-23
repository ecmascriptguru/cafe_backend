"""
Configuration for development. Take care of env.json in project root folder.
"""
import json
from os import environ, path
from django.core.exceptions import ImproperlyConfigured
from .base import *


ON_STAGING_SERVER = 'STAGING_SERVER'
ON_PRODUCTION_SERVER = 'PRODUCTION_SERVER'
CURRENT_ENVIRONMENT = 'dev'
STAGING_ENV_KEY = 'STAGING_ENV'
IS_STAGING = False


if ON_STAGING_SERVER in environ:
    IS_STAGING = True

if ON_PRODUCTION_SERVER in environ:
    raise ImproperlyConfigured("You can't use dev configuration on production\
        environment.")

if IS_STAGING:
    ENV_JSON = json.loads(environ.get(STAGING_ENV_KEY, None))
else:
    ENV_FILE = path.join(BASE_DIR, 'local_env.json')
    if not path.exists(ENV_FILE):
        raise ImproperlyConfigured("No local environment file was found in\
            directory: {0}".format(BASE_DIR))
    with open(ENV_FILE) as data_file:
        ENV_JSON = json.load(data_file)

if not ENV_JSON:
    raise ImproperlyConfigured("No environment variables were found")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV_JSON.get('DJANGO_SECRET_KEY', None)

if IS_STAGING:
    DATABASES = {}
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=500, engine='django.db.backends.postgresql')
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': ENV_JSON.get('DATABASE_NAME'),
            'USER': ENV_JSON.get('DATABASE_USER'),
            'PASSWORD': ENV_JSON.get('DATABASE_PW'),
            'HOST': ENV_JSON.get('DATABASE_HOST'),
            'PORT': '5432',
        }
    }


# SMTP CONFIGURATION
# EMAIL_USE_TLS = ENV_JSON.get('EMAIL_USE_TLS')
# EMAIL_HOST = ENV_JSON.get('EMAIL_HOST')
# EMAIL_HOST_USER = ENV_JSON.get('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = ENV_JSON.get('EMAIL_HOST_PASSWORD')
# EMAIL_PORT = ENV_JSON.get('EMAIL_PORT')

# if not EMAIL_HOST or not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD or\
#         not EMAIL_PORT or not EMAIL_USE_TLS:
#     raise ImproperlyConfigured("SMTP Configuration Error!")

# GOOGLE_MAP_API_KEY = ENV_JSON.get('GOOGLE_MAP_API_KEY')


