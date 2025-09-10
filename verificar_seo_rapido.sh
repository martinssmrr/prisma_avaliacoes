#!/bin/bash

# VERIFICAÇÃO RÁPIDA - STATUS SEO ADMIN
# Verifica rapidamente o status do admin SEO

echo "🔍 VERIFICAÇÃO RÁPIDA - SEO ADMIN"
echo "================================="

SERVER_PATH="/var/www/html/prismaavaliacoes.com.br"
cd "$SERVER_PATH"
source venv/bin/activate

echo "📊 Status dos serviços:"
echo "Nginx: $(systemctl is-active nginx)"
echo "Gunicorn: $(systemctl is-active gunicorn)"
echo ""

echo "🌐 Teste de conectividade:"
MAIN_SITE=$(curl -s -o /dev/null -w "%{http_code}" https://prismaavaliacoes.com.br/)
ADMIN_MAIN=$(curl -s -o /dev/null -w "%{http_code}" https://prismaavaliacoes.com.br/admin/)
ADMIN_SEO=$(curl -s -o /dev/null -w "%{http_code}" https://prismaavaliacoes.com.br/admin/seo/)

echo "Site principal: $MAIN_SITE"
echo "Admin principal: $ADMIN_MAIN"
echo "Admin SEO: $ADMIN_SEO"
echo ""

echo "🧪 Verificação Django:"
python manage.py shell --settings=setup.settings -c "
from django.apps import apps
apps_list = [app.name for app in apps.get_app_configs()]
print('SEO carregado:', 'seo' in apps_list)

try:
    from seo.models import SEOMeta, SEOConfig
    print('Modelos SEO: OK')
except Exception as e:
    print('Modelos SEO: ERRO -', e)

try:
    from django.contrib import admin
    from seo.models import SEOMeta, SEOConfig
    registered = SEOMeta in admin.site._registry and SEOConfig in admin.site._registry
    print('Admin registrado:', registered)
except Exception as e:
    print('Admin SEO: ERRO -', e)
"

echo ""
if [ "$ADMIN_SEO" = "302" ] || [ "$ADMIN_SEO" = "200" ]; then
    echo "✅ Admin SEO está funcionando!"
else
    echo "❌ Admin SEO com problema - Execute correção:"
    echo "   ./corrigir_seo_404.sh"
fi
