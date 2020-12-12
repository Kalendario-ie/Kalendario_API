from .base import *
import django_heroku

DEBUG = os.environ.get('DEBUG_MODE', False)

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(';')

white_list = os.getenv('DJANGO_CORS_ORIGIN_WHITELIST')
CORS_ORIGIN_WHITELIST = tuple(white_list.split(';')) if white_list is not None else ()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

EMAIL_BACKEND = 'django_mailgun.MailgunBackend'

# Activate Django-Heroku.
django_heroku.settings(locals(), logging=False)
del DATABASES['default']['OPTIONS']['sslmode']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

SESSION_COOKIE_DOMAIN = '.kalendario.ie'
