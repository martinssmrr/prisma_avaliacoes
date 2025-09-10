#!/bin/bash

# MIGRAÇÃO RÁPIDA - APP SEO APENAS
# Para quando a pasta SEO já existe, só falta migrar o banco

echo "🚀 MIGRAÇÃO RÁPIDA - APP SEO"
echo "============================"
echo "Data: $(date)"
echo ""

# Configurações
SERVER_PATH="/var/www/html/prismaavaliacoes.com.br"

cd "$SERVER_PATH"
source venv/bin/activate

echo "📍 Diretório: $(pwd)"
echo "🐍 Python: $(which python)"
echo ""

echo "🔍 1. Verificando app SEO..."
if [ -d "seo" ]; then
    echo "✅ Pasta seo/ existe"
    echo "📁 Conteúdo da pasta seo/:"
    ls -la seo/ | head -10
else
    echo "❌ Pasta seo/ não encontrada"
    exit 1
fi

echo ""
echo "🧪 2. Testando configuração Django..."
python manage.py check --settings=setup.settings
if [ $? -eq 0 ]; then
    echo "✅ Django configurado corretamente"
else
    echo "❌ Problema na configuração Django"
    exit 1
fi

echo ""
echo "🔧 3. Criando migrações SEO..."
python manage.py makemigrations seo --settings=setup.settings

echo ""
echo "💽 4. Aplicando migrações..."
python manage.py migrate --settings=setup.settings

echo ""
echo "🔄 5. Reiniciando serviços..."
systemctl restart gunicorn
echo "✅ Gunicorn reiniciado"

systemctl reload nginx
echo "✅ Nginx recarregado"

echo ""
echo "⏱️  6. Aguardando estabilização..."
sleep 3

echo ""
echo "🧪 7. Testando admin SEO..."
ADMIN_SEO_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://prismaavaliacoes.com.br/admin/seo/)
echo "Status /admin/seo/: $ADMIN_SEO_STATUS"

if [ "$ADMIN_SEO_STATUS" = "302" ] || [ "$ADMIN_SEO_STATUS" = "200" ]; then
    echo "✅ SUCCESS! Admin SEO funcionando!"
else
    echo "⚠️  Status $ADMIN_SEO_STATUS - pode precisar de login"
fi

echo ""
echo "🎉 MIGRAÇÃO CONCLUÍDA!"
echo "============================"
echo "🌐 TESTE AS URLS:"
echo "  https://prismaavaliacoes.com.br/admin/"
echo "  https://prismaavaliacoes.com.br/admin/seo/"
echo "  https://prismaavaliacoes.com.br/admin/seo/seometa/"
echo "  https://prismaavaliacoes.com.br/admin/seo/seoconfig/"
echo ""
echo "📋 NO ADMIN DEVE APARECER:"
echo "  ✅ Seção 'SEO' no menu lateral"
echo "  ✅ Submenu 'SEO metas' e 'SEO configs'"
