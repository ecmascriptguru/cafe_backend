from connect.settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'docker',
        'USER': 'u1d8ipduumuel3',
        'PASSWORD': 'u1d8ipduumuel3',
        'HOST': 'db',
        'PORT': 5432,
    }
}

SECURE_SSL_REDIRECT = False

ALLOWED_HOSTS = ["*"]

DEBUG = True
