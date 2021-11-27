import dotenv
import os
import dj_database_url


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# load environment variables from .env
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'djas139das$%@#*()dasd132173nsads1sbdascl')

# Application definition
INSTALLED_APPS = [
    'scheduling.apps.SchedulingConfig',
    'customers.apps.CustomersConfig',
    'core.apps.CoreConfig',
    'app_auth.apps.AuthConfig',
    'billing.apps.BillingConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'rest_framework',
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',

    'corsheaders',

    # cloudinary image uploader
    'cloudinary',
    'simple_history',
    'safedelete',
]
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
        # Any other renders
    ),
    'DEFAULT_PARSER_CLASSES': (
        # If you use MultiPartFormParser or FormParser, we also have a camel case version
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        # Any other parsers
    ),
    'EXCEPTION_HANDLER': 'kalendario.common.handlers.custom_exception_handler'

}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # below adds middleware for cors
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',  # Used for appointment history
]

ROOT_URLCONF = 'kalendario.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'kalendario.wsgi.application'

DATABASES = {'default': dj_database_url.config(conn_max_age=600)}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGIN_REDIRECT_URL = '/'

SITE_ID = 1

AUTH_USER_MODEL = 'core.User'

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'app_auth.serializers.CustomRegisterSerializer',
}

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'app_auth.serializers.UserSerializer',
}
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'kalendario-auth'

OLD_PASSWORD_FIELD_ENABLED = True

ACCOUNT_ADAPTER = 'app_auth.adapters.AccountAdapter'

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_AUTHENTICATION_METHOD = 'email'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_EMAIL_FIELD = 'email'

DEFAULT_FROM_EMAIL = 'no-reply@kalendario.ie'

# Social authentication
AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_TMP = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

os.makedirs(STATIC_TMP, exist_ok=True)
os.makedirs(STATIC_ROOT, exist_ok=True)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STRIPE_API_KEY = os.environ.get('STRIPE_SECRET_KEY', '')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY', '')
STRIPE_API_VERSION = os.environ.get('STRIPE_API_VERSION', '2019-12-03')
STRIPE_SUBSCRIPTION_PRICE_ID = os.environ.get('STRIPE_SUBSCRIPTION_PRICE_ID', '')

ACCOUNT_WEBHOOK_SECRET = os.environ.get('ACCOUNT_WEBHOOK_SECRET', '')
CONNECTED_ACCOUNT_WEBHOOK_SECRET = os.environ.get('CONNECTED_ACCOUNT_WEBHOOK_SECRET', '')

CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
CELERY_TIMEZONE = os.environ.get('CELERY_TIMEZONE', 'Europe/London')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://localhost:6379')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_BEAT_SCHEDULE = {
    'delete-idle-every-2-minute': {
        'task': 'scheduling.tasks.delete_idle_requests',
        'schedule': 120.0
    },
}

SPA_BASE_URL = os.environ.get('SPA_URL', '')
