from .base import *

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'seyyidibrahimgulec',
        'USER': 'seyyidibrahimgulec',
        'PASSWORD': 'M(sqg69;"rSA;"y',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'TEST': {
            'NAME': 'mytestdatabase',
        },
    }
}
