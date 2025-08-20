#!/usr/bin/env python3
"""
Script de correção para problemas de imagem e erro 500 no blog
Execute no PythonAnywhere: python corrigir_problemas.py
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
        if result.returncode == 0:
            print(f"✅ {descricao} - Sucesso!")
            if result.stdout.strip():
                print(result.stdout.strip())
        else:
            print(f"⚠️ {descricao} - Aviso:")
            if result.stderr.strip():
                print(result.stderr.strip())
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {descricao} - Erro: {e}")
        return False

def criar_env_corrigido():
    """Cria arquivo .env corrigido para produção"""
    
    print("📝 Criando arquivo .env corrigido...")
    
    env_content = """# Configurações de produção PythonAnywhere - CORRIGIDO
SECRET_KEY=django-insecure-(=-&$c%lq2!cxtmdwinj4uw&yftv$0*jsgn*)ew)%accjk@gk$
DEBUG=False
ALLOWED_HOSTS=prismaav.pythonanywhere.com,localhost,127.0.0.1,testserver
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DJANGO_SUPERUSER_USERNAME=prismaav
DJANGO_SUPERUSER_PASSWORD=PrismaAv4002@--
DJANGO_SUPERUSER_EMAIL=admin@prismaavaliacoes.com
STATIC_URL=/static/
STATIC_ROOT=staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=media
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Arquivo .env criado com hosts corrigidos!")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar .env: {e}")
        return False

def verificar_estrutura_diretorios():
    """Verifica e cria estrutura de diretórios necessária"""
    
    print("\n📁 Verificando estrutura de diretórios...")
    
    diretorios = [
        'static/img',
        'static/css',
        'static/js', 
        'media/artigos/imagens',
        'staticfiles'
    ]
    
    for diretorio in diretorios:
        dir_path = Path(diretorio)
        if dir_path.exists():
            print(f"✅ {diretorio}/")
        else:
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"✅ {diretorio}/ - CRIADO")
            except Exception as e:
                print(f"❌ {diretorio}/ - Erro: {e}")

def corrigir_imagens():
    """Corrige problemas de imagens"""
    
    print("\n🖼️ Corrigindo imagens...")
    
    # Verificar se home2.jpg existe em static/img
    home_img_static = Path('static/img/home2.jpg')
    home_img_media = Path('media/home2.jpg')
    
    if not home_img_static.exists():
        if home_img_media.exists():
            try:
                # Copiar da media para static/img
                import shutil
                shutil.copy2(home_img_media, home_img_static)
                print("✅ home2.jpg copiado de media/ para static/img/")
            except Exception as e:
                print(f"❌ Erro ao copiar imagem: {e}")
        else:
            print("⚠️ Imagem home2.jpg não encontrada em media/")
            # Criar uma imagem placeholder se necessário
            print("💡 Você pode fazer upload da imagem manualmente")
    else:
        print("✅ home2.jpg já existe em static/img/")

def corrigir_settings_producao():
    """Corrige configurações de produção"""
    
    print("\n⚙️ Verificando configurações de produção...")
    
    # Verificar se production_settings.py existe
    prod_settings = Path('setup/production_settings.py')
    if prod_settings.exists():
        print("✅ production_settings.py existe")
        
        # Ler e verificar ALLOWED_HOSTS
        with open(prod_settings, 'r') as f:
            content = f.read()
            
        if 'prismaav.pythonanywhere.com' in content:
            print("✅ ALLOWED_HOSTS configurado em production_settings.py")
        else:
            print("⚠️ ALLOWED_HOSTS pode estar incorreto")
    else:
        print("❌ production_settings.py não encontrado")

def verificar_dependencias():
    """Verifica e instala dependências"""
    
    print("\n📦 Verificando dependências...")
    
    dependencias = ['django', 'python-decouple', 'Pillow']
    
    # Detectar comando pip
    pip_cmd = 'pip'
    if 'PYTHONANYWHERE_DOMAIN' in os.environ or '--pythonanywhere' in sys.argv:
        pip_cmd = 'pip3.10'
    
    for dep in dependencias:
        try:
            if dep == 'python-decouple':
                import decouple
            elif dep == 'django':
                import django
            elif dep == 'Pillow':
                import PIL
            print(f"✅ {dep} instalado")
        except ImportError:
            print(f"❌ {dep} não instalado")
            executar_comando(f'{pip_cmd} install --user {dep}', f'Instalando {dep}')

def testar_configuracao():
    """Testa a configuração Django"""
    
    print("\n🧪 Testando configuração Django...")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.production_settings')
        import django
        django.setup()
        
        from django.conf import settings
        print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"✅ DEBUG: {settings.DEBUG}")
        print(f"✅ STATIC_URL: {settings.STATIC_URL}")
        print(f"✅ MEDIA_URL: {settings.MEDIA_URL}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        return False

def main():
    print("🚨 CORREÇÃO DE PROBLEMAS - IMAGEM E BLOG")
    print("=" * 50)
    
    # Verificar se estamos no diretório correto
    if not Path('manage.py').exists():
        print("❌ Execute este script no diretório raiz do projeto Django!")
        sys.exit(1)
    
    print(f"📁 Diretório: {os.getcwd()}")
    
    # Executar correções
    criar_env_corrigido()
    verificar_estrutura_diretorios()
    corrigir_imagens()
    verificar_dependencias()
    corrigir_settings_producao()
    
    # Executar comandos Django
    print("\n🔄 Executando comandos Django...")
    
    # Detectar sistema operacional e comando Python
    python_cmd = 'python'
    pip_cmd = 'pip'
    
    # No PythonAnywhere usar python3.10
    if 'PYTHONANYWHERE_DOMAIN' in os.environ or '--pythonanywhere' in sys.argv:
        python_cmd = 'python3.10'
        pip_cmd = 'pip3.10'
    
    # Instalar dependências se requirements.txt existir
    if Path('requirements.txt').exists():
        executar_comando(f'{pip_cmd} install --user -r requirements.txt', 'Instalando dependências')
    
    # Executar migrações
    executar_comando(f'{python_cmd} manage.py migrate --settings=setup.production_settings', 'Executando migrações')
    
    # Coletar arquivos estáticos
    executar_comando(f'{python_cmd} manage.py collectstatic --noinput --settings=setup.production_settings', 'Coletando arquivos estáticos')
    
    # Verificar configuração
    if testar_configuracao():
        print("\n" + "=" * 50)
        print("✅ CORREÇÕES APLICADAS COM SUCESSO!")
        print("=" * 50)
        print("\n🔄 PRÓXIMOS PASSOS:")
        print("1. Reload da Web App no PythonAnywhere")
        print("2. Teste: https://prismaav.pythonanywhere.com")
        print("3. Teste blog: https://prismaav.pythonanywhere.com/blog/")
    else:
        print("\n❌ Ainda há problemas. Verifique o Error log no PythonAnywhere.")

if __name__ == '__main__':
    main()
