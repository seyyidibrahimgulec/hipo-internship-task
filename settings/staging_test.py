from .base import *

ALLOWED_HOSTS = ['*']

if 'TRAVIS' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'travis_ci_test',
            'USER': 'postgres',
            'PASSWORD': '',
            'PORT': '5432',
        }
    }
