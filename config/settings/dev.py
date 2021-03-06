"""
Configuration for development. Take care of env.json in project root folder.
"""
import json
from os import environ, path
from django.core.exceptions import ImproperlyConfigured, MiddlewareNotUsed
from celery.schedules import crontab
from .base import *


CURRENT_ENVIRONMENT = 'dev'
STAGING_ENV_KEY = 'STAGING_ENV'
IS_STAGING = False


ENV_FILE = path.join(path.dirname(BASE_DIR), 'local_env.json')
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

# TWILIO CONFIGURATION
TWILIO_NUMBER = ENV_JSON.get('TWILIO_NUMBER')
TWILIO_ACCOUNT_SID = ENV_JSON.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = ENV_JSON.get('TWILIO_AUTH_TOKEN')

if not TWILIO_AUTH_TOKEN or not TWILIO_ACCOUNT_SID or not TWILIO_NUMBER:
    raise MiddlewareNotUsed("Missing TWILIO configuration")

# if not EMAIL_HOST or not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD or\
#         not EMAIL_PORT or not EMAIL_USE_TLS:
#     raise ImproperlyConfigured("SMTP Configuration Error!")

# GOOGLE_MAP_API_KEY = ENV_JSON.get('GOOGLE_MAP_API_KEY')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# AWS CONFIGURATION
AWS_ACCESS_KEY_ID = ENV_JSON.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = ENV_JSON.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = ENV_JSON.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
AWS_DEFAULT_ACL = None
AWS_S3_ENCRYPTION = True
AWS_S3_FILE_OVERWRITE = True
AWS_S3_SECURE_URLS = False


if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY or\
        not AWS_STORAGE_BUCKET_NAME:
    raise ImproperlyConfigured('AWS SETTINGS are missing.')

# STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
# ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

ADMINS = ENV_JSON.get('ADMINS', [])
ALLOWED_HOSTS = ENV_JSON.get('ALLOWED_HOSTS', ALLOWED_HOSTS)
DEBUG = ENV_JSON.get('DEBUG', False)

if not DEBUG:
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": ['redis://127.0.0.1:6379/0'],
        },
    },
}

EVENT_QUERY_INTERVAL = ENV_JSON.get('EVENT_QUERY_INTERVAL', 10)
SOCKET_SERVER_HOST = ENV_JSON.get('SOCKET_SERVER_HOST', 'ws://localhost')

# Celery configuration
CELERY_BROKER_URL = ENV_JSON.get(
    'CELERY_BROKER_URL', 'redis://localhost:6379/1')
CELERY_TIMEZONE = TIME_ZONE
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULE = {
    'check-valid-events-every-5-minutes': {
       'task': 'cafe_backend.apps.events.tasks.check_valid_events',
       'schedule': EVENT_QUERY_INTERVAL * 60,
    },
    'check-invalid-music-every-day': {
        'task': 'cafe_backend.mgnt.music.tasks.check_invalid_musics',
        'schedule': crontab(hour=11, minute=56),
    },
}

# SPOTIFY CONFIGURATION
SPOTIPY_CLIENT_ID = '5676b70e517b4887be7bcbbc5f5fa728'
SPOTIPY_CLIENT_SECRET = '11252984015d49c48453669848637a17'
SPOTIPY_REDIRECT_URI = 'http://localhost:8000/?code=123'
SPOTIFY_USERNAME = '9e3nuf6l66sxqvhtvagnzxzym'
SPOTIFY_PASSWORD = 'blue dragon'
SPOTIFY_PLAYLIST_NAME = 'cafe_backend_dev'
SPOTIFY_PLAYLIST_ID = '5NNq0AArn0y4wuFeWCNzE8'

HOSTNAME = ENV_JSON.get('HOSTNAME', 'http://cafe.smartdjango.com')
# PRINTER CONFIGURATION
EYPRINT_58_API_KEY = ENV_JSON.get(
    'EYPRINT_58_API_KEY', '326d59ad741cb7ddf278f55f08a75170')
EYPRINT_80_API_KEY = ENV_JSON.get(
    'EYPRINT_80_API_KEY', '9a93eee5c427897be3df77afd3a4203a')
