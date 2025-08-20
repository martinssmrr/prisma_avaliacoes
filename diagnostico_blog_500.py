#!/usr/bin/env python3
"""
DIAGNÓSTICO ESPECÍFICO - Erro 500 Blog
Execute: python3.10 diagnostico_blog_500.py
"""

import os
import sys
from pathlib import Path

def test_django_import():
    """Testa importação Django"""
    print("🔍 TESTANDO IMPORTAÇÃO DJANGO")
    print("-" * 40)
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.production_settings')
        import django
        django.setup()
        print("✅ Django importado com sucesso")
        
        from django.conf import settings
        print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"✅ DEBUG: {settings.DEBUG}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao importar Django: {e}")
        return False

def test_apps():
    """Testa apps Django"""
    print("\n🔍 TESTANDO APPS")
    print("-" * 40)
    
    try:
        from django.apps import apps
        
        # Testar app Prisma_avaliacoes
        try:
            app = apps.get_app_config('Prisma_avaliacoes')
            print("✅ App Prisma_avaliacoes carregado")
        except Exception as e:
            print(f"❌ Erro no app Prisma_avaliacoes: {e}")
        
        # Testar app artigos
        try:
            app = apps.get_app_config('artigos')
            print("✅ App artigos carregado")
        except Exception as e:
            print(f"❌ Erro no app artigos: {e}")
            
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar apps: {e}")
        return False

def test_models():
    """Testa modelos"""
    print("\n🔍 TESTANDO MODELOS")
    print("-" * 40)
    
    try:
        # Testar modelo Empresa
        from Prisma_avaliacoes.models import Empresa
        empresas = Empresa.objects.all()
        print(f"✅ Modelo Empresa - {empresas.count()} registros")
        
        # Testar modelo Artigo
        from artigos.models import Artigo
        artigos = Artigo.objects.all()
        print(f"✅ Modelo Artigo - {artigos.count()} registros")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar modelos: {e}")
        return False

def test_urls():
    """Testa URLs"""
    print("\n🔍 TESTANDO URLs")
    print("-" * 40)
    
    try:
        from django.urls import reverse
        
        # Testar URLs principais
        urls_to_test = [
            ('home', 'Prisma_avaliacoes:home'),
            ('blog', 'artigos:blog'),
        ]
        
        for name, url_name in urls_to_test:
            try:
                url = reverse(url_name)
                print(f"✅ URL {name}: {url}")
            except Exception as e:
                print(f"❌ Erro na URL {name}: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar URLs: {e}")
        return False

def test_templates():
    """Testa templates"""
    print("\n🔍 TESTANDO TEMPLATES")
    print("-" * 40)
    
    templates = [
        'templates/artigos/blog.html',
        'templates/artigos/artigo_detail.html',
        'templates/Prisma_avaliacoes/home.html',
        'templates/base.html'
    ]
    
    all_ok = True
    for template in templates:
        path = Path(template)
        if path.exists():
            print(f"✅ {template}")
        else:
            print(f"❌ {template} - NÃO ENCONTRADO")
            all_ok = False
    
    return all_ok

def test_static_files():
    """Testa arquivos estáticos para o blog"""
    print("\n🔍 TESTANDO ARQUIVOS ESTÁTICOS")
    print("-" * 40)
    
    static_files = [
        'static/css/style.css',
        'static/js/main.js',
        'staticfiles/css/style.css',
        'staticfiles/js/main.js'
    ]
    
    for file_path in static_files:
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            print(f"✅ {file_path} - {size:,} bytes")
        else:
            print(f"❌ {file_path} - NÃO ENCONTRADO")

def test_database():
    """Testa banco de dados"""
    print("\n🔍 TESTANDO BANCO DE DADOS")
    print("-" * 40)
    
    try:
        from django.db import connection
        cursor = connection.cursor()
        
        # Testar conexão
        cursor.execute("SELECT 1")
        print("✅ Conexão com banco OK")
        
        # Verificar tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"✅ Tabelas no banco: {len(tables)}")
        
        # Verificar tabelas específicas
        table_names = [table[0] for table in tables]
        expected_tables = ['artigos_artigo', 'Prisma_avaliacoes_empresa']
        
        for table in expected_tables:
            if table in table_names:
                print(f"✅ Tabela {table} existe")
            else:
                print(f"❌ Tabela {table} NÃO EXISTE")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no banco de dados: {e}")
        return False

def test_view_blog():
    """Testa view do blog diretamente"""
    print("\n🔍 TESTANDO VIEW BLOG")
    print("-" * 40)
    
    try:
        from django.test import RequestFactory
        from artigos.views import blog
        
        factory = RequestFactory()
        request = factory.get('/blog/')
        
        response = blog(request)
        print(f"✅ View blog executada - Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Blog view funcionando corretamente")
            return True
        else:
            print(f"❌ Blog view retornou status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar view blog: {e}")
        return False

def generate_debug_commands():
    """Gera comandos para debug"""
    print("\n🔧 COMANDOS DE DEBUG")
    print("-" * 40)
    
    commands = [
        "# Verificar se migrations foram aplicadas",
        "python3.10 manage.py showmigrations --settings=setup.production_settings",
        "",
        "# Aplicar migrations se necessário",
        "python3.10 manage.py migrate --settings=setup.production_settings",
        "",
        "# Verificar dados no banco",
        "python3.10 manage.py shell --settings=setup.production_settings",
        "# Dentro do shell:",
        "# from artigos.models import Artigo",
        "# print(Artigo.objects.all())",
        "",
        "# Testar servidor localmente (se possível)",
        "python3.10 manage.py runserver 8000 --settings=setup.production_settings",
        "",
        "# Ver logs detalhados",
        "tail -f /home/prismaav/logs/*.error.log"
    ]
    
    for cmd in commands:
        print(cmd)

def main():
    """Executa diagnóstico completo do erro 500"""
    print("🚨 DIAGNÓSTICO ESPECÍFICO - ERRO 500 BLOG")
    print("=" * 50)
    
    if not Path('manage.py').exists():
        print("❌ Execute no diretório raiz do projeto Django!")
        sys.exit(1)
    
    # Lista de testes
    tests = [
        ("Importação Django", test_django_import),
        ("Apps Django", test_apps),
        ("Modelos", test_models),
        ("URLs", test_urls),
        ("Templates", test_templates),
        ("Arquivos Estáticos", test_static_files),
        ("Banco de Dados", test_database),
        ("View Blog", test_view_blog)
    ]
    
    failed_tests = []
    for name, test_func in tests:
        print(f"\n{'='*20} {name} {'='*20}")
        try:
            if not test_func():
                failed_tests.append(name)
        except Exception as e:
            print(f"❌ ERRO CRÍTICO em {name}: {e}")
            failed_tests.append(name)
    
    # Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DO DIAGNÓSTICO")
    print("=" * 50)
    
    if failed_tests:
        print("❌ PROBLEMAS ENCONTRADOS:")
        for test in failed_tests:
            print(f"   - {test}")
        print("\n💡 Execute os comandos de debug abaixo:")
        generate_debug_commands()
    else:
        print("✅ TODOS OS TESTES PASSARAM!")
        print("💡 O problema pode estar na configuração do PythonAnywhere:")
        print("   - Verifique WSGI file")
        print("   - Verifique Error log")
        print("   - Verifique se reload foi feito")

if __name__ == '__main__':
    main()
