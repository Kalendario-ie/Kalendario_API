from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
# Don't add anything as DEBUG_MODE in production
DEBUG = True

ENVIRONMENT = 'DEV'

ALLOWED_HOSTS = '*'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'http://localhost:4200',
    'https://localhost:4200',
    'https://192.168.0.19:4200',
)

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
            'propagate': True,
        },
        'scheduling.views': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
