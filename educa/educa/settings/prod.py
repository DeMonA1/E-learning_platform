from .base import *


DEBUG = False

ADMINS = [('Dzmitry', 'admin@email.com')]   # (name, email)

ALLOWED_HOSTS = ['*']   # all hosts

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3',
                         'NAME': BASE_DIR / 'db.sqlite3'}}
