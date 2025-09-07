#!/usr/bin/env python3
"""
Script para migração completa do Sistema SEO para Produção
Prisma Avaliações Imobiliárias

Este script deve ser executado no servidor de produção para:
1. Verificar se o app SEO existe
2. Aplicar as migrações
3. Verificar se a configuração está correta
4. Criar configuração inicial se necessário
"""

import os
import sys
import django
from pathlib import Path

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings_production')

# Adicionar o caminho do projeto
PROJECT_ROOT = Path('/var/www/prisma_avaliacoes')
sys.path.insert(0, str(PROJECT_ROOT))

# Configurar Django
django.setup()

from django.core.management import call_command
from django.db import connection
from django.apps import apps

def main():
    print("=" * 80)
    print("🚀 MIGRAÇÃO DO SISTEMA SEO PARA PRODUÇÃO")
    print("=" * 80)
    
    # 1. Verificar se o app SEO está instalado
    print("\n1️⃣ Verificando instalação do app SEO...")
    try:
        seo_app = apps.get_app_config('seo')
        print(f"✅ App SEO encontrado: {seo_app.name}")
    except:
        print("❌ App SEO NÃO ENCONTRADO!")
        print("   O app 'seo' deve estar em INSTALLED_APPS")
        return False
    
    # 2. Verificar estrutura de arquivos
    print("\n2️⃣ Verificando estrutura de arquivos...")
    seo_files_required = [
        'seo/models.py',
        'seo/admin.py', 
        'seo/apps.py',
        'seo/views.py',
        'seo/urls.py',
        'seo/templatetags/seo_tags.py',
        'seo/migrations/0001_initial.py',
    ]
    
    missing_files = []
    for file_path in seo_files_required:
        full_path = PROJECT_ROOT / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - ARQUIVO FALTANDO!")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️ {len(missing_files)} arquivos faltando!")
        print("Execute 'git pull' para sincronizar os arquivos.")
        return False
    
    # 3. Aplicar migrações
    print("\n3️⃣ Aplicando migrações do SEO...")
    try:
        call_command('migrate', 'seo', verbosity=2)
        print("✅ Migrações aplicadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao aplicar migrações: {e}")
        return False
    
    # 4. Verificar se as tabelas foram criadas
    print("\n4️⃣ Verificando tabelas do banco...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'seo_%'")
            tables = cursor.fetchall()
            
        if tables:
            print("✅ Tabelas SEO criadas:")
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print("❌ Nenhuma tabela SEO encontrada!")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar tabelas: {e}")
        return False
    
    # 5. Testar importação dos models
    print("\n5️⃣ Testando models do SEO...")
    try:
        from seo.models import SEOMeta, SEOConfig
        
        # Contar registros
        meta_count = SEOMeta.objects.count()
        config_count = SEOConfig.objects.count()
        
        print(f"✅ SEOMeta: {meta_count} registros")
        print(f"✅ SEOConfig: {config_count} registros")
        
        # Criar configuração inicial se não existir
        if config_count == 0:
            print("\n6️⃣ Criando configuração inicial...")
            config = SEOConfig.objects.create(
                site_name='Prisma Avaliações Imobiliárias',
                site_domain='prismaavaliacoes.com.br',
                site_description='Avaliações imobiliárias profissionais e consultoria especializada em Minas Gerais',
                default_keywords='avaliação imobiliária, laudo de avaliação, perícia imobiliária, consultoria imobiliária, Belo Horizonte, Minas Gerais'
            )
            print("✅ Configuração inicial criada!")
        
    except Exception as e:
        print(f"❌ Erro ao testar models: {e}")
        return False
    
    # 6. Verificar admin
    print("\n7️⃣ Testando admin do SEO...")
    try:
        from django.contrib import admin
        from seo.admin import SEOMetaAdmin, SEOConfigAdmin
        
        # Verificar se estão registrados
        if SEOMeta in admin.site._registry:
            print("✅ SEOMetaAdmin registrado")
        else:
            print("❌ SEOMetaAdmin NÃO registrado")
            
        if SEOConfig in admin.site._registry:
            print("✅ SEOConfigAdmin registrado")
        else:
            print("❌ SEOConfigAdmin NÃO registrado")
            
    except Exception as e:
        print(f"❌ Erro ao verificar admin: {e}")
        return False
    
    # 7. Coletar arquivos estáticos
    print("\n8️⃣ Coletando arquivos estáticos...")
    try:
        call_command('collectstatic', '--noinput', verbosity=1)
        print("✅ Arquivos estáticos coletados!")
    except Exception as e:
        print(f"⚠️ Aviso ao coletar estáticos: {e}")
    
    print("\n" + "=" * 80)
    print("🎉 MIGRAÇÃO DO SEO CONCLUÍDA COM SUCESSO!")
    print("=" * 80)
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Reiniciar o Gunicorn: sudo systemctl restart gunicorn")
    print("2. Verificar logs: sudo tail -f /var/log/gunicorn/gunicorn.log")
    print("3. Acessar admin: https://prismaavaliacoes.com.br/admin/")
    print("4. Procurar seção 'SEO' no menu do admin")
    print("\n✅ Sistema SEO pronto para uso em produção!")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
