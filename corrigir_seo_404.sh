#!/bin/bash

# DIAGNÓSTICO E CORREÇÃO - SEO 404 NO ADMIN
# Identifica e corrige o problema do admin SEO retornando 404

echo "🔍 DIAGNÓSTICO SEO 404 - PRISMA AVALIAÇÕES"
echo "=========================================="
echo "Data: $(date)"
echo "URL com erro: https://prismaavaliacoes.com.br/admin/seo/"
echo ""

# Configurações
SERVER_PATH="/var/www/html/prismaavaliacoes.com.br"

cd "$SERVER_PATH"
source venv/bin/activate

echo "📊 1. VERIFICAÇÃO INICIAL..."
echo "Diretório atual: $(pwd)"
echo "Python: $(which python)"
echo "Django: $(python -c 'import django; print(django.get_version())')"
echo ""

echo "🧪 2. DIAGNÓSTICO COMPLETO DO APP SEO..."
python manage.py shell --settings=setup.settings << 'EOF'
import os
import sys
from django.apps import apps
from django.conf import settings
from django.contrib import admin

print("=== DIAGNÓSTICO SEO ADMIN ===")
print(f"Django version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print()

# 1. Verificar INSTALLED_APPS
print("1. INSTALLED_APPS:")
for i, app in enumerate(settings.INSTALLED_APPS, 1):
    marker = "✅" if "seo" in app.lower() else "  "
    print(f"  {i:2d}. {marker} {app}")

seo_in_installed = 'seo' in settings.INSTALLED_APPS
print(f"\nSEO em INSTALLED_APPS: {'✅ SIM' if seo_in_installed else '❌ NÃO'}")
print()

# 2. Verificar apps carregados
print("2. APPS CARREGADOS:")
loaded_apps = [app.name for app in apps.get_app_configs()]
for app in loaded_apps:
    marker = "✅" if "seo" in app.lower() else "  "
    print(f"  {marker} {app}")

seo_loaded = 'seo' in loaded_apps
print(f"\nSEO carregado: {'✅ SIM' if seo_loaded else '❌ NÃO'}")
print()

# 3. Verificar estrutura de arquivos SEO
print("3. ESTRUTURA DE ARQUIVOS SEO:")
import os
if os.path.exists('seo'):
    print("  ✅ Diretório seo/ existe")
    
    files_to_check = [
        '__init__.py',
        'models.py', 
        'admin.py',
        'apps.py',
        'migrations/__init__.py'
    ]
    
    for file in files_to_check:
        path = f'seo/{file}'
        exists = os.path.exists(path)
        marker = "✅" if exists else "❌"
        print(f"  {marker} {path}")
        
    # Verificar conteúdo do admin.py
    admin_path = 'seo/admin.py'
    if os.path.exists(admin_path):
        with open(admin_path, 'r') as f:
            content = f.read()
            has_register = '@admin.register' in content or 'admin.site.register' in content
            print(f"  {'✅' if has_register else '❌'} admin.py tem registros de admin")
    
else:
    print("  ❌ Diretório seo/ NÃO existe")
print()

# 4. Verificar se modelos SEO existem
print("4. MODELOS SEO:")
try:
    from seo.models import SEOMeta, SEOConfig
    print("  ✅ Modelos importados com sucesso")
    
    try:
        meta_count = SEOMeta.objects.count()
        config_count = SEOConfig.objects.count()
        print(f"  ✅ SEOMeta: {meta_count} registros")
        print(f"  ✅ SEOConfig: {config_count} registros")
    except Exception as e:
        print(f"  ⚠️  Erro ao contar registros: {e}")
        
except ImportError as e:
    print(f"  ❌ Erro ao importar modelos: {e}")
print()

# 5. Verificar admin SEO
print("5. ADMIN SEO:")
try:
    from seo.admin import SEOMetaAdmin, SEOConfigAdmin
    print("  ✅ Classes admin importadas")
    
    # Verificar se estão registradas
    from seo.models import SEOMeta, SEOConfig
    
    seo_meta_registered = SEOMeta in admin.site._registry
    seo_config_registered = SEOConfig in admin.site._registry
    
    print(f"  {'✅' if seo_meta_registered else '❌'} SEOMeta registrado no admin")
    print(f"  {'✅' if seo_config_registered else '❌'} SEOConfig registrado no admin")
    
except ImportError as e:
    print(f"  ❌ Erro ao importar admin: {e}")
print()

# 6. Verificar modelos registrados no admin
print("6. TODOS OS MODELOS NO ADMIN:")
registered_models = list(admin.site._registry.keys())
for model in registered_models:
    app_label = model._meta.app_label
    model_name = model.__name__
    marker = "🎯" if app_label == 'seo' else "  "
    print(f"  {marker} {app_label}.{model_name}")

print(f"\nTotal de modelos registrados: {len(registered_models)}")
print()

# 7. Verificar URLs do admin
print("7. URLS ADMIN:")
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

admin_urls = [
    'admin:index',
    'admin:seo_seometa_changelist',
    'admin:seo_seoconfig_changelist'
]

for url_name in admin_urls:
    try:
        url = reverse(url_name)
        print(f"  ✅ {url_name} -> {url}")
    except NoReverseMatch:
        print(f"  ❌ {url_name} -> NÃO ENCONTRADA")

print()
print("=== RESUMO DO DIAGNÓSTICO ===")
print(f"SEO em INSTALLED_APPS: {'✅' if seo_in_installed else '❌'}")
print(f"SEO carregado: {'✅' if seo_loaded else '❌'}")

try:
    from seo.models import SEOMeta, SEOConfig
    models_ok = True
except:
    models_ok = False
print(f"Modelos SEO: {'✅' if models_ok else '❌'}")

try:
    from seo.admin import SEOMetaAdmin, SEOConfigAdmin
    admin_ok = True
except:
    admin_ok = False
print(f"Admin SEO: {'✅' if admin_ok else '❌'}")

if seo_in_installed and seo_loaded and models_ok and admin_ok:
    print("\n🎉 DIAGNÓSTICO: Configuração parece OK")
    print("🔧 POSSÍVEL CAUSA: Cache ou reload necessário")
else:
    print("\n⚠️  DIAGNÓSTICO: Problemas encontrados")
    print("🔧 CORREÇÃO: Aplicar fixes necessários")

print("\n=== FIM DO DIAGNÓSTICO ===")
EOF

echo ""
echo "🔧 3. APLICANDO CORREÇÕES AUTOMÁTICAS..."

# Verificar se SEO está em INSTALLED_APPS
echo "Verificando INSTALLED_APPS..."
if grep -q "seo" setup/settings.py; then
    echo "✅ SEO encontrado em INSTALLED_APPS"
else
    echo "❌ SEO não encontrado em INSTALLED_APPS"
    echo "🔧 Adicionando SEO ao INSTALLED_APPS..."
    
    # Backup do settings
    cp setup/settings.py setup/settings.py.backup
    
    # Adicionar SEO se não estiver presente
    sed -i "/INSTALLED_APPS = \[/,/\]/ {
        /\]/i\    'seo',
    }" setup/settings.py
    
    echo "✅ SEO adicionado ao INSTALLED_APPS"
fi

echo ""
echo "🔄 4. APLICANDO MIGRAÇÕES..."
python manage.py makemigrations seo --settings=setup.settings
python manage.py migrate --settings=setup.settings

echo ""
echo "📁 5. COLETANDO ARQUIVOS ESTÁTICOS..."
python manage.py collectstatic --noinput --settings=setup.settings

echo ""
echo "🔄 6. REINICIANDO SERVIÇOS..."
systemctl restart gunicorn
systemctl reload nginx

echo ""
echo "🧪 7. VERIFICAÇÃO PÓS-CORREÇÃO..."
sleep 3

# Testar se admin SEO está acessível
ADMIN_SEO_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://prismaavaliacoes.com.br/admin/seo/)
echo "Status admin SEO: $ADMIN_SEO_STATUS"

if [ "$ADMIN_SEO_STATUS" = "302" ] || [ "$ADMIN_SEO_STATUS" = "200" ]; then
    echo "✅ Admin SEO funcionando!"
else
    echo "❌ Admin SEO ainda com problemas (Status: $ADMIN_SEO_STATUS)"
fi

echo ""
echo "🎉 CORREÇÃO SEO 404 CONCLUÍDA!"
echo "=========================================="
echo "🌐 TESTE AS URLS:"
echo "  https://prismaavaliacoes.com.br/admin/"
echo "  https://prismaavaliacoes.com.br/admin/seo/"
echo "  https://prismaavaliacoes.com.br/admin/seo/seometa/"
echo "  https://prismaavaliacoes.com.br/admin/seo/seoconfig/"
echo ""
echo "📋 O QUE DEVE APARECER:"
echo "  ✅ Seção 'SEO' no menu admin"
echo "  ✅ Subseções 'SEO metas' e 'SEO configs'"
echo "  ✅ Formulários de configuração SEO"
echo ""
echo "Se ainda houver problemas, verificar logs:"
echo "  tail -f /var/log/gunicorn/error.log"
