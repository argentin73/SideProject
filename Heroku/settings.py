"""
Django settings for Heroku project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path
from telnetlib import SE
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / 'frontend'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-b=m-28=4oxgrer)p6b^gza&l@v41=%2nkr6pjdlu=c95!_q(r4'
# SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '*',
]

CORS_ORIGIN_WHITELIST = '139.59.135.130'
CORS_ALLOW_CREDENTIALS = True

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

SECURE_CROSS_ORIGIN_OPENER_POLICY='same-origin-allow-popups'

# STRIPE
STRIPE_API_KEY = 'sk_test_51L8i6WCxR8aIBa9PqrdHDGHaF3uwfz7ccj4CuqJZk5En5Ulq320RUYNydQ7DISneNXzWiWAmH8vi1P5J9JELlyr500boD6sw42';
STRIPE_WEBHOOK_SECRET_KEY = 'whsec_9f4f80b711b7847901af6baff11dbd5b3261eb50ab7ff21f13a1bef83fc108b9';
# PAYPAL
PAYPAL_CLIENT_ID = 'Aa25Ii8Z4pmWK7Oh0WAU7VBP8inlB1C9Z_bRlPvMMUKT9CbMfHJRffumSDMtWdNrj05yZPgYMOChgm6w'
PAYPAL_APP_SECRET = 'EIHCxQ4pACan3ovM4ZtI9aTAGEGkj3kUWKHnfHcfsKhcoC6p3pjGpnLVBXm9BuOmBlJgE1DWf_gEQdl6'
PAYPAL_BASE_URL = 'https://api-m.sandbox.paypal.com'

# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    # MY APPS
    'rest_framework',
    'django_better_admin_arrayfield',
    'service'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Heroku.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [FRONTEND_DIR / 'build']
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

WSGI_APPLICATION = 'Heroku.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "demodb",
        "USER": "django",
        "PASSWORD": "djangopassword",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATICFILES_DIRS = (
    ( FRONTEND_DIR / 'build' / 'root' / 'static'),
    ( BASE_DIR / 'style' )
)

STATICFILES_STORAGE = (
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
)

STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = '/static/'

# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'frontend', 'build', 'static')]

WHITENOISE_ROOT = FRONTEND_DIR / 'build' / 'root'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
