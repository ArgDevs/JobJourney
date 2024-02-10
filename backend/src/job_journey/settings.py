from datetime import timedelta
from pathlib import Path
from typing import Any

import environ
import kombu

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env: environ.Env = environ.Env()

print(f'BASE_DIR: {BASE_DIR}')
# reading .env file
environ.Env.read_env(BASE_DIR.joinpath('.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='django-insecure-$aj=p5@^265v964cgogn8l5ps#7&adx$zoua!8iwr2oaam0x3y')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

# This contains the external domain name that clients will use to access your site
ALLOWED_HOSTS: list[str] = env.list('ALLOWED_HOSTS', default=['*'])

# This tells Django to use the X-Forwarded-Host header value for constructing absolute URLs instead of the host header.
# If your Django application is being accessed through a series of reverse proxies, you'll need to ensure a few
# configurations to make sure your app is aware of the actual client's IP and other headers. This is important for
# various reasons like security, geolocation, and logging, to name a few.
USE_X_FORWARDED_HOST: bool = env.bool('USE_X_FORWARDED_HOST', default=False)
CSRF_TRUSTED_ORIGINS: list[str] = env.list('CSRF_TRUSTED_ORIGINS', default=['*'])

#  Tells Django to consider the connection as secure if it arrives with an X-Forwarded-Proto header with a value
#  of 'https' (this is often set by reverse proxies when they terminate SSL before forwarding the request).
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# This sets many intermediate reverse proxies do we trust.
XFF_TRUSTED_PROXY_DEPTH: int = env.int('XFF_TRUSTED_PROXY_DEPTH', default=2)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'django_extensions',
    'debug_toolbar',

    # Health checks: https://github.com/revsys/django-health-check
    'health_check',
    'health_check.db',
    'health_check.cache',
    'health_check.storage',
    'health_check.contrib.migrations',
    'health_check.contrib.celery',
    'health_check.contrib.celery_ping',
    'health_check.contrib.psutil',  # disk and memory utilization; requires psutil
    'health_check.contrib.rabbitmq',
    'health_check.contrib.redis',

]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # To serve static files for Admin
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'job_journey.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'job_journey.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME', default='job_journey_local'),
        'USER': env('DATABASE_USER', default='job_journey'),
        'PASSWORD': env('DATABASE_PASSWORD', default='password'),
        'TEST': {
            'NAME': env('POSTGRES_TEST_DATABASE_NAME',
                        default=f'test_{env("DATABASE_NAME", default='job_journey_local')}'),
        },
        'HOST': env('DATABASE_HOST', default='localhost'),
        'PORT': env('DATABASE_PORT', default=5432),
        'CONN_MAX_AGE': env.int('POSTGRES_CONN_MAX_AGE_SECONDS', default=0),
        'CONN_HEALTH_CHECKS': env.bool('POSTGRES_CONN_HEALTH_CHECKS', default=True)
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # Enable session to access the API docs.
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': env.int('PAGE_SIZE', default=50),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Celery Settings
CELERY_BROKER_URL = env.str('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND', default='rpc://')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_HIJACK_ROOT_LOGGER = False

# Celery queues: https://docs.celeryq.dev/en/3.1/configuration.html#celery-queues
CELERY_QUEUES: list[kombu.Queue] = [
    kombu.Queue(name='celery', exchange='celery', routing_key='celery'),
    kombu.Queue(name='trip_tracking', exchange='trip_tracking', routing_key='trip_tracking'),
    kombu.Queue(name='telemetry', exchange='telemetry', routing_key='telemetry'),
]

CELERY_DEFAULT_QUEUE = 'celery'
CELERY_DEFAULT_EXCHANGE = 'celery'
CELERY_DEFAULT_ROUTING_KEY = 'celery'

CELERY_BEAT_SCHEDULE = {}

# JWT Config
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=env.int('ACCESS_TOKEN_LIFETIME', default=300)),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=env.int('REFRESH_TOKEN_LIFETIME', default=1)),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'UPDATE_LAST_LOGIN': True,
    'ISSUER': 'job_journey_app',
    'TOKEN_OBTAIN_SERIALIZER': 'job_journey.token.CustomTokenSerializer',
}

GLOBAL_LOG_LEVEL = env.str('GLOBAL_LOG_LEVEL', default='INFO')
LOGGING: dict[str, Any] = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {},
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': GLOBAL_LOG_LEVEL
    },
    'loggers': {
        'asyncio': {
            'level': GLOBAL_LOG_LEVEL,
        },
        'pika': {
            'level': 'WARNING'
        },
        'factory': {
            'level': 'INFO',
            'propagate': True,
        },
        'faker': {
            'level': 'INFO',
            'propagate': True,
        },
        'factory.generate': {
            'level': 'INFO',
            'propagate': True,
        },
        'libevreactor': {
            'level': 'INFO',
            'propagate': True,
        },
    },
}

LOGIN_URL = '/admin/login/'
REDIS_URL: str = env.str('REDIS_URL', default='redis://127.0.0.1:6379')

# Add cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'db': env.int('REDIS_CACHE_DB', default=2)
        }
    }
}

# RabbitMQ configuration. Required by `django-health-check`.
BROKER_URL: str = CELERY_BROKER_URL

# Health checks: https://github.com/revsys/django-health-check
HEALTH_CHECK: dict[str, Any] = {
    'DISK_USAGE_MAX': env.int('HEALTHCHECK_DISK_USAGE_MAX', default=90),  # Percent
    'MEMORY_MIN': env.int('HEALTHCHECK_MEMORY_MIN', default=100),  # MB
}
HEALTHCHECK_CELERY_QUEUE_TIMEOUT: int = env.int('HEALTHCHECK_CELERY_QUEUE_TIMEOUT', default=3)  # Seconds
HEALTHCHECK_CELERY_RESULT_TIMEOUT: int = env.int('HEALTHCHECK_CELERY_RESULT_TIMEOUT', default=3)  # Seconds
HEALTHCHECK_ENDPOINT: str = env.str('HEALTHCHECK_ENDPOINT', default='api/JFUcbQpi86ww7SqsU/')
HEALTHCHECK_CELERY_BEAT_CACHE_KEY: str = env.str('HEALTHCHECK_CELERY_BEAT_CACHE_KEY', default='beathealth')

# Email server settings.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env.str('EMAIL_HOST', default='localhost')
EMAIL_PORT = env.int('EMAIL_PORT', default=1025)
EMAIL_USE_TLS = env.str('EMAIL_USE_TLS', default=False)
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', default='')

DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL', default='info@jobjourney.com')
DEFAULT_REPLY_TO_EMAIL = env.str('DEFAULT_REPLY_TO_EMAIL', default='no-reply@jobjourney.com')
