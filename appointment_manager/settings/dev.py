from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
# Don't add anything as DEBUG_MODE in production
DEBUG = True

ALLOWED_HOSTS = '*'

CORS_ORIGIN_WHITELIST = (
    'https://localhost:4200',
    'https://192.168.0.19:4200',
)

SECURE_SSL_REDIRECT = False



