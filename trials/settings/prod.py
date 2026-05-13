import os
from .base import BASE_DIR

# SECURITY: SECRET_KEY must be set via environment variable, no fallback
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY: Never run debug in production
DEBUG = False

# SECURITY: ALLOWED_HOSTS from environment (comma-separated)
ALLOWED_HOSTS = [
    h.strip() for h in os.environ.get('ALLOWED_HOSTS', '').split(',') if h.strip()
]
# Internal hostname used by patents-web for the rename webhook.
# Django rejects HTTP_HOST values violating RFC 1034/1035 (e.g. the docker
# service name "trials_service" with an underscore) before consulting
# ALLOWED_HOSTS, so the Patents service overrides Host: with this label.
# It is not routable from outside the patents_shared docker network.
for internal_host in ('trials_service', 'trials.local'):
    if internal_host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(internal_host)

# Database — all credentials from environment, no fallbacks
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ['SQL_DATABASE'],
        'USER': os.environ['SQL_USER'],
        'PASSWORD': os.environ['SQL_PASSWORD'],
        'HOST': os.environ['SQL_HOST'],
        'PORT': os.environ.get('SQL_PORT', '5432'),
    }
}

# SECURITY: Password validators enabled in production
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# SECURITY: Explicit CORS origins, not allow-all
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    o.strip() for o in os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',') if o.strip()
]

# Logging — less verbose in production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}
