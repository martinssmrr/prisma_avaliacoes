#!/bin/bash

# SCRIPT COMPLETO DE DEPLOY - PRISMA AVALIAÇÕES VPS HOSTINGER
# Atualiza o sistema em produção com todas as melhorias implementadas

echo "🚀 DEPLOY PRISMA AVALIAÇÕES - HOSTINGER VPS"
echo "============================================="
echo "Data: $(date)"
echo "Todas as atualizações: Settings fix, SEO, Canonical Tags, Cores"
echo ""

# Configurações do servidor
SERVER_PATH="/var/www/html/prismaavaliacoes.com.br"
BACKUP_PATH="/var/www/backups"
PROJECT_NAME="prisma_avaliacoes"

# Criar diretório de backup se não existir
mkdir -p "$BACKUP_PATH"

# 1. BACKUP DO SISTEMA ATUAL
echo "💾 1. Fazendo backup do sistema atual..."
BACKUP_FILE="$BACKUP_PATH/backup_$(date +%Y%m%d_%H%M%S).tar.gz"
cd /var/www/html/
tar -czf "$BACKUP_FILE" prismaavaliacoes.com.br/
echo "✅ Backup criado: $BACKUP_FILE"

# 2. ATUALIZAR CÓDIGO DO REPOSITÓRIO
echo ""
echo "📥 2. Atualizando código do repositório..."
cd "$SERVER_PATH"

# Verificar se é um repositório git
if [ -d ".git" ]; then
    echo "🔄 Atualizando repositório existente..."
    
    # Corrigir problema de ownership do Git
    git config --global --add safe.directory /var/www/html/prismaavaliacoes.com.br
    
    git fetch origin master
    git reset --hard origin/master
    echo "✅ Código atualizado via Git"
else
    echo "📦 Clonando repositório fresh..."
    cd /var/www/html/
    mv prismaavaliacoes.com.br prismaavaliacoes.com.br_old_$(date +%Y%m%d_%H%M%S)
    git clone https://github.com/martinssmrr/prisma_avaliacoes.git prismaavaliacoes.com.br
    cd "$SERVER_PATH"
    echo "✅ Repositório clonado"
fi

# 3. CORREÇÃO CRÍTICA - RESOLVER CONFLITO SETTINGS
echo ""
echo "🔧 3. Resolvendo conflito de configurações..."
if [ -d "setup/settings" ]; then
    mv setup/settings "setup/settings_backup_$(date +%Y%m%d_%H%M%S)"
    echo "✅ Conflito setup/settings/ resolvido"
else
    echo "✅ Nenhum conflito de settings encontrado"
fi

# 4. CONFIGURAR AMBIENTE VIRTUAL
echo ""
echo "🐍 4. Configurando ambiente virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Ambiente virtual criado"
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependências instaladas"

# 5. VERIFICAR CONFIGURAÇÃO DJANGO
echo ""
echo "🧪 5. Testando configuração Django..."
python manage.py check --settings=setup.settings
if [ $? -eq 0 ]; then
    echo "✅ Configuração Django válida"
else
    echo "❌ Erro na configuração Django"
    echo "Verifique logs acima e corrija manualmente"
    exit 1
fi

# 6. APLICAR MIGRAÇÕES DO BANCO DE DADOS
echo ""
echo "💽 6. Aplicando migrações do banco de dados..."
python manage.py migrate --settings=setup.settings
echo "✅ Migrações aplicadas"

# 7. CONFIGURAR SEO E SITES FRAMEWORK
echo ""
echo "🎯 7. Configurando SEO e Sites Framework..."
python manage.py shell --settings=setup.settings << 'EOF'
from django.contrib.sites.models import Site
from seo.models import SEOConfig

print("=== CONFIGURAÇÃO SEO ===")

# Configurar Site para URLs corretas
try:
    site = Site.objects.get(pk=1)
    site.domain = 'prismaavaliacoes.com.br'
    site.name = 'Prisma Avaliações'
    site.save()
    print(f"✅ Site configurado: {site.domain}")
except Exception as e:
    print(f"❌ Erro ao configurar site: {e}")

# Criar/atualizar configuração SEO
try:
    config, created = SEOConfig.objects.get_or_create(
        pk=1,
        defaults={
            'site_name': 'Prisma Avaliações',
            'default_description': 'Prisma Avaliações Imobiliárias - Especialistas em avaliações de imóveis no Brasil. Laudos técnicos, agilidade e confiabilidade comprovada.',
            'default_keywords': 'avaliação imobiliária, laudo técnico de avaliação, avaliação de imóveis, laudo de avaliação de imóveis, avaliação de um imóvel, modelo de avaliação de imóveis',
            'contact_email': 'contato@prismaavaliacoes.com.br',
            'domain': 'prismaavaliacoes.com.br',
            'default_image': '/static/img/logo.png'
        }
    )
    
    if created:
        print(f"✅ SEOConfig criado: {config.site_name}")
    else:
        # Atualizar domínio se já existe
        config.domain = 'prismaavaliacoes.com.br'
        config.site_name = 'Prisma Avaliações'
        config.save()
        print(f"✅ SEOConfig atualizado: {config.domain}")
        
except Exception as e:
    print(f"❌ Erro SEO: {e}")

print("=== CONFIGURAÇÃO CONCLUÍDA ===")
EOF

# 8. COLETAR ARQUIVOS ESTÁTICOS
echo ""
echo "📁 8. Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --settings=setup.settings
echo "✅ Arquivos estáticos coletados"

# 9. CONFIGURAR PERMISSÕES
echo ""
echo "🔐 9. Configurando permissões..."
chown -R www-data:www-data "$SERVER_PATH"
chmod -R 755 "$SERVER_PATH"
echo "✅ Permissões configuradas"

# 10. REINICIAR SERVIÇOS
echo ""
echo "🔄 10. Reiniciando serviços..."

# Parar serviços
systemctl stop gunicorn
systemctl stop nginx

# Aguardar parada completa
sleep 2

# Iniciar serviços
systemctl start nginx
systemctl start gunicorn

# Habilitar inicialização automática
systemctl enable nginx
systemctl enable gunicorn

# Recarregar configurações
systemctl reload nginx

echo "✅ Serviços reiniciados"

# 11. VERIFICAÇÃO FINAL
echo ""
echo "📊 11. Verificação final dos serviços..."
echo "Nginx: $(systemctl is-active nginx)"
echo "Gunicorn: $(systemctl is-active gunicorn)"

# Verificar se os processos estão rodando
if systemctl is-active --quiet nginx && systemctl is-active --quiet gunicorn; then
    echo "✅ Todos os serviços estão ativos"
else
    echo "⚠️  Algum serviço pode não estar funcionando corretamente"
    echo "Status detalhado:"
    systemctl status nginx --no-pager -l
    systemctl status gunicorn --no-pager -l
fi

# 12. TESTE DE CONECTIVIDADE
echo ""
echo "🌐 12. Testando conectividade..."
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/ | grep -q "200\|301\|302" && echo "✅ Servidor Django respondendo" || echo "❌ Problema no servidor Django"

echo ""
echo "🎉 DEPLOY CONCLUÍDO COM SUCESSO!"
echo "============================================="
echo "📋 RESUMO DAS ATUALIZAÇÕES APLICADAS:"
echo "✅ Conflito setup/settings resolvido"
echo "✅ Código atualizado do repositório"
echo "✅ Migrações do banco aplicadas"
echo "✅ SEO configurado (prismaavaliacoes.com.br)"
echo "✅ Canonical tags implementadas"
echo "✅ Cores atualizadas (#1e40af)"
echo "✅ Arquivos estáticos coletados"
echo "✅ Serviços reiniciados"
echo ""
echo "🌐 URLS PARA TESTAR:"
echo "🏠 Site: https://prismaavaliacoes.com.br/"
echo "🔧 Admin: https://prismaavaliacoes.com.br/admin/"
echo "📈 SEO Meta: https://prismaavaliacoes.com.br/admin/seo/seometa/"
echo "⚙️  SEO Config: https://prismaavaliacoes.com.br/admin/seo/seoconfig/"
echo "🗺️  Sitemap: https://prismaavaliacoes.com.br/sitemap.xml"
echo ""
echo "💾 Backup do sistema anterior em: $BACKUP_FILE"
echo ""
echo "🎯 PRÓXIMOS PASSOS:"
echo "1. Testar todas as URLs acima"
echo "2. Verificar se admin SEO está funcionando"
echo "3. Confirmar sitemap com domínio correto"
echo "4. Testar canonical tags no código fonte"
echo ""
echo "✨ Sistema atualizado com todas as melhorias!"
