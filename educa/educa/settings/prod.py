from decouple import config
from .base import *


DEBUG = False

ADMINS = [('Dzmitry', 'admin@email.com')]   # (name, email)

ALLOWED_HOSTS = ['educaproject.com', 'www.educaproject.com']   # all hosts

DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql',
                         'NAME': config('POSTGRES_DB'),
                         'USER': config('POSTGRES_USER'),
                         'PASSWORD': config('POSTGRES_PASSWORD'),
                         'HOST': 'db',  # db service in yml file
                         'PORT': 5432}}

REDIS_URL = 'redis://cache:6379'    # cache service in yml file
CACHES['default']['LOCATION'] = REDIS_URL
CHANNEL_LAYERS['default']['CONFIG']['hosts'] = [REDIS_URL]

# security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True