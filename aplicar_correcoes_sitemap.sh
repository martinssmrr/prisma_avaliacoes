#!/bin/bash
# Script para aplicar correções do sitemap no servidor IMEDIATAMENTE

echo "🚀 APLICANDO CORREÇÕES DO SITEMAP NO SERVIDOR"
echo "=============================================="

# 1. Navegar para diretório do projeto
cd /var/www/prisma_avaliacoes || {
    echo "❌ Erro: Diretório do projeto não encontrado"
    exit 1
}

echo "📁 Diretório atual: $(pwd)"

# 2. Fazer backup antes de aplicar mudanças
echo "💾 Fazendo backup dos arquivos..."
cp setup/urls.py setup/urls.py.backup.$(date +%Y%m%d_%H%M%S)
if [ -f "seo/sitemaps.py" ]; then
    cp seo/sitemaps.py seo/sitemaps.py.backup.$(date +%Y%m%d_%H%M%S)
fi

# 3. Atualizar código do repositório
echo "📥 Atualizando código do repositório..."
git stash push -m "Backup antes da atualização sitemap"
git pull origin master

if [ $? -ne 0 ]; then
    echo "❌ Erro ao fazer git pull"
    echo "Tentando forçar atualização..."
    git reset --hard origin/master
fi

# 4. Verificar se os arquivos foram atualizados
echo "🔍 Verificando arquivos atualizados..."

if [ -f "simple_sitemap.py" ]; then
    echo "✅ simple_sitemap.py encontrado"
else
    echo "❌ simple_sitemap.py NÃO encontrado"
fi

if [ -f "GUIA_RESOLVER_SITEMAP.md" ]; then
    echo "✅ GUIA_RESOLVER_SITEMAP.md encontrado"
else
    echo "❌ GUIA_RESOLVER_SITEMAP.md NÃO encontrado"
fi

# 5. Verificar se SEO está funcionando
echo "🧪 Testando configuração SEO..."
python3 manage.py shell --settings=setup.settings_production -c "
try:
    from seo.models import SEOConfig
    config = SEOConfig.get_config()
    if config:
        print('✅ SEOConfig funcionando')
        print(f'   Domínio: {config.site_domain}')
        print(f'   URL completa: {config.get_full_domain()}')
    else:
        print('⚠️ SEOConfig não encontrado - criando...')
        SEOConfig.objects.create(
            site_name='Prisma Avaliações Imobiliárias',
            site_domain='prismaavaliacoes.com.br',
            site_description='Avaliações imobiliárias profissionais em Minas Gerais'
        )
        print('✅ SEOConfig criado')
except Exception as e:
    print(f'❌ Erro no SEO: {e}')
"

# 6. Limpar cache do Django se existir
echo "🧹 Limpando cache..."
python3 manage.py shell --settings=setup.settings_production -c "
try:
    from django.core.cache import cache
    cache.clear()
    print('✅ Cache limpo')
except:
    print('⚠️ Cache não configurado')
"

# 7. Reiniciar serviços
echo "🔄 Reiniciando serviços..."
sudo systemctl restart gunicorn
sleep 3
sudo systemctl restart nginx
sleep 2

# 8. Verificar status dos serviços
echo "📊 Verificando status dos serviços..."
if systemctl is-active --quiet gunicorn; then
    echo "✅ Gunicorn: Ativo"
else
    echo "❌ Gunicorn: Inativo"
    sudo systemctl status gunicorn --no-pager -l
fi

if systemctl is-active --quiet nginx; then
    echo "✅ Nginx: Ativo"
else
    echo "❌ Nginx: Inativo"
    sudo systemctl status nginx --no-pager -l
fi

# 9. Testar sitemap
echo "🌐 Testando sitemap..."
echo "Aguarde 10 segundos para os serviços iniciarem..."
sleep 10

curl -s -o /dev/null -w "%{http_code}" http://localhost/sitemap.xml > /tmp/sitemap_test
status_code=$(cat /tmp/sitemap_test)

if [ "$status_code" = "200" ]; then
    echo "✅ Sitemap respondendo (código 200)"
    echo "🔗 Acesse: https://prismaavaliacoes.com.br/sitemap.xml"
else
    echo "❌ Sitemap com problema (código $status_code)"
fi

# 10. Testar robots.txt
curl -s -o /dev/null -w "%{http_code}" http://localhost/robots.txt > /tmp/robots_test
robots_code=$(cat /tmp/robots_test)

if [ "$robots_code" = "200" ]; then
    echo "✅ Robots.txt respondendo (código 200)"
    echo "🔗 Acesse: https://prismaavaliacoes.com.br/robots.txt"
else
    echo "❌ Robots.txt com problema (código $robots_code)"
fi

echo ""
echo "=============================================="
echo "🎉 CORREÇÕES APLICADAS!"
echo "=============================================="
echo ""
echo "📋 VERIFICAÇÕES OBRIGATÓRIAS:"
echo "1. Acesse: https://prismaavaliacoes.com.br/sitemap.xml"
echo "2. Verifique se as URLs têm prismaavaliacoes.com.br"
echo "3. Acesse: https://prismaavaliacoes.com.br/robots.txt"
echo "4. Resubmeta sitemap no Google Search Console"
echo ""
echo "📞 Se houver problemas:"
echo "- Logs: sudo tail -f /var/log/gunicorn/gunicorn.log"
echo "- Status: sudo systemctl status gunicorn"
echo ""
echo "✅ SCRIPT CONCLUÍDO!"
