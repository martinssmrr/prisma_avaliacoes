#!/usr/bin/env python3
"""
DIAGNÓSTICO COMPLETO - PythonAnywhere
Execute: python3.10 diagnostico_pythonanywhere.py
"""

import os
import sys
import subprocess
from pathlib import Path

def executar_comando(comando, descricao):
    """Executa um comando e mostra o resultado"""
    print(f"\n🔍 {descricao}...")
    try:
        result = subprocess.run(comando, shell=True, capture_output=True, text=True)
        print(f"Comando: {comando}")
        print(f"Return code: {result.returncode}")
        if result.stdout.strip():
            print(f"STDOUT:\n{result.stdout.strip()}")
        if result.stderr.strip():
            print(f"STDERR:\n{result.stderr.strip()}")
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        print(f"❌ Erro ao executar comando: {e}")
        return False, "", str(e)

def verificar_estrutura_arquivos():
    """Verifica a estrutura de arquivos"""
    print("\n📁 VERIFICANDO ESTRUTURA DE ARQUIVOS")
    print("=" * 50)
    
    arquivos_importantes = [
        'manage.py',
        'setup/settings.py', 
        'setup/production_settings.py',
        'setup/wsgi.py',
        '.env',
        'static/img/home2.jpg',
        'staticfiles/img/home2.jpg',
        'templates/Prisma_avaliacoes/home.html'
    ]
    
    for arquivo in arquivos_importantes:
        caminho = Path(arquivo)
        if caminho.exists():
            tamanho = caminho.stat().st_size
            print(f"✅ {arquivo} - {tamanho} bytes")
        else:
            print(f"❌ {arquivo} - NÃO ENCONTRADO")

def verificar_configuracoes_django():
    """Verifica configurações Django"""
    print("\n⚙️ VERIFICANDO CONFIGURAÇÕES DJANGO")
    print("=" * 50)
    
    # Verificar production_settings.py
    prod_settings = Path('setup/production_settings.py')
    if prod_settings.exists():
        print("✅ production_settings.py existe")
        with open(prod_settings, 'r') as f:
            content = f.read()
            
        # Verificar ALLOWED_HOSTS
        if 'ALLOWED_HOSTS' in content:
            print("✅ ALLOWED_HOSTS definido")
            # Extrair ALLOWED_HOSTS
            lines = content.split('\n')
            for line in lines:
                if 'ALLOWED_HOSTS' in line and not line.strip().startswith('#'):
                    print(f"   {line.strip()}")
        else:
            print("❌ ALLOWED_HOSTS não encontrado")
            
        # Verificar DEBUG
        if 'DEBUG' in content:
            lines = content.split('\n')
            for line in lines:
                if line.strip().startswith('DEBUG') and not line.strip().startswith('#'):
                    print(f"   {line.strip()}")
    else:
        print("❌ production_settings.py NÃO ENCONTRADO")

def verificar_arquivo_env():
    """Verifica arquivo .env"""
    print("\n📄 VERIFICANDO ARQUIVO .env")
    print("=" * 50)
    
    env_file = Path('.env')
    if env_file.exists():
        print("✅ .env existe")
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar variáveis importantes
            vars_importantes = ['SECRET_KEY', 'DEBUG', 'ALLOWED_HOSTS', 'STATIC_URL', 'MEDIA_URL']
            for var in vars_importantes:
                if var in content:
                    # Extrair valor
                    lines = content.split('\n')
                    for line in lines:
                        if line.strip().startswith(var) and '=' in line:
                            print(f"   {line.strip()}")
                            break
                else:
                    print(f"❌ {var} não encontrado")
                    
        except UnicodeDecodeError as e:
            print(f"❌ Erro de codificação no .env: {e}")
        except Exception as e:
            print(f"❌ Erro ao ler .env: {e}")
    else:
        print("❌ .env NÃO ENCONTRADO")

def verificar_wsgi():
    """Verifica configuração WSGI"""
    print("\n🌐 VERIFICANDO CONFIGURAÇÃO WSGI")
    print("=" * 50)
    
    wsgi_file = Path('setup/wsgi.py')
    if wsgi_file.exists():
        print("✅ wsgi.py existe")
        with open(wsgi_file, 'r') as f:
            content = f.read()
        
        if 'DJANGO_SETTINGS_MODULE' in content:
            lines = content.split('\n')
            for line in lines:
                if 'DJANGO_SETTINGS_MODULE' in line and not line.strip().startswith('#'):
                    print(f"   {line.strip()}")
        else:
            print("❌ DJANGO_SETTINGS_MODULE não configurado")
    else:
        print("❌ wsgi.py NÃO ENCONTRADO")

def testar_django():
    """Testa configuração Django"""
    print("\n🧪 TESTANDO CONFIGURAÇÃO DJANGO")
    print("=" * 50)
    
    # Testar com production_settings
    success, stdout, stderr = executar_comando(
        'python3.10 manage.py check --settings=setup.production_settings', 
        'Django Check (production_settings)'
    )
    
    if not success:
        print("⚠️ Tentando com settings padrão...")
        executar_comando('python3.10 manage.py check', 'Django Check (settings padrão)')

def verificar_collectstatic():
    """Verifica arquivos estáticos"""
    print("\n📦 VERIFICANDO ARQUIVOS ESTÁTICOS")
    print("=" * 50)
    
    staticfiles_dir = Path('staticfiles')
    if staticfiles_dir.exists():
        print(f"✅ staticfiles/ existe")
        
        # Contar arquivos
        arquivos = list(staticfiles_dir.rglob('*'))
        arquivos_files = [f for f in arquivos if f.is_file()]
        print(f"   Total de arquivos: {len(arquivos_files)}")
        
        # Verificar home2.jpg especificamente
        home_img = staticfiles_dir / 'img' / 'home2.jpg'
        if home_img.exists():
            tamanho = home_img.stat().st_size
            print(f"✅ staticfiles/img/home2.jpg - {tamanho} bytes")
        else:
            print("❌ staticfiles/img/home2.jpg NÃO ENCONTRADO")
            
        # Listar alguns arquivos
        print("   Arquivos em staticfiles/:")
        for arquivo in sorted(arquivos_files)[:10]:
            rel_path = arquivo.relative_to(staticfiles_dir)
            print(f"      {rel_path}")
        if len(arquivos_files) > 10:
            print(f"      ... e mais {len(arquivos_files) - 10} arquivos")
    else:
        print("❌ staticfiles/ NÃO ENCONTRADO")

def verificar_urls():
    """Verifica configuração de URLs"""
    print("\n🔗 VERIFICANDO CONFIGURAÇÃO DE URLs")
    print("=" * 50)
    
    # URLs principais
    urls_file = Path('setup/urls.py')
    if urls_file.exists():
        print("✅ setup/urls.py existe")
        with open(urls_file, 'r') as f:
            content = f.read()
        
        if 'static' in content and 'MEDIA_URL' in content:
            print("✅ Configuração de static/media URLs presente")
        else:
            print("❌ Configuração de static/media URLs ausente")
            
        if 'include' in content:
            print("✅ Apps incluídos")
        else:
            print("⚠️ Verificar se apps estão incluídos")
    else:
        print("❌ setup/urls.py NÃO ENCONTRADO")

def verificar_apps():
    """Verifica apps Django"""
    print("\n📱 VERIFICANDO APPS DJANGO")
    print("=" * 50)
    
    apps = ['Prisma_avaliacoes', 'artigos']
    for app in apps:
        app_dir = Path(app)
        if app_dir.exists():
            print(f"✅ {app}/ existe")
            
            # Verificar arquivos importantes do app
            arquivos_app = ['models.py', 'views.py', 'urls.py']
            for arquivo in arquivos_app:
                arquivo_path = app_dir / arquivo
                if arquivo_path.exists():
                    print(f"   ✅ {arquivo}")
                else:
                    print(f"   ❌ {arquivo}")
        else:
            print(f"❌ {app}/ NÃO ENCONTRADO")

def main():
    """Executa diagnóstico completo"""
    print("🚨 DIAGNÓSTICO COMPLETO - PYTHONANYWHERE")
    print("=" * 60)
    print(f"📁 Diretório atual: {os.getcwd()}")
    print(f"🐍 Python: {sys.version}")
    print(f"🌍 PATH: {os.environ.get('PATH', 'N/A')[:100]}...")
    
    if not Path('manage.py').exists():
        print("❌ ERRO: Execute este script no diretório raiz do projeto Django!")
        sys.exit(1)
    
    # Executar todas as verificações
    verificar_estrutura_arquivos()
    verificar_arquivo_env()
    verificar_configuracoes_django()
    verificar_wsgi()
    verificar_urls()
    verificar_apps()
    verificar_collectstatic()
    testar_django()
    
    print("\n" + "=" * 60)
    print("🎯 DIAGNÓSTICO CONCLUÍDO!")
    print("=" * 60)
    print("\n💡 Próximos passos:")
    print("1. Analise os resultados acima")
    print("2. Corrija problemas identificados")
    print("3. Execute: python3.10 corrigir_problemas_pythonanywhere.py")
    print("4. Reload da Web App no PythonAnywhere")

if __name__ == '__main__':
    main()
