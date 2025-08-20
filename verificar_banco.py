#!/usr/bin/env python
"""
Script para verificar e configurar banco de dados
Execute: python verificar_banco.py
"""

import os
import django
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line
from django.conf import settings
from decouple import config

def verificar_configuracao_banco():
    """Verifica a configuração atual do banco de dados"""
    
    print("🗄️ Verificação do Banco de Dados - Prisma Avaliações")
    print("=" * 55)
    
    # Informações da configuração
    db_config = settings.DATABASES['default']
    
    print("📋 Configuração Atual:")
    print(f"  Engine: {db_config['ENGINE']}")
    print(f"  Nome: {db_config['NAME']}")
    
    if db_config['USER']:
        print(f"  Usuário: {db_config['USER']}")
    if db_config['HOST']:
        print(f"  Host: {db_config['HOST']}")
    if db_config['PORT']:
        print(f"  Porta: {db_config['PORT']}")
    
    # Verificar tipo de banco
    engine = db_config['ENGINE']
    if 'sqlite3' in engine:
        print("\n🔧 Tipo: SQLite (Desenvolvimento)")
        verificar_sqlite()
    elif 'postgresql' in engine:
        print("\n🔧 Tipo: PostgreSQL (Produção)")
        verificar_postgresql()
    elif 'mysql' in engine:
        print("\n🔧 Tipo: MySQL/MariaDB (Produção)")
        verificar_mysql()

def verificar_sqlite():
    """Verifica configuração específica do SQLite"""
    
    db_path = settings.DATABASES['default']['NAME']
    
    # Verificar se arquivo existe
    if os.path.exists(db_path):
        size = os.path.getsize(db_path)
        print(f"✅ Arquivo do banco existe: {db_path}")
        print(f"📊 Tamanho: {size:,} bytes ({size/1024:.1f} KB)")
    else:
        print(f"⚠️  Arquivo do banco não existe: {db_path}")
        print("💡 Execute: python manage.py migrate")
    
    # Verificar .gitignore
    gitignore_path = Path('.gitignore')
    if gitignore_path.exists():
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if '*.sqlite3' in content or 'db.sqlite3' in content:
                print("✅ SQLite está no .gitignore")
            else:
                print("⚠️  SQLite não está no .gitignore!")
    
def verificar_postgresql():
    """Verifica configuração específica do PostgreSQL"""
    
    try:
        import psycopg2
        print("✅ Driver psycopg2 instalado")
    except ImportError:
        print("❌ Driver psycopg2 não instalado")
        print("💡 Execute: pip install psycopg2-binary")
        return
    
    # Testar conexão
    testar_conexao_banco()

def verificar_mysql():
    """Verifica configuração específica do MySQL"""
    
    try:
        import MySQLdb
        print("✅ Driver MySQLdb instalado")
    except ImportError:
        try:
            import pymysql
            print("✅ Driver PyMySQL instalado")
        except ImportError:
            print("❌ Driver MySQL não instalado")
            print("💡 Execute: pip install mysqlclient")
            return
    
    # Testar conexão
    testar_conexao_banco()

def testar_conexao_banco():
    """Testa a conexão com o banco de dados"""
    
    try:
        print("\n🔌 Testando conexão...")
        
        # Testar conexão
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
        print("✅ Conexão com banco estabelecida com sucesso!")
        
        # Verificar tabelas
        verificar_tabelas()
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        print("💡 Verifique as configurações no arquivo .env")

def verificar_tabelas():
    """Verifica tabelas existentes no banco"""
    
    try:
        from django.db import connection
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
            """)
            tables = cursor.fetchall()
        
        if tables:
            print(f"\n📋 Tabelas encontradas ({len(tables)}):")
            for table in tables:
                print(f"  • {table[0]}")
        else:
            print("\n⚠️  Nenhuma tabela encontrada")
            print("💡 Execute: python manage.py migrate")
            
    except Exception as e:
        print(f"\n⚠️  Erro ao verificar tabelas: {e}")

def verificar_migrações():
    """Verifica status das migrações"""
    
    print("\n🔄 Verificando migrações...")
    
    try:
        from django.core.management import call_command
        from io import StringIO
        
        # Capturar output do showmigrations
        output = StringIO()
        call_command('showmigrations', stdout=output)
        result = output.getvalue()
        
        if '[X]' in result:
            applied = result.count('[X]')
            total_lines = len([line for line in result.split('\n') if '[' in line])
            print(f"✅ Migrações aplicadas: {applied}/{total_lines}")
        
        if '[ ]' in result:
            pending = result.count('[ ]')
            print(f"⚠️  Migrações pendentes: {pending}")
            print("💡 Execute: python manage.py migrate")
        else:
            print("✅ Todas as migrações estão aplicadas")
            
    except Exception as e:
        print(f"❌ Erro ao verificar migrações: {e}")

def verificar_variaveis_env():
    """Verifica variáveis de ambiente relacionadas ao banco"""
    
    print("\n🔧 Variáveis de Ambiente:")
    
    env_vars = [
        'DB_ENGINE',
        'DB_NAME', 
        'DB_USER',
        'DB_PASSWORD',
        'DB_HOST',
        'DB_PORT'
    ]
    
    for var in env_vars:
        value = config(var, default='')
        if value:
            if 'PASSWORD' in var:
                print(f"  {var}: {'*' * len(value)}")
            else:
                print(f"  {var}: {value}")
        else:
            print(f"  {var}: (não definido)")

def gerar_relatorio():
    """Gera relatório completo do banco"""
    
    print("\n" + "=" * 55)
    print("📊 RELATÓRIO FINAL")
    print("=" * 55)
    
    # Status geral
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Banco de dados: FUNCIONANDO")
    except:
        print("❌ Banco de dados: COM PROBLEMAS")
    
    # Verificar arquivo .env
    if os.path.exists('.env'):
        print("✅ Arquivo .env: EXISTE")
    else:
        print("❌ Arquivo .env: NÃO ENCONTRADO")
    
    # Verificar .gitignore
    if os.path.exists('.gitignore'):
        print("✅ Arquivo .gitignore: EXISTE")
    else:
        print("❌ Arquivo .gitignore: NÃO ENCONTRADO")
    
    print("\n💡 Para mais informações, consulte CONFIGURACAO_BANCO.md")

def main():
    verificar_configuracao_banco()
    verificar_variaveis_env()
    verificar_migrações()
    gerar_relatorio()

if __name__ == '__main__':
    main()
