#!/usr/bin/env python3
"""
DIAGNÓSTICO EMERGENCIAL - Identifica problema exato
Execute: python3.10 diagnostico_emergencial.py
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Executa comando e retorna resultado"""
    print(f"\n🔍 {description}")
    print(f"Comando: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        print(f"Return code: {result.returncode}")
        if result.stdout:
            print(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            print(f"STDERR:\n{result.stderr}")
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        print(f"ERRO: {e}")
        return -1, "", str(e)

def check_critical_files():
    """Verifica arquivos críticos"""
    print("\n" + "="*60)
    print("🔍 VERIFICAÇÃO CRÍTICA DE ARQUIVOS")
    print("="*60)
    
    critical_files = {
        'manage.py': 'Arquivo principal Django',
        '.env': 'Variáveis de ambiente',
        'setup/settings.py': 'Settings padrão',
        'setup/production_settings.py': 'Settings produção',
        'setup/wsgi.py': 'Configuração WSGI',
        'static/img/home2.jpg': 'Imagem home',
        'staticfiles/img/home2.jpg': 'Imagem coletada',
        'requirements.txt': 'Dependências'
    }
    
    missing_files = []
    for file_path, description in critical_files.items():
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            print(f"✅ {file_path} ({description}) - {size:,} bytes")
        else:
            print(f"❌ {file_path} ({description}) - AUSENTE")
            missing_files.append(file_path)
    
    return missing_files

def test_env_file():
    """Testa arquivo .env em detalhes"""
    print("\n" + "="*60)
    print("🔍 ANÁLISE DETALHADA DO .env")
    print("="*60)
    
    env_path = Path('.env')
    if not env_path.exists():
        print("❌ CRÍTICO: Arquivo .env não existe!")
        return False
    
    try:
        # Ler como bytes para verificar encoding
        with open(env_path, 'rb') as f:
            raw_content = f.read()
        
        print(f"📊 Tamanho do arquivo: {len(raw_content)} bytes")
        print(f"📊 Primeiros 100 caracteres (hex): {raw_content[:100].hex()}")
        
        # Tentar ler como UTF-8
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print("✅ Encoding UTF-8 OK")
            
            # Verificar linhas
            lines = content.split('\n')
            print(f"📊 Total de linhas: {len(lines)}")
            
            required_vars = ['SECRET_KEY', 'ALLOWED_HOSTS', 'DEBUG']
            for var in required_vars:
                found = any(line.startswith(var) for line in lines)
                print(f"{'✅' if found else '❌'} {var} encontrado")
            
            # Mostrar conteúdo (mascarando SECRET_KEY)
            print("\n📄 Conteúdo do .env:")
            for i, line in enumerate(lines[:20], 1):
                if 'SECRET_KEY' in line:
                    print(f"{i:2d}: SECRET_KEY=***MASKED***")
                else:
                    print(f"{i:2d}: {line}")
            
            return True
            
        except UnicodeDecodeError as e:
            print(f"❌ ERRO DE ENCODING: {e}")
            return False
            
    except Exception as e:
        print(f"❌ ERRO ao ler .env: {e}")
        return False

def test_django_startup():
    """Testa inicialização do Django"""
    print("\n" + "="*60)
    print("🔍 TESTE DE INICIALIZAÇÃO DJANGO")
    print("="*60)
    
    # Testar com production_settings
    code, stdout, stderr = run_command(
        'python3.10 -c "import os; os.environ[\'DJANGO_SETTINGS_MODULE\'] = \'setup.production_settings\'; import django; django.setup(); print(\'DJANGO OK\')"',
        "Teste inicialização Django"
    )
    
    if code == 0:
        print("✅ Django inicializa corretamente")
        return True
    else:
        print("❌ Django FALHA ao inicializar")
        print("🔍 Tentando com settings padrão...")
        
        code2, stdout2, stderr2 = run_command(
            'python3.10 -c "import os; os.environ[\'DJANGO_SETTINGS_MODULE\'] = \'setup.settings\'; import django; django.setup(); print(\'DJANGO OK\')"',
            "Teste settings padrão"
        )
        
        return code2 == 0

def test_dependencies():
    """Verifica dependências instaladas"""
    print("\n" + "="*60)
    print("🔍 VERIFICAÇÃO DE DEPENDÊNCIAS")
    print("="*60)
    
    deps = ['django', 'python-decouple', 'Pillow']
    missing_deps = []
    
    for dep in deps:
        code, stdout, stderr = run_command(
            f'python3.10 -c "import {dep.replace("-", "_")}; print(\'{dep} OK\')"',
            f"Verificando {dep}"
        )
        
        if code != 0:
            missing_deps.append(dep)
    
    return missing_deps

def test_static_collection():
    """Testa coleta de arquivos estáticos"""
    print("\n" + "="*60)
    print("🔍 TESTE COLLECTSTATIC")
    print("="*60)
    
    code, stdout, stderr = run_command(
        'python3.10 manage.py collectstatic --noinput --settings=setup.production_settings --verbosity=2',
        "Executando collectstatic"
    )
    
    return code == 0

def test_migrations():
    """Verifica status das migrations"""
    print("\n" + "="*60)
    print("🔍 VERIFICAÇÃO DE MIGRATIONS")
    print("="*60)
    
    code, stdout, stderr = run_command(
        'python3.10 manage.py showmigrations --settings=setup.production_settings',
        "Status das migrations"
    )
    
    if code == 0:
        # Verificar se há migrations não aplicadas
        unapplied = '[' in stdout and ']' in stdout
        if unapplied:
            print("⚠️ HÁ MIGRATIONS NÃO APLICADAS!")
            return False
        else:
            print("✅ Todas migrations aplicadas")
            return True
    
    return False

def test_direct_blog_access():
    """Testa acesso direto ao blog via Django"""
    print("\n" + "="*60)
    print("🔍 TESTE DIRETO DA VIEW BLOG")
    print("="*60)
    
    test_code = """
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'setup.production_settings'
import django
django.setup()

try:
    from artigos.views import blog
    from django.test import RequestFactory
    
    factory = RequestFactory()
    request = factory.get('/blog/')
    response = blog(request)
    print(f'BLOG VIEW OK: Status {response.status_code}')
    
    # Verificar artigos
    from artigos.models import Artigo
    count = Artigo.objects.count()
    print(f'ARTIGOS NO BANCO: {count}')
    
except Exception as e:
    print(f'ERRO NO BLOG: {e}')
    import traceback
    traceback.print_exc()
"""
    
    code, stdout, stderr = run_command(
        f'python3.10 -c "{test_code}"',
        "Teste direto blog view"
    )
    
    return code == 0

def generate_emergency_fix():
    """Gera correção de emergência"""
    print("\n" + "="*60)
    print("🚨 CORREÇÃO DE EMERGÊNCIA")
    print("="*60)
    
    print("""
# EXECUTE ESTES COMANDOS EM ORDEM:

# 1. RECRIAR .env LIMPO
cat > .env << 'EOF'
SECRET_KEY=django-insecure-emergency-key-2025
DEBUG=False
ALLOWED_HOSTS=prismaav.pythonanywhere.com,localhost,127.0.0.1,testserver
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
STATIC_URL=/static/
STATIC_ROOT=staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=media
EOF

# 2. INSTALAR DEPENDÊNCIAS
pip3.10 install --user django python-decouple Pillow

# 3. VERIFICAR SE PRODUCTION_SETTINGS EXISTE
ls -la setup/production_settings.py

# 4. SE NÃO EXISTIR, CRIAR:
cp setup/settings.py setup/production_settings.py

# 5. APLICAR MIGRATIONS
python3.10 manage.py migrate --settings=setup.production_settings

# 6. COLLECTSTATIC
python3.10 manage.py collectstatic --noinput --settings=setup.production_settings

# 7. TESTAR DJANGO
python3.10 manage.py check --settings=setup.production_settings

# 8. NO PAINEL PYTHONANYWHERE:
#    - Web Apps → Static files:
#      URL: /static/ → Directory: /home/prismaav/staticfiles
#      URL: /media/ → Directory: /home/prismaav/media
#    - WSGI file deve conter:
#      os.environ['DJANGO_SETTINGS_MODULE'] = 'setup.production_settings'
#    - Reload da aplicação

# 9. SE AINDA FALHAR, VER LOGS:
tail -n 100 /home/prismaav/logs/*.error.log
""")

def main():
    """Diagnóstico emergencial completo"""
    print("🚨 DIAGNÓSTICO EMERGENCIAL - PYTHONANYWHERE")
    print("="*60)
    print(f"📁 Diretório: {os.getcwd()}")
    print(f"🐍 Python: {sys.version}")
    
    if not Path('manage.py').exists():
        print("❌ ERRO CRÍTICO: Não está no diretório do projeto Django!")
        sys.exit(1)
    
    # Executar todos os testes
    tests = [
        ("Arquivos críticos", check_critical_files),
        ("Arquivo .env", test_env_file), 
        ("Inicialização Django", test_django_startup),
        ("Dependências", test_dependencies),
        ("Migrations", test_migrations),
        ("Collectstatic", test_static_collection),
        ("Blog direto", test_direct_blog_access)
    ]
    
    failed_tests = []
    for name, test_func in tests:
        print(f"\n{'='*20} {name.upper()} {'='*20}")
        try:
            result = test_func()
            if not result:
                failed_tests.append(name)
        except Exception as e:
            print(f"❌ ERRO CRÍTICO em {name}: {e}")
            failed_tests.append(name)
    
    # Resumo final
    print("\n" + "="*60)
    print("📊 RESUMO FINAL")
    print("="*60)
    
    if failed_tests:
        print("❌ PROBLEMAS CRÍTICOS ENCONTRADOS:")
        for test in failed_tests:
            print(f"   - {test}")
        
        print("\n🚨 EXECUTAR CORREÇÃO DE EMERGÊNCIA:")
        generate_emergency_fix()
    else:
        print("✅ TODOS OS TESTES PASSARAM!")
        print("💡 O problema está na configuração do PythonAnywhere:")
        print("   1. Verificar Static files mapping no Web tab")
        print("   2. Verificar WSGI configuration file")
        print("   3. Fazer reload da aplicação")
        print("   4. Verificar Error log para detalhes específicos")

if __name__ == '__main__':
    main()
