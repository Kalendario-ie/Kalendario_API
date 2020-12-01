from .base import *
import django_heroku

DEBUG = False

# TODO: FIX THIS
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(';')

CORS_ORIGIN_WHITELIST = ()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

# Activate Django-Heroku.
django_heroku.settings(locals())
del DATABASES['default']['OPTIONS']['sslmode']
