"""
Configurações temporárias para desenvolvimento local
Use: python manage.py runserver --settings=dev_settings
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# Forçar modo desenvolvimento
DEBUG = True

# Hosts permitidos para desenvolvimento
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
]

# Configuração básica de URLs
ROOT_URLCONF = 'setup.urls'

# Configuração básica WSGI
WSGI_APPLICATION = 'setup.wsgi.application'

# SECRET_KEY para desenvolvimento
SECRET_KEY = 'django-insecure-dev-key-only-for-local-development'

# Apps instalados
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
    "area_cliente",  # Nova área do cliente
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Templates
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

# Banco de dados SQLite local
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Arquivos estáticos
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Internacionalização
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# Campo padrão para auto field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Configurações do Django Jazzmin
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

print("🚀 USANDO CONFIGURAÇÕES DE DESENVOLVIMENTO")
print(f"📋 DEBUG: {DEBUG}")
print(f"🌐 ALLOWED_HOSTS: {ALLOWED_HOSTS}")
print(f"🗂️ ROOT_URLCONF: {ROOT_URLCONF}")
