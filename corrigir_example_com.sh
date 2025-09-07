#!/bin/bash
# Script URGENTE para corrigir URLs do sitemap com example.com

echo "🚨 CORREÇÃO URGENTE: URLs com example.com no sitemap"
echo "=================================================="

cd /var/www/prisma_avaliacoes || exit 1

echo "📍 Situação atual do sitemap:"
curl -s https://prismaavaliacoes.com.br/sitemap.xml | grep -o "https://[^<]*" | head -5

echo ""
echo "🔧 Aplicando correção IMEDIATA..."

# 1. Backup atual
cp setup/urls.py setup/urls.py.backup.emergency

# 2. Verificar se existe configuração SEO
echo "🔍 Verificando configuração SEO..."
python3 manage.py shell --settings=setup.settings_production << 'EOF'
from seo.models import SEOConfig

# Verificar se existe configuração
config = SEOConfig.objects.first()
if config:
    print(f"Configuração encontrada: {config.site_domain}")
    if config.site_domain != 'prismaavaliacoes.com.br':
        print("Corrigindo domínio...")
        config.site_domain = 'prismaavaliacoes.com.br'
        config.save()
        print("✅ Domínio corrigido")
    else:
        print("✅ Domínio já está correto")
else:
    print("Criando configuração SEO...")
    SEOConfig.objects.create(
        site_name='Prisma Avaliações Imobiliárias',
        site_domain='prismaavaliacoes.com.br',
        site_description='Avaliações imobiliárias profissionais em Minas Gerais',
        default_keywords='avaliação imobiliária, perícia imobiliária, consultoria'
    )
    print("✅ Configuração SEO criada")
EOF

# 3. Verificar se Sites framework está configurado
echo "🔍 Verificando Sites framework..."
python3 manage.py shell --settings=setup.settings_production << 'EOF'
from django.contrib.sites.models import Site

# Verificar site atual
site = Site.objects.get_current()
print(f"Site atual: {site.domain}")

if site.domain != 'prismaavaliacoes.com.br':
    print("Corrigindo site domain...")
    site.domain = 'prismaavaliacoes.com.br'
    site.name = 'Prisma Avaliações Imobiliárias'
    site.save()
    print("✅ Site domain corrigido")
else:
    print("✅ Site domain já está correto")
EOF

# 4. Limpar cache se existir
echo "🧹 Limpando cache..."
python3 manage.py shell --settings=setup.settings_production << 'EOF'
try:
    from django.core.cache import cache
    cache.clear()
    print("✅ Cache limpo")
except:
    print("⚠️ Cache não configurado")
EOF

# 5. Reiniciar serviços
echo "🔄 Reiniciando serviços..."
sudo systemctl restart gunicorn
sleep 5
sudo systemctl restart nginx
sleep 3

# 6. Aguardar serviços subirem
echo "⏳ Aguardando serviços iniciarem (15 segundos)..."
sleep 15

# 7. Testar sitemap corrigido
echo "🧪 Testando sitemap corrigido..."
echo "URLs no sitemap após correção:"
curl -s https://prismaavaliacoes.com.br/sitemap.xml | grep -o "https://[^<]*" | head -10

echo ""
echo "🤖 Testando robots.txt:"
curl -s https://prismaavaliacoes.com.br/robots.txt | grep Sitemap

echo ""
echo "=================================================="
echo "✅ CORREÇÃO APLICADA!"
echo "=================================================="
echo ""
echo "🔍 VERIFICAÇÃO:"
echo "1. Acesse: https://prismaavaliacoes.com.br/sitemap.xml"
echo "2. URLs devem mostrar 'prismaavaliacoes.com.br'"
echo "3. Se ainda mostrar 'example.com', execute:"
echo "   sudo systemctl restart gunicorn"
echo "   sudo systemctl restart nginx"
echo ""
echo "📞 Resubmeta o sitemap no Google Search Console!"
