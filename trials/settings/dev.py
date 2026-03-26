import os
from .base import BASE_DIR, REST_FRAMEWORK

SECRET_KEY = 'trials-dev-secret-key-not-for-production'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('SQL_DATABASE', 'trials_db'),
        'USER': os.environ.get('SQL_USER', 'admin'),
        'PASSWORD': os.environ.get('SQL_PASSWORD', 'password'),
        'HOST': os.environ.get('SQL_HOST', 'trials-db'),
        'PORT': os.environ.get('SQL_PORT', '5432'),
    }
}

# Dev: allow all origins
CORS_ALLOW_ALL_ORIGINS = True

# Dev: allow any permissions for easier development
REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = [
    'rest_framework.permissions.AllowAny',
]
