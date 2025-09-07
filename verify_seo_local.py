#!/usr/bin/env python3
"""
Script de Verificação Local do Sistema SEO
Prisma Avaliações Imobiliárias

Este script verifica se o sistema SEO está completo e pronto para deploy
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description=""):
    """Verifica se um arquivo existe"""
    if Path(file_path).exists():
        print(f"✅ {file_path} {description}")
        return True
    else:
        print(f"❌ {file_path} {description} - FALTANDO!")
        return False

def main():
    print("=" * 80)
    print("🔍 VERIFICAÇÃO LOCAL DO SISTEMA SEO")
    print("=" * 80)
    
    base_dir = Path(__file__).parent
    missing_files = []
    
    # 1. Verificar estrutura do app SEO
    print("\n1️⃣ Verificando estrutura do app SEO...")
    
    seo_files = {
        'seo/__init__.py': 'Inicializador do app',
        'seo/models.py': 'Models SEOMeta e SEOConfig',
        'seo/admin.py': 'Interface admin',
        'seo/apps.py': 'Configuração do app',
        'seo/views.py': 'Views do SEO',
        'seo/urls.py': 'URLs do SEO',
        'seo/signals.py': 'Sinais Django',
        'seo/context_processors.py': 'Processadores de contexto',
        'seo/sitemaps.py': 'Geração de sitemaps',
        'seo/templatetags/__init__.py': 'Inicializador template tags',
        'seo/templatetags/seo_tags.py': 'Template tags do SEO',
        'seo/templates/seo/seo_head.html': 'Template principal SEO',
        'seo/templates/seo/json_ld.html': 'Template JSON-LD',
        'seo/migrations/__init__.py': 'Inicializador migrações',
        'seo/migrations/0001_initial.py': 'Migração inicial',
        'seo/management/__init__.py': 'Inicializador comandos',
        'seo/management/commands/__init__.py': 'Inicializador comandos',
    }
    
    for file_path, description in seo_files.items():
        full_path = base_dir / file_path
        if not check_file_exists(full_path, f"- {description}"):
            missing_files.append(file_path)
    
    # 2. Verificar configurações
    print("\n2️⃣ Verificando arquivos de configuração...")
    
    config_files = {
        'setup/settings.py': 'Settings desenvolvimento',
        'setup/settings_production.py': 'Settings produção',
        'setup/urls.py': 'URLs principais',
        'manage.py': 'Script de gerenciamento',
    }
    
    for file_path, description in config_files.items():
        full_path = base_dir / file_path
        if not check_file_exists(full_path, f"- {description}"):
            missing_files.append(file_path)
    
    # 3. Verificar se SEO está nos settings
    print("\n3️⃣ Verificando configuração nos settings...")
    
    try:
        # Verificar settings.py
        settings_path = base_dir / 'setup/settings.py'
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings_content = f.read()
            
        if '"seo"' in settings_content or "'seo'" in settings_content:
            print("✅ App 'seo' encontrado em INSTALLED_APPS (settings.py)")
        else:
            print("❌ App 'seo' NÃO encontrado em INSTALLED_APPS (settings.py)")
            missing_files.append("seo app in settings.py")
            
        # Verificar settings_production.py  
        settings_prod_path = base_dir / 'setup/settings_production.py'
        with open(settings_prod_path, 'r', encoding='utf-8') as f:
            settings_prod_content = f.read()
            
        if '"seo"' in settings_prod_content or "'seo'" in settings_prod_content:
            print("✅ App 'seo' encontrado em INSTALLED_APPS (settings_production.py)")
        else:
            print("❌ App 'seo' NÃO encontrado em INSTALLED_APPS (settings_production.py)")
            missing_files.append("seo app in settings_production.py")
            
    except Exception as e:
        print(f"❌ Erro ao verificar settings: {e}")
        missing_files.append("settings verification")
    
    # 4. Verificar se existem arquivos template tags
    print("\n4️⃣ Verificando template tags...")
    
    seo_tags_path = base_dir / 'seo/templatetags/seo_tags.py'
    if seo_tags_path.exists():
        try:
            with open(seo_tags_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            required_tags = ['render_seo_meta', 'get_seo_config', 'render_json_ld']
            for tag in required_tags:
                if tag in content:
                    print(f"✅ Template tag '{tag}' encontrada")
                else:
                    print(f"❌ Template tag '{tag}' NÃO encontrada")
                    missing_files.append(f"template tag {tag}")
                    
        except Exception as e:
            print(f"❌ Erro ao verificar template tags: {e}")
    
    # 5. Verificar estrutura de templates
    print("\n5️⃣ Verificando templates...")
    
    template_files = [
        'seo/templates/seo/seo_head.html',
        'seo/templates/seo/json_ld.html',
    ]
    
    for template in template_files:
        full_path = base_dir / template
        if not check_file_exists(full_path, "- Template SEO"):
            missing_files.append(template)
    
    # 6. Verificar se as migrações estão corretas
    print("\n6️⃣ Verificando migrações...")
    
    migration_path = base_dir / 'seo/migrations/0001_initial.py'
    if migration_path.exists():
        try:
            with open(migration_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            required_models = ['SEOConfig', 'SEOMeta']
            for model in required_models:
                if model in content:
                    print(f"✅ Model '{model}' encontrado na migração")
                else:
                    print(f"❌ Model '{model}' NÃO encontrado na migração")
                    missing_files.append(f"migration {model}")
                    
        except Exception as e:
            print(f"❌ Erro ao verificar migração: {e}")
    
    # 7. Resumo
    print("\n" + "=" * 80)
    
    if missing_files:
        print(f"❌ VERIFICAÇÃO FALHOU - {len(missing_files)} problemas encontrados:")
        for item in missing_files:
            print(f"   - {item}")
        print("\n🔧 CORRIJA OS PROBLEMAS ANTES DE FAZER O DEPLOY!")
        return False
    else:
        print("✅ VERIFICAÇÃO PASSOU - Sistema SEO está completo!")
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Fazer commit dos arquivos: git add . && git commit -m 'Sistema SEO completo'")
        print("2. Fazer push: git push origin main")
        print("3. No servidor: git pull")
        print("4. No servidor: python3 migrate_seo_to_production.py")
        print("5. Reiniciar serviços")
        return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
