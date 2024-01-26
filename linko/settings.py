from pathlib import Path
import os
from decouple import config
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

LOCAL_APPS = [
    'accounts.apps.AccountsConfig',
    'links.apps.LinksConfig',
    'shop.apps.ShopConfig',
    'payment.apps.PaymentConfig',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    'djoser',
    'corsheaders',
    'drf_yasg',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS += LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # coreheaders
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'linko.urls'

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

WSGI_APPLICATION = 'linko.wsgi.application'

AUTH_USER_MODEL = 'accounts.User'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('MYSQL_CONNECTION_NAME'),
        'USER': config('MYSQL_USER'),
        'PASSWORD': config('MYSQL_PASSWORD'),
        'HOST': '172.17.0.1',
        'PORT': 3307,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
    }
}

# Password validation

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated'  # change needed
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],

    'DEFAULT_THROTTLE_RATES': {
        'anon': '50/min',
        'user': '80/min'
    },
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=2),  # testing
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),

    'AUTH_HEADER_TYPES': ('Bearer',),
    'BLACKLIST_AFTER_ROTATION': True,
    'ROTATE_REFRESH_TOKENS': True,

}

DJOSER = {
    # set new password
    'USER_CREATE_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_RETYPE': True,

    # set new username
    'USERNAME_RESET_CONFIRM_URL': 'username/reset/confirm/{uid}/{token}',

    'LOGIN_FIELD': 'email',
    'HIDE_USERS': True,

    'SERIALIZERS': {
        'user_create': 'accounts.serializers.UserCreate',
        'current_user': 'accounts.serializers.CurrentUser',
    },
}

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "PATCH",
    "POST",
    "PUT",
]


SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'JWT',
            'name': 'Authorization',
            'in': 'header',
        },
    },
    'USE_SESSION_AUTH': False,
    'PERSIST_AUTH': True,
}


if DEBUG is False:
    ALLOWED_HOSTS = []
    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
        'REFRESH_TOKEN_LIFETIME': timedelta(hours=1),

        'AUTH_HEADER_TYPES': ('Bearer',),
        'BLACKLIST_AFTER_ROTATION': True,
        'ROTATE_REFRESH_TOKENS': True,
    }

    DJOSER = {
        # set new password
        'USER_CREATE_PASSWORD_RETYPE': True,
        'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
        'PASSWORD_RESET_CONFIRM_RETYPE': True,

        # set new username
        'USERNAME_RESET_CONFIRM_URL': 'username/reset/confirm/{uid}/{token}',

        # activate account via email
        'ACTIVATION_URL': 'activate/{uid}/{token}',
        'SEND_ACTIVATION_EMAIL': True,
        'SEND_CONFIRMATION_EMAIL': True,

        'LOGIN_FIELD': 'email',
        'HIDE_USERS': True,

        'SERIALIZERS': {
            'user_create': 'accounts.serializers.UserCreate',
            'current_user': 'accounts.serializers.CurrentUser',
        },
    }

    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    CORS_ALLOW_ALL_ORIGINS = False