"""
Django settings for LotoFinder project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-9mmysi9%og*e=ro3$x27%4)d(fdp!k6%n93jwqrbq0vi-3c!^8')
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = bool( os.environ.get('DJANGO_DEBUG', True) )

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.18.244']


# Application definition

INSTALLED_APPS = [    
    'apps.Administracion',
    'apps.Cliente',
    'apps.Global',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'paypalcheckoutsdk',
    'cookie_consent',
    'ckeditor',
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

ROOT_URLCONF = 'LotoFinder.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'apps/templates'),
            'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

#cookies consent#
COOKIE_CONSENT_POPUP = {
    'message': 'Este sitio web utiliza cookies para ofrecerte la mejor experiencia de usuario. Al continuar navegando, aceptas nuestro uso de cookies.',
    'button_text': 'Aceptar',
}

WSGI_APPLICATION = 'LotoFinder.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db',
        'USER': 'django',
        'PASSWORD': 'django12321$',
        'HOST': 'localhost',
        'PORT': '3306',
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

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'Global.Usuario'

#recuperar contraseñas
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'sgarcia263@alu.ucam.edu'
EMAIL_HOST_PASSWORD = 'Srsam12321$'
PASSWORD_RESET_EMAIL_TEMPLATE = 'registration/password_reset_email.html'

#manejo de archivos no estaticos
MEDIA_URL = '/imagenes/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuración de sesiones
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Almacena las sesiones en la base de datos
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # La sesión permanece activa incluso después de cerrar el navegador
SESSION_COOKIE_AGE = 3600 * 12  

CART_SESSION_ID = 'cart'