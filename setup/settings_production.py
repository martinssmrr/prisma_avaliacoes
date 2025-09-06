"""
Configurações de produção para Django - VPS/Hostinger
"""
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# CONFIGURAÇÕES DE SEGURANÇA
# =============================================================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'prisma-avaliacoes-2024-super-secret-key-muito-forte-e-segura-xyz123'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'www.prismaavaliacoes.com.br',
    'prismaavaliacoes.com.br',
    '72.60.144.18',
    'localhost',
    '127.0.0.1'
]

# =============================================================================
# APPLICATION DEFINITION
# =============================================================================

INSTALLED_APPS = [
    "jazzmin",  # Interface de admin aprimorada
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",  # Framework para sitemap
    "django.contrib.sites",  # Necessário para sitemaps
    
    # Apps do projeto
    "Prisma_avaliacoes",
    "artigos",
    "controle",
    "area_cliente",  # Nova área do cliente
    "seo",  # App SEO completo
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "setup.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "seo.context_processors.seo_context",  # Context processor SEO
            ],
        },
    },
]

WSGI_APPLICATION = "setup.wsgi.application"

# =============================================================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# =============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/var/www/prisma_avaliacoes/db.sqlite3',
    }
}

# =============================================================================
# PASSWORD VALIDATION
# =============================================================================

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

# =============================================================================
# INTERNATIONALIZATION
# =============================================================================

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# =============================================================================
# STATIC FILES (CSS, JavaScript, Images)
# =============================================================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = '/var/www/prisma_avaliacoes/staticfiles'

# =============================================================================
# MEDIA FILES (User uploads)
# =============================================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/prisma_avaliacoes/media'

# =============================================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# =============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================================================
# CONFIGURAÇÕES DE SEO
# =============================================================================

# Site ID para sitemaps e framework django.contrib.sites
SITE_ID = 1

# =============================================================================
# CONFIGURAÇÕES DE SEGURANÇA PARA PRODUÇÃO
# =============================================================================

# HTTPS Settings
SECURE_SSL_REDIRECT = False  # Nginx já trata isso
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Session Security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# =============================================================================
# LOGGING
# =============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/www/prisma_avaliacoes/logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# =============================================================================
# JAZZMIN CONFIGURATION
# =============================================================================

JAZZMIN_SETTINGS = {
    "site_title": "Prisma Avaliações",
    "site_header": "Prisma Avaliações Imobiliárias",
    "site_brand": "Prisma Avaliações",
    "site_logo": None,
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "Bem-vindo ao Admin da Prisma Avaliações",
    "copyright": "Prisma Avaliações Imobiliárias",
    "search_model": ["auth.User", "artigos.Artigo"],
    "user_avatar": None,
    
    # Menu lateral
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Ver Site", "url": "/", "new_window": True},
    ],
    
    # Ordem dos apps no menu
    "order_with_respect_to": [
        "auth",
        "artigos", 
        "controle",
        "area_cliente",
        "seo",
        "Prisma_avaliacoes"
    ],
    
    # Ícones personalizados
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "artigos.Artigo": "fas fa-newspaper",
        "artigos.Categoria": "fas fa-tags",
        "controle.Cliente": "fas fa-user-tie",
        "controle.Contrato": "fas fa-file-contract",
        "controle.Laudo": "fas fa-file-alt",
        "area_cliente.PerfilCliente": "fas fa-user-circle",
        "seo.SEOMeta": "fas fa-search",
        "seo.SEOConfig": "fas fa-cogs",
    },
    
    # Tema
    "theme": "lumen",
    "dark_mode_theme": "darkly",
}
