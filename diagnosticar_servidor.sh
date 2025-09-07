#!/bin/bash
# Script para encontrar logs e diagnosticar o problema do sitemap

echo "🔍 DIAGNÓSTICO COMPLETO DO SERVIDOR"
echo "=================================="

cd /var/www/prisma_avaliacoes || exit 1

# 1. Encontrar logs do Gunicorn
echo "📄 Procurando logs do Gunicorn..."
find /var/log -name "*gunicorn*" 2>/dev/null
find /var/log -name "*django*" 2>/dev/null
find /var/www -name "*.log" 2>/dev/null

# 2. Verificar processos ativos
echo ""
echo "📊 Processos ativos:"
ps aux | grep gunicorn | grep -v grep
ps aux | grep nginx | grep -v grep

# 3. Verificar configuração do Gunicorn
echo ""
echo "⚙️ Configuração do Gunicorn:"
systemctl status gunicorn --no-pager

# 4. Verificar se há serviço customizado
echo ""
echo "🔧 Arquivos de serviço:"
ls -la /etc/systemd/system/*gunicorn* 2>/dev/null
ls -la /etc/systemd/system/*django* 2>/dev/null
ls -la /etc/systemd/system/*prisma* 2>/dev/null

# 5. Verificar configuração do Nginx
echo ""
echo "🌐 Configuração do Nginx:"
ls -la /etc/nginx/sites-enabled/
cat /etc/nginx/sites-enabled/* 2>/dev/null | grep -A5 -B5 prisma

# 6. Testar sitemap diretamente
echo ""
echo "🧪 Testando sitemap diretamente:"
python3 manage.py shell --settings=setup.settings_production << 'EOF'
import os
print("=== DIAGNÓSTICO DJANGO ===")
print("DEBUG:", os.environ.get('DEBUG', 'não definido'))
print("DJANGO_SETTINGS_MODULE:", os.environ.get('DJANGO_SETTINGS_MODULE', 'não definido'))

try:
    from django.conf import settings
    print("ALLOWED_HOSTS:", settings.ALLOWED_HOSTS)
    print("SITE_ID:", getattr(settings, 'SITE_ID', 'não definido'))
    
    from django.contrib.sites.models import Site
    site = Site.objects.get_current()
    print("Site atual:", site.domain, site.name)
    
    from seo.models import SEOConfig
    config = SEOConfig.objects.first()
    if config:
        print("SEO Config:", config.site_domain)
    else:
        print("SEO Config: não encontrado")
        
except Exception as e:
    print("Erro:", e)
EOF

# 7. Testar URL local
echo ""
echo "🌍 Testando URLs locais:"
curl -I http://localhost/sitemap.xml 2>/dev/null | head -1
curl -I http://127.0.0.1/sitemap.xml 2>/dev/null | head -1

# 8. Verificar porta do Gunicorn
echo ""
echo "🔌 Portas em uso:"
netstat -tlnp | grep python
netstat -tlnp | grep gunicorn

echo ""
echo "=================================="
echo "📋 PRÓXIMOS PASSOS:"
echo "1. Verificar logs encontrados acima"
echo "2. Aplicar correções baseadas no diagnóstico"
echo "3. Reiniciar serviços se necessário"
echo "=================================="
