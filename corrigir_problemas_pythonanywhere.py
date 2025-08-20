#!/usr/bin/env python3
"""
CORREÇÃO DEFINITIVA - PythonAnywhere
Execute: python3.10 corrigir_problemas_pythonanywhere.py
"""

import os
import sys
import subprocess
from pathlib import Path

def executar_comando(comando, descricao):
    """Executa um comando e mostra o resultado"""
    print(f"\n🔧 {descricao}...")
    try:
        result = subprocess.run(comando, shell=True, capture_output=True, text=True)
        print(f"Comando: {comando}")
        if result.returncode == 0:
            print(f"✅ Sucesso!")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        else:
            print(f"⚠️ Código de saída: {result.returncode}")
            if result.stderr.strip():
                print(f"Erro: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def criar_env_pythonanywhere():
    """Cria arquivo .env correto para PythonAnywhere"""
    print("\n📝 CRIANDO ARQUIVO .env PARA PYTHONANYWHERE")
    print("=" * 50)
    
    env_content = """# Configuracao PythonAnywhere - SEM CARACTERES ESPECIAIS
SECRET_KEY=django-insecure-prisma-av-pythonanywhere-key-2025
DEBUG=False
ALLOWED_HOSTS=prismaav.pythonanywhere.com,localhost,127.0.0.1,testserver
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DJANGO_SUPERUSER_USERNAME=prismaav
DJANGO_SUPERUSER_PASSWORD=PrismaAv4002
DJANGO_SUPERUSER_EMAIL=admin@prismaavaliacoes.com
STATIC_URL=/static/
STATIC_ROOT=staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=media
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Arquivo .env criado com sucesso!")
        
        # Verificar se foi criado corretamente
        with open('.env', 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ Arquivo tem {len(content)} caracteres")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar .env: {e}")
        return False

def verificar_production_settings():
    """Verifica e corrige production_settings.py"""
    print("\n⚙️ VERIFICANDO PRODUCTION_SETTINGS.PY")
    print("=" * 50)
    
    prod_settings = Path('setup/production_settings.py')
    if not prod_settings.exists():
        print("❌ production_settings.py não existe! Criando...")
        
        content = """import os
from pathlib import Path
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-default-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth", 
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "Prisma_avaliacoes",
    "artigos",
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
            ],
        },
    },
]

WSGI_APPLICATION = "setup.wsgi.application"

# Database
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': config('DB_NAME', default=BASE_DIR / 'db.sqlite3'),
        'USER': config('DB_USER', default=''),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default=''),
        'PORT': config('DB_PORT', default=''),
    }
}

# Internationalization
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = config('STATIC_URL', default='/static/')
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / config('STATIC_ROOT', default='staticfiles')

# Media files
MEDIA_URL = config('MEDIA_URL', default='/media/')
MEDIA_ROOT = BASE_DIR / config('MEDIA_ROOT', default='media')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
"""
        
        try:
            with open(prod_settings, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ production_settings.py criado!")
            return True
        except Exception as e:
            print(f"❌ Erro ao criar production_settings.py: {e}")
            return False
    else:
        print("✅ production_settings.py já existe")
        return True

def corrigir_wsgi():
    """Corrige arquivo WSGI"""
    print("\n🌐 VERIFICANDO ARQUIVO WSGI")
    print("=" * 50)
    
    wsgi_file = Path('setup/wsgi.py')
    if wsgi_file.exists():
        with open(wsgi_file, 'r') as f:
            content = f.read()
        
        if 'production_settings' not in content:
            print("⚠️ WSGI não está usando production_settings")
            # Criar backup
            backup_content = content
            
            # Substituir settings por production_settings
            new_content = content.replace(
                'os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")',
                'os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.production_settings")'
            )
            
            try:
                with open(wsgi_file, 'w') as f:
                    f.write(new_content)
                print("✅ WSGI atualizado para usar production_settings")
                return True
            except Exception as e:
                print(f"❌ Erro ao atualizar WSGI: {e}")
                # Restaurar backup
                with open(wsgi_file, 'w') as f:
                    f.write(backup_content)
                return False
        else:
            print("✅ WSGI já está configurado corretamente")
            return True
    else:
        print("❌ wsgi.py não encontrado")
        return False

def criar_diretorios():
    """Cria diretórios necessários"""
    print("\n📁 CRIANDO DIRETÓRIOS NECESSÁRIOS")
    print("=" * 50)
    
    diretorios = [
        'static/img',
        'static/css', 
        'static/js',
        'media/artigos/imagens',
        'staticfiles',
        'templates/Prisma_avaliacoes',
        'templates/artigos'
    ]
    
    for diretorio in diretorios:
        dir_path = Path(diretorio)
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ {diretorio}/")
        except Exception as e:
            print(f"❌ {diretorio}/ - Erro: {e}")

def executar_comandos_django():
    """Executa comandos Django necessários"""
    print("\n🔄 EXECUTANDO COMANDOS DJANGO")
    print("=" * 50)
    
    comandos = [
        ('python3.10 manage.py migrate --settings=setup.production_settings', 'Executando migrações'),
        ('python3.10 manage.py collectstatic --noinput --settings=setup.production_settings', 'Coletando arquivos estáticos'),
    ]
    
    for comando, descricao in comandos:
        sucesso = executar_comando(comando, descricao)
        if not sucesso:
            print(f"⚠️ Falha em: {comando}")

def verificar_imagem():
    """Verifica se a imagem existe"""
    print("\n🖼️ VERIFICANDO IMAGEM HOME2.JPG")
    print("=" * 50)
    
    # Verificar em static/img
    img_static = Path('static/img/home2.jpg')
    if img_static.exists():
        tamanho = img_static.stat().st_size
        print(f"✅ static/img/home2.jpg - {tamanho} bytes")
    else:
        print("❌ static/img/home2.jpg NÃO ENCONTRADO")
        print("💡 Faça upload da imagem para static/img/")
    
    # Verificar em staticfiles após collectstatic
    img_staticfiles = Path('staticfiles/img/home2.jpg')
    if img_staticfiles.exists():
        tamanho = img_staticfiles.stat().st_size
        print(f"✅ staticfiles/img/home2.jpg - {tamanho} bytes")
    else:
        print("❌ staticfiles/img/home2.jpg NÃO ENCONTRADO")
        print("💡 Execute collectstatic novamente")

def testar_configuracao():
    """Testa a configuração final"""
    print("\n🧪 TESTANDO CONFIGURAÇÃO FINAL")
    print("=" * 50)
    
    # Test Django check
    success = executar_comando(
        'python3.10 manage.py check --settings=setup.production_settings',
        'Django System Check'
    )
    
    if success:
        print("✅ Configuração Django OK!")
    else:
        print("❌ Problemas na configuração Django")
    
    # Testar imports
    try:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'setup.production_settings'
        import django
        django.setup()
        from django.conf import settings
        
        print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"✅ DEBUG: {settings.DEBUG}")
        print(f"✅ STATIC_URL: {settings.STATIC_URL}")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao importar Django: {e}")
        return False

def main():
    """Executa todas as correções"""
    print("🚨 CORREÇÃO DEFINITIVA - PYTHONANYWHERE")
    print("=" * 60)
    
    if not Path('manage.py').exists():
        print("❌ Execute este script no diretório raiz do projeto!")
        sys.exit(1)
    
    print(f"📁 Diretório: {os.getcwd()}")
    
    # Executar correções em ordem
    steps = [
        criar_env_pythonanywhere,
        verificar_production_settings,
        corrigir_wsgi,
        criar_diretorios,
        executar_comandos_django,
        verificar_imagem,
        testar_configuracao
    ]
    
    sucesso_total = True
    for step in steps:
        try:
            if not step():
                sucesso_total = False
        except Exception as e:
            print(f"❌ Erro em {step.__name__}: {e}")
            sucesso_total = False
    
    print("\n" + "=" * 60)
    if sucesso_total:
        print("✅ CORREÇÕES APLICADAS COM SUCESSO!")
        print("=" * 60)
        print("\n🔄 PRÓXIMOS PASSOS NO PYTHONANYWHERE:")
        print("1. Vá para Web Apps")
        print("2. Clique em 'Reload' na sua aplicação")
        print("3. Teste: https://prismaav.pythonanywhere.com")
        print("4. Teste blog: https://prismaav.pythonanywhere.com/blog/")
        print("\n💡 Se ainda houver problemas:")
        print("1. Verifique Error Log no PythonAnywhere")
        print("2. Verifique se o WSGI file está apontando para production_settings")
    else:
        print("❌ ALGUMAS CORREÇÕES FALHARAM")
        print("=" * 60)
        print("🔍 Execute diagnostico_pythonanywhere.py para mais detalhes")

if __name__ == '__main__':
    main()
