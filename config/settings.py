
import os
from pathlib import Path
from dotenv import load_dotenv # <--- Importar
import dj_database_url # <--- Útil para Render
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Leer secretos desde variables de entorno
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# backend/config/settings.py

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.localhost', '.onrender.com'] # El punto permite subdominios


# 1. DEFINICIÓN DE APPS MULTI-TENANT
SHARED_APPS = (
    'django_tenants',  # OBLIGATORIO: Debe ser la primera
    'core',            # Nuestra app para gestionar las Unidades Transfusionales (Esquema public)
    'usuarios',
    'drf_spectacular',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    
    'rest_framework',
    'corsheaders',
)

TENANT_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    
    'usuarios',  
    'core',        # Usuarios y Roles independientes por hospital
    # Aquí iremos agregando: pacientes, hemocomponentes, transfusiones, etc.
)
# Configuración para Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema', # <--- Activa Spectacular
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# Configuración específica de Swagger/OpenAPI
SPECTACULAR_SETTINGS = {
    'TITLE': 'API Unidad Transfusional (SGT)',
    'DESCRIPTION': 'Sistema de Gestión Transfusional con arquitectura Multi-tenant.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_PATCH': True,
    'COMPONENT_SPLIT_REQUEST': True,
    'SECURITY': [{'jwt': []}], # <--- Habilita el botón de candado para JWT
    'APPEND_COMPONENTS': {
        'securitySchemes': {
            'jwt': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
            }
        }
    },
}
# Django unirá ambas listas para su uso interno
INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]


# 2. CONFIGURACIÓN DE MIDDLEWARE (Orden crítico)
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',         # 1. CORS primero
    'django_tenants.middleware.main.TenantMainMiddleware', # Enruta al esquema correcto basado en el dominio
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'
PUBLIC_SCHEMA_URLCONF = 'config.urls' # URLs específicas para cuando estés en localhost

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

WSGI_APPLICATION = 'config.wsgi.application'


# 3. CONFIGURACIÓN DE BASE DE DATOS (PostgreSQL con Esquemas)
if os.getenv('DATABASE_URL'):
    # Si estamos en Render, usamos la URL que ellos nos dan
    DATABASES = {
        'default': dj_database_url.config(engine='django_tenants.postgresql_backend')
    }
else:
    # Si estamos en local, usamos los datos del .env
    DATABASES = {
        'default': {
            'ENGINE': 'django_tenants.postgresql_backend',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASS'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
        }
    }

# 4. CONFIGURACIÓN DEL ENRUTADOR DE TENANTS
DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

TENANT_MODEL = "core.UnidadTransfusional" 
TENANT_DOMAIN_MODEL = "core.Dominio"


# Validaciones de contraseñas (por defecto de Django)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internacionalización
LANGUAGE_CODE = 'es-bo'
TIME_ZONE = 'America/La_Paz'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Permitir peticiones desde React
CORS_ALLOW_ALL_ORIGINS = True

AUTH_USER_MODEL = 'usuarios.Usuario'