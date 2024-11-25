from decouple import config
from .base import *


DEBUG = False

ADMINS = [('Dzmitry', 'admin@email.com')]   # (name, email)

ALLOWED_HOSTS = ['*']   # all hosts

DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql',
                         'NAME': config('POSTGRES_DB'),
                         'USER': config('POSTGRES_USER'),
                         'PASSWORD': config('POSTGRES_PASSWORD'),
                         'HOST': 'db',  # db service in compose file
                         'PORT': 5432}}

