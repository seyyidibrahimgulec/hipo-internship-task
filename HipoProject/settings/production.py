from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db9dctg6lq3211',
        'USER': 'ocveazvespixua',
        'PASSWORD': 'cade7ca45e05c4498d8ae7466f79d1919db0efe987c0541c34f68a8cf315144b',
        'HOST': 'ec2-174-129-29-101.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}
