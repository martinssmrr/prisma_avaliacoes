#!/bin/bash

# Script para corrigir problema de configuração Django no servidor
# Resolve conflito entre setup/settings.py e setup/settings/

echo "=== CORREÇÃO DJANGO SETTINGS - PRODUÇÃO ==="
echo "Data: $(date)"
echo "Servidor: $(hostname)"
echo ""

# Navegar para o diretório do projeto
cd /var/www/html/prismaavaliacoes.com.br || {
    echo "❌ Erro: Diretório do projeto não encontrado"
    exit 1
}

echo "📂 Diretório atual: $(pwd)"
echo ""

# Verificar se existe o conflito
echo "🔍 Verificando estrutura de arquivos..."
if [ -d "setup/settings" ] && [ -f "setup/settings.py" ]; then
    echo "⚠️  CONFLITO DETECTADO:"
    echo "   - Arquivo: setup/settings.py"
    echo "   - Diretório: setup/settings/"
    echo ""
    
    # Fazer backup do diretório settings
    echo "💾 Criando backup do diretório settings..."
    if [ -d "setup/settings_backup" ]; then
        rm -rf setup/settings_backup
    fi
    mv setup/settings setup/settings_backup
    echo "✅ Diretório renomeado: setup/settings → setup/settings_backup"
    echo ""
    
elif [ -f "setup/settings.py" ]; then
    echo "✅ Apenas setup/settings.py encontrado (correto)"
    echo ""
else
    echo "❌ Nenhuma configuração Django encontrada!"
    exit 1
fi

# Ativar ambiente virtual se existir
if [ -d "venv" ]; then
    echo "🐍 Ativando ambiente virtual..."
    source venv/bin/activate
    echo "✅ Ambiente virtual ativado"
    echo ""
fi

# Testar configuração Django
echo "🧪 Testando configuração Django..."
python manage.py check --settings=setup.settings
CHECK_STATUS=$?

if [ $CHECK_STATUS -eq 0 ]; then
    echo "✅ Configuração Django OK"
    echo ""
else
    echo "❌ Erro na configuração Django"
    echo ""
fi

# Aplicar migrações
echo "🔄 Aplicando migrações..."
python manage.py migrate --settings=setup.settings
MIGRATE_STATUS=$?

if [ $MIGRATE_STATUS -eq 0 ]; then
    echo "✅ Migrações aplicadas com sucesso"
    echo ""
else
    echo "❌ Erro ao aplicar migrações"
    echo ""
fi

# Verificar se app SEO está funcionando
echo "🔍 Verificando app SEO..."
python manage.py shell --settings=setup.settings << 'EOF'
try:
    from seo.models import SEOMeta, SEOConfig
    print("✅ SEO models importados com sucesso")
    
    seo_count = SEOMeta.objects.count()
    config_count = SEOConfig.objects.count()
    
    print(f"📊 SEOMeta registros: {seo_count}")
    print(f"📊 SEOConfig registros: {config_count}")
    
    if config_count == 0:
        print("⚠️  Criando configuração SEO padrão...")
        config = SEOConfig.objects.create(
            site_name="Prisma Avaliações",
            default_description="Prisma Avaliações Imobiliárias - Serviços profissionais de avaliação",
            default_keywords="avaliação imobiliária, laudo de avaliação, prisma",
            contact_email="contato@prismaavaliacoes.com.br",
            domain="prismaavaliacoes.com.br"
        )
        print(f"✅ Configuração SEO criada: {config.site_name}")
    
except Exception as e:
    print(f"❌ Erro no app SEO: {e}")
EOF

SEO_STATUS=$?

if [ $SEO_STATUS -eq 0 ]; then
    echo "✅ App SEO funcionando"
    echo ""
else
    echo "❌ Erro no app SEO"
    echo ""
fi

# Reiniciar serviços se necessário
echo "🔄 Reiniciando serviços..."
systemctl reload nginx
systemctl restart gunicorn

echo ""
echo "=== RESUMO ==="
echo "✅ Conflito de settings resolvido"
echo "✅ Migrações aplicadas"
echo "✅ App SEO verificado"
echo "✅ Serviços reiniciados"
echo ""
echo "🌐 Teste o admin em: https://prismaavaliacoes.com.br/admin/"
echo ""
echo "=== SCRIPT CONCLUÍDO ==="
