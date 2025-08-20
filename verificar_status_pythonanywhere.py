#!/usr/bin/env python3
"""
VERIFICAÇÃO RÁPIDA - Status PythonAnywhere
Execute: python3.10 verificar_status_pythonanywhere.py
"""

import os
import sys
from pathlib import Path

def check_env_file():
    """Verifica arquivo .env"""
    print("🔍 VERIFICANDO ARQUIVO .env")
    print("-" * 40)
    
    if not Path('.env').exists():
        print("❌ .env NÃO EXISTE")
        return False
    
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = {
            'SECRET_KEY': 'SECRET_KEY=' in content,
            'ALLOWED_HOSTS': 'ALLOWED_HOSTS=' in content and 'prismaav.pythonanywhere.com' in content,
            'STATIC_URL': 'STATIC_URL=/static/' in content,
            'STATIC_ROOT': 'STATIC_ROOT=staticfiles' in content
        }
        
        all_ok = True
        for key, ok in checks.items():
            status = "✅" if ok else "❌"
            print(f"{status} {key}")
            if not ok:
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print(f"❌ Erro ao ler .env: {e}")
        return False

def check_production_settings():
    """Verifica production_settings.py"""
    print("\n🔍 VERIFICANDO PRODUCTION_SETTINGS.PY")
    print("-" * 40)
    
    settings_file = Path('setup/production_settings.py')
    if not settings_file.exists():
        print("❌ setup/production_settings.py NÃO EXISTE")
        return False
    
    print("✅ setup/production_settings.py EXISTE")
    return True

def check_image_files():
    """Verifica arquivos de imagem"""
    print("\n🔍 VERIFICANDO IMAGENS")
    print("-" * 40)
    
    checks = {
        'static/img/home2.jpg': Path('static/img/home2.jpg'),
        'staticfiles/img/home2.jpg': Path('staticfiles/img/home2.jpg')
    }
    
    all_ok = True
    for name, path in checks.items():
        if path.exists():
            size = path.stat().st_size
            print(f"✅ {name} - {size:,} bytes")
        else:
            print(f"❌ {name} - NÃO ENCONTRADO")
            all_ok = False
    
    return all_ok

def check_directories():
    """Verifica diretórios necessários"""
    print("\n🔍 VERIFICANDO DIRETÓRIOS")
    print("-" * 40)
    
    dirs = ['static/img', 'staticfiles', 'media', 'templates']
    all_ok = True
    
    for dir_name in dirs:
        path = Path(dir_name)
        if path.exists() and path.is_dir():
            print(f"✅ {dir_name}/")
        else:
            print(f"❌ {dir_name}/ - NÃO ENCONTRADO")
            all_ok = False
    
    return all_ok

def check_wsgi_config():
    """Verifica configuração WSGI"""
    print("\n🔍 VERIFICANDO WSGI")
    print("-" * 40)
    
    wsgi_file = Path('setup/wsgi.py')
    if not wsgi_file.exists():
        print("❌ setup/wsgi.py NÃO EXISTE")
        return False
    
    with open(wsgi_file, 'r') as f:
        content = f.read()
    
    if 'production_settings' in content:
        print("✅ WSGI configurado para production_settings")
        return True
    else:
        print("❌ WSGI NÃO está usando production_settings")
        print("💡 Deve conter: os.environ['DJANGO_SETTINGS_MODULE'] = 'setup.production_settings'")
        return False

def generate_commands():
    """Gera comandos para execução"""
    print("\n🚀 COMANDOS PARA EXECUTAR NO PYTHONANYWHERE")
    print("=" * 50)
    
    commands = [
        "# 1. Atualizar repositório",
        "cd /home/prismaav",
        "git pull origin master",
        "",
        "# 2. Instalar dependências", 
        "pip3.10 install --user -r requirements.txt",
        "",
        "# 3. Executar migrações",
        "python3.10 manage.py migrate --settings=setup.production_settings",
        "",
        "# 4. Coletar arquivos estáticos",
        "python3.10 manage.py collectstatic --noinput --settings=setup.production_settings",
        "",
        "# 5. Verificar se tudo está OK",
        "python3.10 manage.py check --settings=setup.production_settings",
        "",
        "# 6. DEPOIS: Reload da Web App no painel"
    ]
    
    for cmd in commands:
        print(cmd)

def main():
    """Executa verificação completa"""
    print("🔍 VERIFICAÇÃO RÁPIDA - PYTHONANYWHERE")
    print("=" * 50)
    print(f"📁 Diretório: {os.getcwd()}")
    
    if not Path('manage.py').exists():
        print("❌ Execute no diretório raiz do projeto Django!")
        sys.exit(1)
    
    # Executar verificações
    checks = [
        ("Arquivo .env", check_env_file),
        ("Production Settings", check_production_settings),
        ("Diretórios", check_directories),
        ("Imagens", check_image_files),
        ("WSGI Config", check_wsgi_config)
    ]
    
    all_passed = True
    for name, check_func in checks:
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ TODAS VERIFICAÇÕES PASSARAM!")
        print("💡 Se ainda não funcionar, verifique:")
        print("   1. Mapeamento Static Files no Web tab")
        print("   2. WSGI file no painel aponta para production_settings")
        print("   3. Error log para detalhes específicos")
    else:
        print("❌ PROBLEMAS ENCONTRADOS!")
        print("💡 Execute os comandos abaixo para corrigir:")
    
    generate_commands()

if __name__ == '__main__':
    main()
