#!/bin/bash
# Script para forçar atualização do código e aplicar correções

echo "🚀 FORÇANDO ATUALIZAÇÃO E CORREÇÃO DO SITEMAP"
echo "============================================="

cd /var/www/prisma_avaliacoes || exit 1

# 1. Backup de segurança
echo "💾 Fazendo backup completo..."
tar -czf backup_antes_correcao_$(date +%Y%m%d_%H%M%S).tar.gz setup/ seo/ *.py

# 2. Forçar atualização do código
echo "🔄 Forçando atualização do repositório..."
git stash push -m "Backup antes de forçar atualização"
git fetch origin
git reset --hard origin/master

# 3. Verificar se arquivos foram atualizados
echo "📁 Verificando arquivos atualizados:"
ls -la simple_sitemap.py aplicar_correcoes_sitemap.sh corrigir_example_com.sh 2>/dev/null

# 4. Aplicar configurações específicas para resolver example.com
echo "🛠️ Aplicando configurações específicas..."

# Criar arquivo temporário de configuração
cat > fix_sitemap_urls.py << 'EOF'
#!/usr/bin/env python3
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings_production')
sys.path.insert(0, '/var/www/prisma_avaliacoes')
django.setup()

from django.contrib.sites.models import Site
from seo.models import SEOConfig

print("🔧 Corrigindo configurações de domínio...")

# Corrigir Sites framework
try:
    site = Site.objects.get_current()
    if site.domain != 'prismaavaliacoes.com.br':
        site.domain = 'prismaavaliacoes.com.br'
        site.name = 'Prisma Avaliações Imobiliárias'
        site.save()
        print(f"✅ Site domain atualizado: {site.domain}")
    else:
        print(f"✅ Site domain já correto: {site.domain}")
except Exception as e:
    print(f"❌ Erro no Sites: {e}")

# Corrigir SEO Config
try:
    config, created = SEOConfig.objects.get_or_create(
        defaults={
            'site_name': 'Prisma Avaliações Imobiliárias',
            'site_domain': 'prismaavaliacoes.com.br',
            'site_description': 'Avaliações imobiliárias profissionais em Minas Gerais'
        }
    )
    
    if config.site_domain != 'prismaavaliacoes.com.br':
        config.site_domain = 'prismaavaliacoes.com.br'
        config.save()
        print(f"✅ SEO Config atualizado: {config.site_domain}")
    else:
        print(f"✅ SEO Config já correto: {config.site_domain}")
        
except Exception as e:
    print(f"❌ Erro no SEO Config: {e}")

print("🎉 Configurações aplicadas!")
EOF

# Executar correção
python3 fix_sitemap_urls.py

# 5. Reiniciar serviços com força
echo "🔄 Reiniciando serviços com força..."
sudo systemctl stop gunicorn
sudo systemctl stop nginx
sleep 3
sudo systemctl start nginx
sudo systemctl start gunicorn
sleep 10

# 6. Verificar status
echo "📊 Status dos serviços:"
systemctl is-active gunicorn nginx

# 7. Testar resultado
echo "🧪 Testando resultado final..."
sleep 5

echo "URLs no sitemap:"
curl -s https://prismaavaliacoes.com.br/sitemap.xml | grep -o "https://[^<]*" | head -5

echo ""
echo "============================================="
if curl -s https://prismaavaliacoes.com.br/sitemap.xml | grep -q "prismaavaliacoes.com.br"; then
    echo "✅ SUCESSO! URLs corrigidas para prismaavaliacoes.com.br"
else
    echo "❌ PROBLEMA PERSISTE! URLs ainda com example.com"
    echo "Verifique logs:"
    echo "sudo tail -20 /var/log/gunicorn/gunicorn.log"
fi
echo "============================================="
