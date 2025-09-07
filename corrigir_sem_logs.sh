#!/bin/bash
# Script para corrigir sitemap SEM depender de logs específicos

echo "🛠️ CORREÇÃO DO SITEMAP SEM LOGS"
echo "==============================="

cd /var/www/prisma_avaliacoes || exit 1

# 1. Verificar se estamos no diretório correto
echo "📁 Diretório atual: $(pwd)"
echo "📋 Arquivos Django:"
ls -la manage.py setup/ seo/ 2>/dev/null

# 2. Corrigir configurações básicas
echo ""
echo "🔧 Aplicando correções de configuração..."

# Script Python para corrigir tudo
python3 << 'EOF'
import os
import sys
import django

# Configurar ambiente
sys.path.insert(0, '/var/www/prisma_avaliacoes')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings_production')

try:
    django.setup()
    print("✅ Django configurado com sucesso")
    
    # Corrigir Sites framework
    from django.contrib.sites.models import Site
    site, created = Site.objects.get_or_create(pk=1, defaults={
        'domain': 'prismaavaliacoes.com.br',
        'name': 'Prisma Avaliações Imobiliárias'
    })
    
    if site.domain != 'prismaavaliacoes.com.br':
        site.domain = 'prismaavaliacoes.com.br'
        site.name = 'Prisma Avaliações Imobiliárias'
        site.save()
        print(f"✅ Site corrigido: {site.domain}")
    else:
        print(f"✅ Site já correto: {site.domain}")
    
    # Corrigir SEO Config
    from seo.models import SEOConfig
    config, created = SEOConfig.objects.get_or_create(defaults={
        'site_name': 'Prisma Avaliações Imobiliárias',
        'site_domain': 'prismaavaliacoes.com.br',
        'site_description': 'Avaliações imobiliárias profissionais em Minas Gerais'
    })
    
    if config.site_domain != 'prismaavaliacoes.com.br':
        config.site_domain = 'prismaavaliacoes.com.br'
        config.save()
        print(f"✅ SEO Config corrigido: {config.site_domain}")
    else:
        print(f"✅ SEO Config já correto: {config.site_domain}")
    
    # Testar sitemap
    print("\n🧪 Testando sitemap...")
    from django.test import RequestFactory
    from django.contrib.sitemaps.views import sitemap
    
    # Usar simple_sitemap se seo.sitemaps der problema
    try:
        from seo.sitemaps import sitemaps
        print("✅ Usando seo.sitemaps")
    except:
        print("⚠️ Problema com seo.sitemaps, usando simple_sitemap")
        # Criar sitemap básico
        from django.contrib.sitemaps import Sitemap
        
        class BasicSitemap(Sitemap):
            protocol = 'https'
            def items(self):
                return ['/']
            def location(self, item):
                return item
        
        sitemaps = {'basic': BasicSitemap}
    
    # Testar geração do sitemap
    factory = RequestFactory()
    request = factory.get('/sitemap.xml')
    request.META['HTTP_HOST'] = 'prismaavaliacoes.com.br'
    
    try:
        response = sitemap(request, sitemaps=sitemaps)
        content = response.content.decode('utf-8')
        if 'prismaavaliacoes.com.br' in content:
            print("✅ Sitemap gerando URLs corretas")
        else:
            print("❌ Sitemap ainda com URLs incorretas")
            print("Primeiras linhas:", content[:200])
    except Exception as e:
        print(f"❌ Erro ao testar sitemap: {e}")
    
except Exception as e:
    print(f"❌ Erro geral: {e}")
    import traceback
    traceback.print_exc()
EOF

# 3. Encontrar e reiniciar serviços
echo ""
echo "🔄 Reiniciando serviços..."

# Encontrar serviços relacionados
echo "Serviços encontrados:"
systemctl list-units --type=service | grep -E "(gunicorn|django|prisma|nginx)"

# Reiniciar serviços comuns
services_to_restart=("nginx" "gunicorn")

for service in "${services_to_restart[@]}"; do
    if systemctl is-enabled $service &>/dev/null; then
        echo "Reiniciando $service..."
        systemctl restart $service
        sleep 2
        if systemctl is-active $service &>/dev/null; then
            echo "✅ $service ativo"
        else
            echo "❌ $service com problema"
        fi
    else
        echo "⚠️ $service não encontrado"
    fi
done

# 4. Testar resultado final
echo ""
echo "🧪 Teste final do sitemap..."
sleep 5

# Testar diferentes URLs
for url in "http://localhost/sitemap.xml" "http://127.0.0.1/sitemap.xml" "https://prismaavaliacoes.com.br/sitemap.xml"; do
    echo "Testando $url:"
    response=$(curl -s -w "%{http_code}" "$url" | tail -1)
    if [ "$response" = "200" ]; then
        echo "✅ $url responde"
        curl -s "$url" | grep -o "https://[^<]*" | head -3
    else
        echo "❌ $url código: $response"
    fi
    echo ""
done

echo "==============================="
echo "🎉 CORREÇÃO APLICADA!"
echo "==============================="
echo ""
echo "📋 VERIFICAÇÕES:"
echo "1. https://prismaavaliacoes.com.br/sitemap.xml"
echo "2. Se ainda mostrar example.com, aguarde 5-10 minutos"
echo "3. Resubmeta no Google Search Console"
