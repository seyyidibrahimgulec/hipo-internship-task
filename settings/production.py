from .base import *
import django_heroku

DEBUG = False
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

ALLOWED_HOSTS = ['.herokuapp.com']

# Activate Django-Heroku.
django_heroku.settings(locals())
