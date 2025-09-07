#!/bin/bash
# Script de verificação rápida do sitemap

echo "🔍 VERIFICAÇÃO RÁPIDA DO SITEMAP"
echo "==============================="

# Verificar sitemap atual
echo "📄 Conteúdo atual do sitemap:"
curl -s https://prismaavaliacoes.com.br/sitemap.xml | head -20

echo ""
echo "🤖 Conteúdo atual do robots.txt:"
curl -s https://prismaavaliacoes.com.br/robots.txt

echo ""
echo "🔧 Verificando configuração no servidor:"
cd /var/www/prisma_avaliacoes

# Verificar qual sitemap está sendo usado
grep -n "sitemaps" setup/urls.py

echo ""
echo "📊 Status dos serviços:"
systemctl is-active gunicorn nginx

echo ""
echo "⏰ Última modificação dos arquivos:"
ls -la setup/urls.py seo/sitemaps.py simple_sitemap.py 2>/dev/null
