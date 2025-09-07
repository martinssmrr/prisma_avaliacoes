#!/bin/bash

# Script para sincronizar mudanças locais com servidor de produção
# Inclui as correções de settings e SEO

echo "=== SINCRONIZAÇÃO PRODUÇÃO ==="
echo "Data: $(date)"
echo ""

# Navegar para o diretório do projeto
cd /var/www/html/prismaavaliacoes.com.br || {
    echo "❌ Erro: Diretório do projeto não encontrado"
    exit 1
}

echo "📂 Diretório: $(pwd)"
echo ""

# Fazer backup antes das mudanças
echo "💾 Criando backup..."
cp -r . ../backup_$(date +%Y%m%d_%H%M%S)
echo "✅ Backup criado"
echo ""

# Atualizar código do Git
echo "📥 Atualizando código do Git..."
git fetch origin master
git reset --hard origin/master
echo "✅ Código atualizado"
echo ""

# Resolver conflito de settings (mesmo problema local)
echo "🔧 Resolvendo conflito de settings..."
if [ -d "setup/settings" ] && [ -f "setup/settings.py" ]; then
    echo "⚠️  Conflito detectado - renomeando diretório settings"
    mv setup/settings setup/settings_backup_$(date +%Y%m%d_%H%M%S)
    echo "✅ Conflito resolvido"
else
    echo "✅ Nenhum conflito encontrado"
fi
echo ""

# Ativar ambiente virtual
echo "🐍 Ativando ambiente virtual..."
source venv/bin/activate
echo "✅ Ambiente ativo"
echo ""

# Instalar/atualizar dependências
echo "📦 Verificando dependências..."
pip install -r requirements.txt --quiet
echo "✅ Dependências OK"
echo ""

# Aplicar migrações
echo "🔄 Aplicando migrações..."
python manage.py migrate --settings=setup.settings
echo "✅ Migrações aplicadas"
echo ""

# Coletar arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --settings=setup.settings
echo "✅ Estáticos coletados"
echo ""

# Verificar configuração SEO
echo "🔍 Configurando SEO..."
python manage.py shell --settings=setup.settings << 'EOF'
from django.contrib.sites.models import Site
from seo.models import SEOConfig

# Configurar Site correto
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
            'default_description': 'Prisma Avaliações Imobiliárias - Serviços profissionais de avaliação',
            'default_keywords': 'avaliação imobiliária, laudo de avaliação, prisma',
            'contact_email': 'contato@prismaavaliacoes.com.br',
            'domain': 'prismaavaliacoes.com.br'
        }
    )
    if created:
        print(f"✅ SEOConfig criado: {config.site_name}")
    else:
        config.domain = 'prismaavaliacoes.com.br'
        config.save()
        print(f"✅ SEOConfig atualizado: {config.domain}")
except Exception as e:
    print(f"❌ Erro SEO: {e}")
EOF

# Reiniciar serviços
echo ""
echo "🔄 Reiniciando serviços..."
systemctl reload nginx
systemctl restart gunicorn
echo "✅ Serviços reiniciados"
echo ""

# Verificar status
echo "📊 Verificando status..."
systemctl is-active nginx
systemctl is-active gunicorn
echo ""

echo "=== SINCRONIZAÇÃO CONCLUÍDA ==="
echo "🌐 Site: https://prismaavaliacoes.com.br/"
echo "🔧 Admin: https://prismaavaliacoes.com.br/admin/"
echo "🗺️  Sitemap: https://prismaavaliacoes.com.br/sitemap.xml"
echo ""
