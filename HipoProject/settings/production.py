from .base import *
import django_heroku

DEBUG = False
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

ALLOWED_HOSTS = ['tim-zed-31581.herokuapp.com']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Activate Django-Heroku.
django_heroku.settings(locals())
