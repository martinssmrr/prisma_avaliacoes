#!/bin/bash

# SCRIPT DE CLONE FRESH - PRISMA AVALIAÇÕES
# Clona repositório com todas as atualizações SEO

echo "🚀 CLONE FRESH - PRISMA AVALIAÇÕES"
echo "Data: $(date)"
echo "================================="

# 1. Backup do projeto atual
echo "💾 Fazendo backup do projeto atual..."
if [ -d "/var/www/prisma_avaliacoes" ]; then
    mv /var/www/prisma_avaliacoes /var/www/prisma_avaliacoes_backup_$(date +%Y%m%d_%H%M%S)
    echo "✅ Backup criado"
else
    echo "ℹ️  Nenhum projeto anterior encontrado"
fi

# 2. Clone fresh do repositório
echo ""
echo "📥 Clonando repositório atualizado..."
cd /var/www/
git clone https://github.com/martinssmrr/prisma_avaliacoes.git
cd prisma_avaliacoes

echo "✅ Repositório clonado com todas as atualizações"

# 3. Verificar conteúdo SEO
echo ""
echo "🔍 Verificando atualizações SEO..."
echo "App SEO: $([ -d 'seo' ] && echo '✅ OK' || echo '❌ Missing')"
echo "Models: $([ -f 'seo/models.py' ] && echo '✅ OK' || echo '❌ Missing')"
echo "Admin: $([ -f 'seo/admin.py' ] && echo '✅ OK' || echo '❌ Missing')"
echo "Migrations: $([ -d 'seo/migrations' ] && echo '✅ OK' || echo '❌ Missing')"

# 4. Resolver conflito de settings (mesmo problema que tínhamos)
echo ""
echo "🔧 Resolvendo conflito de settings..."
if [ -d "setup/settings" ]; then
    mv setup/settings setup/settings_backup_$(date +%Y%m%d_%H%M%S)
    echo "✅ Conflito resolvido: setup/settings/ → backup"
else
    echo "✅ Nenhum conflito encontrado"
fi

# 5. Setup ambiente virtual
echo ""
echo "🐍 Configurando ambiente virtual..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Ambiente virtual configurado"

# 6. Configurar banco de dados
echo ""
echo "💽 Configurando banco de dados..."
python manage.py migrate --settings=setup.settings
echo "✅ Migrações aplicadas"

# 7. Configurar SEO
echo ""
echo "🎯 Configurando SEO..."
python manage.py shell --settings=setup.settings << 'EOF'
from django.contrib.sites.models import Site
from seo.models import SEOConfig

# Configurar Site
try:
    site = Site.objects.get(pk=1)
    site.domain = 'prismaavaliacoes.com.br'
    site.name = 'Prisma Avaliações'
    site.save()
    print(f"✅ Site configurado: {site.domain}")
except Exception as e:
    print(f"❌ Erro site: {e}")

# Configurar SEO
try:
    config, created = SEOConfig.objects.get_or_create(
        pk=1,
        defaults={
            'site_name': 'Prisma Avaliações',
            'default_description': 'Prisma Avaliações Imobiliárias - Serviços profissionais de avaliação de imóveis',
            'default_keywords': 'avaliação imobiliária, laudo de avaliação, prisma avaliações',
            'contact_email': 'contato@prismaavaliacoes.com.br',
            'domain': 'prismaavaliacoes.com.br'
        }
    )
    status = 'criado' if created else 'atualizado'
    print(f"✅ SEOConfig {status}: {config.site_name}")
except Exception as e:
    print(f"❌ Erro SEO: {e}")
EOF

# 8. Coletar arquivos estáticos
echo ""
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --settings=setup.settings
echo "✅ Estáticos coletados"

# 9. Configurar permissões
echo ""
echo "🔐 Configurando permissões..."
chown -R www-data:www-data .
chmod -R 755 .
echo "✅ Permissões configuradas"

# 10. Reiniciar serviços
echo ""
echo "🔄 Reiniciando serviços..."
systemctl restart gunicorn
systemctl reload nginx
echo "✅ Serviços reiniciados"

# 11. Verificação final
echo ""
echo "📊 Verificação final..."
echo "Gunicorn: $(systemctl is-active gunicorn)"
echo "Nginx: $(systemctl is-active nginx)"

echo ""
echo "🎉 CLONE FRESH CONCLUÍDO!"
echo "================================="
echo "🌐 Site: https://prismaavaliacoes.com.br/"
echo "🔧 Admin: https://prismaavaliacoes.com.br/admin/"
echo "📈 SEO Meta: https://prismaavaliacoes.com.br/admin/seo/seometa/"
echo "⚙️ SEO Config: https://prismaavaliacoes.com.br/admin/seo/seoconfig/"
echo "🗺️ Sitemap: https://prismaavaliacoes.com.br/sitemap.xml"
echo ""
echo "✨ Todas as atualizações SEO incluídas!"
