from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
# Don't add anything as DEBUG_MODE in production
DEBUG = True

ALLOWED_HOSTS = '*'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CORS_ORIGIN_WHITELIST = (
    'http://localhost:4200',
    'https://localhost:4200',
    'https://192.168.0.19:4200',
)



