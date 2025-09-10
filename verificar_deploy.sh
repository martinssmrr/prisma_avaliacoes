#!/bin/bash

# SCRIPT DE VERIFICAÇÃO PÓS-DEPLOY
# Verifica se todas as funcionalidades estão operacionais

echo "🔍 VERIFICAÇÃO PÓS-DEPLOY - PRISMA AVALIAÇÕES"
echo "=============================================="
echo "Data: $(date)"
echo ""

# Configurações
DOMAIN="prismaavaliacoes.com.br"
SERVER_PATH="/var/www/html/prismaavaliacoes.com.br"

cd "$SERVER_PATH"
source venv/bin/activate

echo "📊 1. VERIFICAÇÃO DOS SERVIÇOS..."
echo "Nginx: $(systemctl is-active nginx)"
echo "Gunicorn: $(systemctl is-active gunicorn)"
echo ""

echo "🧪 2. TESTE DE CONFIGURAÇÃO DJANGO..."
python manage.py check --settings=setup.settings
echo ""

echo "🔗 3. TESTE DE CONECTIVIDADE..."
# Teste local
LOCAL_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/)
echo "Localhost (8000): $LOCAL_STATUS"

# Teste domínio
DOMAIN_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://$DOMAIN/)
echo "Domínio HTTPS: $DOMAIN_STATUS"
echo ""

echo "🎯 4. VERIFICAÇÃO SEO..."
python manage.py shell --settings=setup.settings << 'EOF'
from django.contrib.sites.models import Site
from seo.models import SEOConfig, SEOMeta

print("=== VERIFICAÇÃO SEO ===")

# Verificar Sites Framework
try:
    site = Site.objects.get(pk=1)
    print(f"✅ Site: {site.domain}")
    if site.domain == 'prismaavaliacoes.com.br':
        print("✅ Domínio correto configurado")
    else:
        print(f"⚠️  Domínio incorreto: {site.domain}")
except Exception as e:
    print(f"❌ Erro Sites: {e}")

# Verificar SEO Config
try:
    config = SEOConfig.objects.get(pk=1)
    print(f"✅ SEO Config: {config.site_name}")
    print(f"✅ Domínio SEO: {config.domain}")
except SEOConfig.DoesNotExist:
    print("❌ SEOConfig não encontrado")
except Exception as e:
    print(f"❌ Erro SEOConfig: {e}")

# Verificar tabelas SEO
print(f"SEOMeta registros: {SEOMeta.objects.count()}")
print(f"SEOConfig registros: {SEOConfig.objects.count()}")

print("=== VERIFICAÇÃO CONCLUÍDA ===")
EOF

echo ""
echo "📁 5. VERIFICAÇÃO DE ARQUIVOS ESTÁTICOS..."
if [ -d "staticfiles" ]; then
    echo "✅ Diretório staticfiles existe"
    echo "CSS files: $(find staticfiles -name "*.css" | wc -l)"
    echo "JS files: $(find staticfiles -name "*.js" | wc -l)"
    echo "IMG files: $(find staticfiles -name "*.png" -o -name "*.jpg" -o -name "*.gif" | wc -l)"
else
    echo "❌ Diretório staticfiles não encontrado"
fi
echo ""

echo "🗺️  6. TESTE DO SITEMAP..."
SITEMAP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://$DOMAIN/sitemap.xml)
echo "Sitemap status: $SITEMAP_STATUS"
if [ "$SITEMAP_STATUS" = "200" ]; then
    echo "✅ Sitemap acessível"
    # Verificar se contém domínio correto
    SITEMAP_CONTENT=$(curl -s https://$DOMAIN/sitemap.xml | grep -c "prismaavaliacoes.com.br")
    if [ "$SITEMAP_CONTENT" -gt 0 ]; then
        echo "✅ Sitemap contém domínio correto"
    else
        echo "⚠️  Sitemap pode conter domínio incorreto"
    fi
else
    echo "❌ Problema no sitemap"
fi
echo ""

echo "🔗 7. TESTE DAS CANONICAL TAGS..."
HOME_CANONICAL=$(curl -s https://$DOMAIN/ | grep -c 'rel="canonical"')
if [ "$HOME_CANONICAL" -gt 0 ]; then
    echo "✅ Canonical tags encontradas na página inicial"
else
    echo "⚠️  Canonical tags não encontradas"
fi
echo ""

echo "🎨 8. VERIFICAÇÃO DOS ESTILOS CSS..."
ADMIN_CSS=$(curl -s https://$DOMAIN/static/css/admin_custom.css | grep -c "#1e40af")
STYLE_CSS=$(curl -s https://$DOMAIN/static/css/style.css | grep -c "#1e40af")
echo "Admin CSS (cor #1e40af): $ADMIN_CSS ocorrências"
echo "Style CSS (cor #1e40af): $STYLE_CSS ocorrências"
echo ""

echo "🔧 9. TESTE DO ADMIN..."
ADMIN_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://$DOMAIN/admin/)
echo "Admin status: $ADMIN_STATUS"

ADMIN_SEO_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://$DOMAIN/admin/seo/)
echo "Admin SEO status: $ADMIN_SEO_STATUS"
echo ""

echo "📋 10. RESUMO DA VERIFICAÇÃO..."
echo "=============================================="

if systemctl is-active --quiet nginx && systemctl is-active --quiet gunicorn; then
    echo "✅ Serviços: OK"
else
    echo "❌ Serviços: PROBLEMA"
fi

if [ "$DOMAIN_STATUS" = "200" ] || [ "$DOMAIN_STATUS" = "301" ] || [ "$DOMAIN_STATUS" = "302" ]; then
    echo "✅ Site: FUNCIONANDO"
else
    echo "❌ Site: PROBLEMA ($DOMAIN_STATUS)"
fi

if [ "$ADMIN_STATUS" = "200" ] || [ "$ADMIN_STATUS" = "302" ]; then
    echo "✅ Admin: FUNCIONANDO"
else
    echo "❌ Admin: PROBLEMA ($ADMIN_STATUS)"
fi

if [ "$ADMIN_SEO_STATUS" = "200" ] || [ "$ADMIN_SEO_STATUS" = "302" ]; then
    echo "✅ Admin SEO: FUNCIONANDO"
else
    echo "❌ Admin SEO: PROBLEMA ($ADMIN_SEO_STATUS)"
fi

if [ "$SITEMAP_STATUS" = "200" ]; then
    echo "✅ Sitemap: FUNCIONANDO"
else
    echo "❌ Sitemap: PROBLEMA"
fi

echo ""
echo "🌐 URLS PARA TESTE MANUAL:"
echo "https://$DOMAIN/"
echo "https://$DOMAIN/admin/"
echo "https://$DOMAIN/admin/seo/"
echo "https://$DOMAIN/admin/seo/seoconfig/"
echo "https://$DOMAIN/sitemap.xml"
echo ""
echo "✅ Verificação concluída!"
