from django.conf import settings

env = getattr(settings, 'ENVIRONMENT', '')

if env == 'TEST':
    from .mock import *
else:
    from .production import *
