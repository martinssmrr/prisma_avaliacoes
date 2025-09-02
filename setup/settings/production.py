"""
Configurações de Produção para HostGator
Django settings for Prisma Avaliações - Production Environment
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# =============================================================================
# CONFIGURAÇÕES DE SEGURANÇA
# =============================================================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-CHANGE-THIS-IN-PRODUCTION-xyz123abc456def789'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Hosts permitidos - Ajuste conforme seu domínio
ALLOWED_HOSTS = [
    'prismavaliacoes.com.br',
    'www.prismavaliacoes.com.br',
    'localhost',
    '127.0.0.1'
]

# =============================================================================
# APLICAÇÕES INSTALADAS
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
    "Prisma_avaliacoes",
    "artigos",
    "controle",
    "area_cliente",
]

# =============================================================================
# MIDDLEWARE
# =============================================================================

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

# =============================================================================
# CONFIGURAÇÕES DE TEMPLATES
# =============================================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "setup.wsgi.application"

# =============================================================================
# CONFIGURAÇÕES DE BANCO DE DADOS
# =============================================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# =============================================================================
# VALIDAÇÃO DE SENHAS
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
# INTERNACIONALIZAÇÃO
# =============================================================================

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# =============================================================================
# CONFIGURAÇÕES DE ARQUIVOS ESTÁTICOS
# =============================================================================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# =============================================================================
# CONFIGURAÇÕES DE ARQUIVOS DE MÍDIA
# =============================================================================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# =============================================================================
# CONFIGURAÇÕES DE SEGURANÇA HTTPS
# =============================================================================

# Forçar redirecionamento HTTPS
SECURE_SSL_REDIRECT = True

# Configurações de cookies seguros
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Configurações HSTS
SECURE_HSTS_SECONDS = 31536000  # 1 ano
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Outras configurações de segurança
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# =============================================================================
# CONFIGURAÇÕES DE EMAIL (para futuro)
# =============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.prismavaliacoes.com.br'  # Ajuste conforme HostGator
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'contato@prismavaliacoes.com.br'
EMAIL_HOST_PASSWORD = 'SUA_SENHA_EMAIL'  # Configure no cPanel
DEFAULT_FROM_EMAIL = 'contato@prismavaliacoes.com.br'

# =============================================================================
# CONFIGURAÇÕES DO DJANGO JAZZMIN
# =============================================================================

JAZZMIN_SETTINGS = {
    # Nome do site
    "site_title": "Prisma Avaliações",
    "site_header": "Prisma Avaliações Imobiliárias",
    "site_brand": "Prisma Avaliações",
    "site_logo": "img/logo.png",
    "login_logo": "img/logo.png",
    
    # Copyright
    "copyright": "Prisma Avaliações Imobiliárias",
    
    # Pesquisa no topo
    "search_model": ["controle.Cliente", "controle.Venda"],
    
    # Ícones do menu
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "controle.Cliente": "fas fa-user-friends",
        "controle.Venda": "fas fa-handshake",
        "artigos.Artigo": "fas fa-newspaper",
        "Prisma_avaliacoes": "fas fa-home",
    },
    
    # Menu personalizado
    "topmenu_links": [
        {"name": "Início", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Dashboard Vendas", "url": "admin:controle_dashboard", "permissions": ["controle.view_venda"]},
        {"name": "Ver Site", "url": "/", "new_window": True},
    ],
    
    # Ordem dos apps no menu
    "order_with_respect_to": ["controle", "artigos", "auth"],
    
    # Ocultar modelos
    "hide_models": ["auth.Group"],
    
    # Links relacionados
    "related_modal_active": True,
    
    # Customização da interface
    "custom_css": "css/admin_custom.css",
    "custom_js": None,
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    
    # Rodapé
    "show_ui_builder": False,
    
    # Tema
    "theme": "lumen",  # Tema claro com excelente contraste
    
    # Modo escuro
    "dark_mode_theme": "darkly",
    
    # Sidebar personalizada
    "custom_links": {
        "controle": [{
            "name": "Dashboard Vendas",
            "url": "admin:controle_dashboard",
            "icon": "fas fa-chart-line",
        }]
    }
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-light",
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-light-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "lumen",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": False,
}

# =============================================================================
# CONFIGURAÇÕES DE LOGGING
# =============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django_errors.log',
            'formatter': 'verbose',
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
# CONFIGURAÇÕES ADICIONAIS
# =============================================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Cache (opcional - para melhor performance)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': BASE_DIR / 'cache',
    }
}

# Session settings
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 86400  # 24 horas
