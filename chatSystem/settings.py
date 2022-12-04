"""
Django settings for chatSystem project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3&+(=hjoth5rxdyor$pwciqlj=4@km=ms_@-jxpzlfw-jm7r4k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '3.109.85.86',
    'teachatty.xyz', 'www.teachatty.xyz',
    '127.0.0.1',
]

# NB: Taking the name alias of the controllers
LOGOUT_REDIRECT_URL = 'auth/login'
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'auth/login'

# Application definition
INSTALLED_APPS = [
    'daphne',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accountApp',
    'coreApp',
    'roomApp',

    # Comment "django_extensions" before deployment
    # 'django_extensions',  # Generate Entity Relationship Diagram
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'chatSystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'chatSystem.wsgi.application'
ASGI_APPLICATION = 'chatSystem.asgi.application'

# Assign the Custom User Model Configuration
AUTH_USER_MODEL = "accountApp.User"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Channel-Redis Server Setup
"""
If in windows: Open the Ubuntu; execute the cmd to start redis-server first.
    sudo service redis-server start
    sudo service redis-server status
[Ref]: 
# https://linuxhandbook.com/system-has-not-been-booted-with-systemd/
# https://askubuntu.com/a/1379567

# Require to install 'channels-redis' pip-repo.
[Solution]: https://www.youtube.com/watch?v=eHALIS7awDc
"""
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                ("127.0.0.1", 6379),
                # ("172.17.0.3", 6379),
            ],
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
"""
[NB]: In localhost; use only "STATIC_ROOT" in spite of "STATICFILES_DIRS";
In production server; use only "STATICFILES_DIRS" in spite of "STATIC_ROOT";
STATICFILES_DIRS=>Aid to find all the static files across the project filesystem.
"""
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')   # Use in localhost-server instead of STATICFILES_DIRS; this dir will be created to store & server the static files while in the production

# Media Configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Configuration: Generate Graph Models (ERD)  --Comment before deployment; no required in deployment-server
# GRAPH_MODELS = {
#     'all_applications': True,
#     'group_models': True,
# }


# Email Configuration [SMTP] - Zoho Mailing Service
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.zoho.com'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'no-reply@teachatty.xyz'
# # EMAIL_HOST_PASSWORD = 'L6*2ox6qs6KY'    # Used while Two-Factor Auth is disabled;
# EMAIL_HOST_PASSWORD = 'nGbrdqPsWrVy'   # Application-specific Password; used when Two-Factor Auth is enabled;


DEFAULT_FROM_EMAIL = 'no-reply@teachatty.xyz'

# SERVER_MAIL = 'no-reply@teachatty.xyz'

# Example for using Zoho Mail as email sending backend
# EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
# EMAIL_USE_SSL = True
# EMAIL_PORT = 465
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_HOST_USER = 'no-reply@teachatty.xyz'
EMAIL_HOST_PASSWORD = 'nGbrdqPsWrVy'

