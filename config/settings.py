"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-+dj7lm2lol$zxg6t0$og3@(+g2=9j3$)cy1&+f85g$f@o0^89t"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",
    "users",
    "courses",
    "student_requests",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_yasg",
]

MIDDLEWARE = [
<<<<<<< HEAD
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
=======
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
>>>>>>> 10683f4de1e691ed278dcd59f535895643f08f10
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'your_db_name',
#         'USER': 'your_db_user',
#         'PASSWORD': 'your_db_password',
#         'HOST': 'localhost',  # Set to the address of your PostgreSQL server
#         'PORT': '5432',       # Default PostgreSQL port
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "users.User"

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

<<<<<<< HEAD
LANGUAGE_CODE = "en-us"
# LANGUAGE_CODE = 'fa'
=======
LANGUAGE_CODE = 'en-us'
>>>>>>> 10683f4de1e691ed278dcd59f535895643f08f10

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

<<<<<<< HEAD
# LOCALE_PATHES = [
#     os.path.join(BASE_DIR,  'locale')
# ]
=======
>>>>>>> 10683f4de1e691ed278dcd59f535895643f08f10
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(
    BASE_DIR, "files"
)  # This defines the absolute path for uploads
MEDIA_URL = "/media/"

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        #     # 'rest_framework.authentication.SessionAuthentication',
        "rest_framework.authentication.TokenAuthentication",
    ),
    # 'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    # 'DEFAULT_VERSION': 'v1',
    # 'ALLOWED_VERSIONS': ['v1'],
}

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

# MinIO Configuration
MINIO_ENDPOINT = "your-minio-endpoint"
MINIO_ACCESS_KEY = "your-access-key"
MINIO_SECRET_KEY = "your-secret-key"
MINIO_SECURE = False  # Set to True if using HTTPS
<<<<<<< HEAD
MINIO_BUCKET_NAME = "your-bucket-name"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "dev.fahima@gmail.com"  # Your Gmail address
EMAIL_HOST_PASSWORD = "qxbd cuur bjpy ueeq"
=======
MINIO_BUCKET_NAME = 'your-bucket-name'
>>>>>>> 10683f4de1e691ed278dcd59f535895643f08f10
