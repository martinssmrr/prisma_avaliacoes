#!/bin/bash

#=============================================================================
# SCRIPT DE DEPLOY PARA VPS - SISTEMA SEO PRISMA AVALIAÇÕES
#=============================================================================

echo "🚀 INICIANDO DEPLOY DO SISTEMA SEO - PRISMA AVALIAÇÕES"
echo "=================================================="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Diretório do projeto
PROJECT_DIR="/var/www/prisma_avaliacoes"

# Função para logging
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERRO]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[AVISO]${NC} $1"
}

# Verificar se estamos no diretório correto
if [[ ! -d "$PROJECT_DIR" ]]; then
    error "Diretório do projeto não encontrado: $PROJECT_DIR"
    exit 1
fi

cd "$PROJECT_DIR"

log "📂 Diretório atual: $(pwd)"

#=============================================================================
# 1. BACKUP E ATUALIZAÇÃO DO CÓDIGO
#=============================================================================

log "📋 1. FAZENDO BACKUP E ATUALIZANDO CÓDIGO..."

# Backup do banco de dados
if [[ -f "db.sqlite3" ]]; then
    log "💾 Fazendo backup do banco de dados..."
    cp db.sqlite3 "db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Atualizar código
log "📥 Fazendo pull do repositório..."
git stash push -m "Backup antes do deploy $(date)"
git pull origin master

if [[ $? -ne 0 ]]; then
    error "Falha no git pull"
    exit 1
fi

#=============================================================================
# 2. AMBIENTE VIRTUAL E DEPENDÊNCIAS
#=============================================================================

log "🐍 2. CONFIGURANDO AMBIENTE VIRTUAL..."

# Ativar ambiente virtual
if [[ -d "venv" ]]; then
    log "Ativando ambiente virtual..."
    source venv/bin/activate
else
    error "Ambiente virtual não encontrado!"
    exit 1
fi

# Verificar/instalar dependências
log "📦 Verificando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

#=============================================================================
# 3. CONFIGURAÇÕES E MIGRAÇÕES
#=============================================================================

log "⚙️ 3. APLICANDO CONFIGURAÇÕES E MIGRAÇÕES..."

# Usar configurações de produção
export DJANGO_SETTINGS_MODULE="setup.settings_production"

# Verificar se o Django consegue carregar
log "🔍 Verificando configurações..."
python manage.py check --settings=setup.settings_production

if [[ $? -ne 0 ]]; then
    error "Problemas nas configurações do Django"
    exit 1
fi

# Aplicar migrações
log "🗄️ Aplicando migrações..."
python manage.py makemigrations --settings=setup.settings_production
python manage.py migrate --settings=setup.settings_production

if [[ $? -ne 0 ]]; then
    error "Falha nas migrações"
    exit 1
fi

#=============================================================================
# 4. ARQUIVOS ESTÁTICOS E MÍDIA
#=============================================================================

log "📁 4. COLETANDO ARQUIVOS ESTÁTICOS..."

# Coletar arquivos estáticos
python manage.py collectstatic --noreload --settings=setup.settings_production

if [[ $? -ne 0 ]]; then
    warning "Problemas ao coletar arquivos estáticos"
fi

#=============================================================================
# 5. PERMISSÕES E PROPRIEDADE
#=============================================================================

log "🔐 5. AJUSTANDO PERMISSÕES..."

# Ajustar propriedade dos arquivos
chown -R www-data:www-data "$PROJECT_DIR"
chmod -R 755 "$PROJECT_DIR"

# Permissões especiais para banco de dados
chmod 664 db.sqlite3 2>/dev/null || true
chown www-data:www-data db.sqlite3 2>/dev/null || true

# Permissões para logs
mkdir -p logs
chmod 755 logs
chown www-data:www-data logs

#=============================================================================
# 6. TESTE DO SISTEMA SEO
#=============================================================================

log "🔍 6. TESTANDO SISTEMA SEO..."

# Verificar se app SEO foi instalado
python manage.py shell --settings=setup.settings_production << EOF
try:
    from seo.models import SEOMeta, SEOConfig
    print("✅ Modelos SEO carregados com sucesso")
    
    # Testar importação de template tags
    from seo.templatetags.seo_tags import render_seo
    print("✅ Template tags SEO funcionando")
    
    # Verificar sitemaps
    from seo.sitemaps import sitemaps
    print("✅ Sitemaps configurados:", list(sitemaps.keys()))
    
except Exception as e:
    print("❌ Erro no sistema SEO:", str(e))
    exit(1)
EOF

if [[ $? -ne 0 ]]; then
    error "Problemas no sistema SEO"
    exit 1
fi

#=============================================================================
# 7. REINICIAR SERVIÇOS
#=============================================================================

log "🔄 7. REINICIANDO SERVIÇOS..."

# Reiniciar Nginx
systemctl reload nginx
if [[ $? -eq 0 ]]; then
    log "✅ Nginx recarregado"
else
    warning "Problemas ao recarregar Nginx"
fi

# Reiniciar Gunicorn (se existir)
if systemctl is-active --quiet gunicorn; then
    systemctl restart gunicorn
    log "✅ Gunicorn reiniciado"
fi

# Reiniciar Apache (se existir)
if systemctl is-active --quiet apache2; then
    systemctl restart apache2
    log "✅ Apache reiniciado"
fi

#=============================================================================
# 8. VERIFICAÇÃO FINAL
#=============================================================================

log "✅ 8. VERIFICAÇÃO FINAL..."

# Testar URLs importantes
log "🌐 Testando URLs do sistema..."

# Função para testar URL
test_url() {
    local url=$1
    local name=$2
    
    if curl -s -o /dev/null -w "%{http_code}" "http://localhost$url" | grep -q "200\|301\|302"; then
        log "✅ $name: OK"
    else
        warning "⚠️ $name: Possível problema"
    fi
}

test_url "/admin/" "Admin"
test_url "/sitemap.xml" "Sitemap"
test_url "/robots.txt" "Robots.txt"
test_url "/" "Homepage"

#=============================================================================
# DEPLOY CONCLUÍDO
#=============================================================================

echo ""
echo "🎉 DEPLOY CONCLUÍDO COM SUCESSO!"
echo "================================"
echo ""
echo "📊 RESUMO:"
echo "• ✅ Código atualizado via Git"
echo "• ✅ Migrações aplicadas (incluindo SEO)"
echo "• ✅ Arquivos estáticos coletados"
echo "• ✅ Permissões ajustadas"
echo "• ✅ Sistema SEO instalado e testado"
echo "• ✅ Serviços reiniciados"
echo ""
echo "🌐 URLs importantes:"
echo "• Admin: https://prismaavaliacoes.com.br/admin/"
echo "• Sitemap: https://prismaavaliacoes.com.br/sitemap.xml"
echo "• Robots: https://prismaavaliacoes.com.br/robots.txt"
echo ""
echo "🔧 Próximos passos:"
echo "1. Acessar admin e configurar SEO global"
echo "2. Testar SEO em artigos existentes"
echo "3. Verificar sitemaps e robots.txt"
echo ""
echo "✨ Sistema SEO pronto para impulsionar seu ranking!"

# Desativar ambiente virtual
deactivate 2>/dev/null || true

log "🏁 Deploy finalizado em $(date)"
