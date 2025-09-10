#!/bin/bash

# Script para clone fresh do repositório Prisma Avaliações
# Remove instalação atual e faz setup completo do zero

echo "=== CLONE FRESH PRISMA AVALIAÇÕES ==="
echo "Data: $(date)"
echo ""

# Parar serviços
echo "🛑 Parando serviços..."
systemctl stop gunicorn
systemctl stop nginx

# Backup da instalação atual
echo "💾 Fazendo backup..."
BACKUP_DIR="/var/www/backup_prisma_$(date +%Y%m%d_%H%M%S)"
if [ -d "/var/www/prisma_avaliacoes" ]; then
    mv /var/www/prisma_avaliacoes "$BACKUP_DIR"
    echo "✅ Backup criado em: $BACKUP_DIR"
fi

# Navegar para diretório web
cd /var/www/ || exit 1

# Clone fresh do repositório
echo "📥 Clonando repositório..."
git clone https://github.com/martinssmrr/prisma_avaliacoes.git
cd prisma_avaliacoes

echo "✅ Repositório clonado"

# Criar ambiente virtual
echo "🐍 Criando ambiente virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
echo "📦 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Dependências instaladas"

# CORREÇÃO CRÍTICA: Resolver conflito settings
echo "🔧 Resolvendo conflito de settings..."
if [ -d "setup/settings" ]; then
    mv setup/settings setup/settings_backup_$(date +%Y%m%d_%H%M%S)
    echo "✅ Conflito de settings resolvido"
fi

# Verificar configuração Django
echo "🧪 Testando configuração Django..."
python manage.py check --settings=setup.settings
if [ $? -eq 0 ]; then
    echo "✅ Configuração Django OK"
else
    echo "❌ Erro na configuração Django"
    exit 1
fi

# Aplicar migrações
echo "🔄 Aplicando migrações..."
python manage.py migrate --settings=setup.settings

# Configurar SEO automaticamente
echo "⚙️  Configurando SEO..."
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
    print(f"❌ Erro ao configurar site: {e}")

# Configurar SEO
try:
    config, created = SEOConfig.objects.get_or_create(
        pk=1,
        defaults={
            'site_name': 'Prisma Avaliações',
            'default_description': 'Prisma Avaliações Imobiliárias - Serviços profissionais de avaliação de imóveis',
            'default_keywords': 'avaliação imobiliária, laudo de avaliação, prisma avaliações',
            'contact_email': 'contato@prismaavaliacoes.com.br',
            'domain': 'prismaavaliacoes.com.br',
            'default_image': '/static/img/logo-prisma.jpg'
        }
    )
    
    if created:
        print(f"✅ SEOConfig criado: {config.site_name}")
    else:
        # Atualizar domínio se já existe
        config.domain = 'prismaavaliacoes.com.br'
        config.save()
        print(f"✅ SEOConfig atualizado: {config.domain}")
        
except Exception as e:
    print(f"❌ Erro SEO: {e}")
EOF

# Coletar arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --settings=setup.settings

# Configurar permissões
echo "🔐 Configurando permissões..."
chown -R www-data:www-data /var/www/prisma_avaliacoes
chmod -R 755 /var/www/prisma_avaliacoes

# Atualizar configuração Nginx se necessário
echo "🌐 Atualizando Nginx..."
# Aqui você pode adicionar comandos para atualizar nginx.conf se necessário

# Reiniciar serviços
echo "🔄 Reiniciando serviços..."
systemctl start nginx
systemctl start gunicorn
systemctl enable gunicorn
systemctl enable nginx

# Verificar status
echo "📊 Verificando status dos serviços..."
echo "Nginx: $(systemctl is-active nginx)"
echo "Gunicorn: $(systemctl is-active gunicorn)"

echo ""
echo "=== CLONE FRESH CONCLUÍDO ==="
echo "🌐 Site: https://prismaavaliacoes.com.br/"
echo "🔧 Admin: https://prismaavaliacoes.com.br/admin/"
echo "📋 SEO Meta: https://prismaavaliacoes.com.br/admin/seo/seometa/"
echo "⚙️  SEO Config: https://prismaavaliacoes.com.br/admin/seo/seoconfig/"
echo "🗺️  Sitemap: https://prismaavaliacoes.com.br/sitemap.xml"
echo ""
echo "✅ Instalação fresh completa!"
echo "💾 Backup anterior em: $BACKUP_DIR"
