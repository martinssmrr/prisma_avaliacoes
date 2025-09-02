"""
Configurações de Produção para VPS Ubuntu + Nginx + Gunicorn
Django settings for Prisma Avaliações - VPS Production Environment
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# =============================================================================
# CONFIGURAÇÕES DE SEGURANÇA
# =============================================================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-CHANGE-THIS-IN-PRODUCTION-xyz123abc456def789')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Hosts permitidos - VPS Hostinger
ALLOWED_HOSTS = [
    'www.prismaavaliacoes.com.br',
    'prismaavaliacoes.com.br',
    'localhost',
    '127.0.0.1'
]

# =============================================================================
# CONFIGURAÇÕES DE SEGURANÇA SSL
# =============================================================================

# Forçar HTTPS
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cookies seguros
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 ano
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

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
# TEMPLATES
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
# CONFIGURAÇÃO DO BANCO DE DADOS
# =============================================================================

# SQLite para produção (pode ser alterado para PostgreSQL se necessário)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
# ARQUIVOS ESTÁTICOS E MEDIA
# =============================================================================

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files (uploads)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# =============================================================================
# CONFIGURAÇÕES DO JAZZMIN
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
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",  # Navbar claro para melhor contraste
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-light-primary",  # Sidebar claro
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "lumen",  # Tema claro consistente
    "dark_mode_theme": "darkly",
}

# =============================================================================
# LOGGING
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
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Campo padrão para auto field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =============================================================================
# CONFIGURAÇÕES DE EMAIL (ajustar conforme necessário)
# =============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'contato@prismaavaliacoes.com.br')
