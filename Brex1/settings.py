
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv() # Carga las variables de entorno desde el archivo .env


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ehqzsrgi1(=!_wb_sji7$)llfa4v8ejpw$ww)pk47&jq%i&)cl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Clients.apps.ClientsConfig', # Agrega tu app de clientes
    'webhooks.apps.WebhooksConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # se agrega al middleware para servir archivos estáticos en producción
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Brex1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Brex1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

# DATABASES = {
#    'default': {
#       'ENGINE': 'django.db.backends.sqlite3', # Default sqllite  
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / "staticfiles"  # Folder where collectstatic will store files
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"



# db_live = os.getenv("DB_LIVE")


DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.postgresql', # Default PostgreSQL
        'NAME':   os.getenv('DB_NAME'),
        'USER':   os.getenv('DB_USER'),
        'PASSWORD':   os.getenv('DB_PASSWORD'),
        'HOST':   os.getenv('DB_HOST'),
        'PORT':   os.getenv('DB_PORT'),

    }
}   
 
# settings.py

# El "Backend" es el motor que envía el correo
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Configuración del servidor de salida
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True  # Para seguridad

# Tus credenciales
EMAIL_HOST_USER = 'andres@jobbi.me' #Correo mio
EMAIL_HOST_PASSWORD = 'gjlc ttjw duys ynkq' # ¡Ojo aquí!

# Quién aparece como remitente
DEFAULT_FROM_EMAIL = 'Sistema de Alertas <andres@jobbi.me>'