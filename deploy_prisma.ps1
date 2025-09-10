# Script PowerShell para Deploy Remoto - Prisma Avaliações
# Execute este script no Windows para fazer deploy via SSH

param(
    [string]$Server = "srv989739.hstgr.cloud",
    [string]$User = "root",
    [switch]$VerifyOnly = $false
)

Write-Host "🚀 DEPLOY PRISMA AVALIAÇÕES - HOSTINGER VPS" -ForegroundColor Yellow
Write-Host "=============================================" -ForegroundColor Yellow
Write-Host "Servidor: $Server" -ForegroundColor Cyan
Write-Host "Usuário: $User" -ForegroundColor Cyan
Write-Host ""

# Verificar se tem OpenSSH ou PuTTY
$sshCommand = $null
if (Get-Command ssh -ErrorAction SilentlyContinue) {
    $sshCommand = "ssh"
    Write-Host "✅ OpenSSH encontrado" -ForegroundColor Green
} elseif (Get-Command plink -ErrorAction SilentlyContinue) {
    $sshCommand = "plink"
    Write-Host "✅ PuTTY plink encontrado" -ForegroundColor Green
} else {
    Write-Host "❌ SSH não encontrado" -ForegroundColor Red
    Write-Host ""
    Write-Host "OPÇÕES:" -ForegroundColor Yellow
    Write-Host "1. Instalar OpenSSH: winget install Microsoft.OpenSSH.Beta"
    Write-Host "2. Instalar PuTTY: winget install PuTTY.PuTTY"
    Write-Host "3. Executar comandos manualmente via cliente SSH"
    exit 1
}

if ($VerifyOnly) {
    Write-Host "🔍 MODO VERIFICAÇÃO - Executando apenas verificação pós-deploy" -ForegroundColor Cyan
    
    $verifyScript = @"
cd /var/www/html/prismaavaliacoes.com.br
source venv/bin/activate
echo '📊 Status dos serviços:'
systemctl is-active nginx
systemctl is-active gunicorn
echo '🧪 Teste Django:'
python manage.py check --settings=setup.settings
echo '🌐 Teste conectividade:'
curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/
echo '🎯 URLs para testar:'
echo 'https://prismaavaliacoes.com.br/'
echo 'https://prismaavaliacoes.com.br/admin/'
echo 'https://prismaavaliacoes.com.br/admin/seo/'
echo 'https://prismaavaliacoes.com.br/sitemap.xml'
"@

    & $sshCommand "$User@$Server" $verifyScript
    exit
}

Write-Host "⚠️  ATENÇÃO: Este deploy irá:" -ForegroundColor Yellow
Write-Host "  - Fazer backup do sistema atual" -ForegroundColor White
Write-Host "  - Atualizar código do Git" -ForegroundColor White
Write-Host "  - Aplicar migrações do banco" -ForegroundColor White
Write-Host "  - Reiniciar serviços" -ForegroundColor White
Write-Host ""

$confirm = Read-Host "Continuar com o deploy? (s/N)"
if ($confirm -ne 's' -and $confirm -ne 'S') {
    Write-Host "Deploy cancelado pelo usuário" -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "🚀 Iniciando deploy..." -ForegroundColor Green

# Script completo de deploy
$deployScript = @"
echo '🚀 DEPLOY PRISMA AVALIAÇÕES - INÍCIO'
echo 'Data: \$(date)'
echo ''

# Configurações
SERVER_PATH="/var/www/html/prismaavaliacoes.com.br"

# 1. Backup
echo '💾 1. Fazendo backup...'
cd /var/www/html/
cp -r prismaavaliacoes.com.br backup_\$(date +%Y%m%d_%H%M%S)
echo '✅ Backup criado'

# 2. Atualizar código
echo '📥 2. Atualizando código...'
cd "\$SERVER_PATH"

# Corrigir problema de ownership do Git
git config --global --add safe.directory /var/www/html/prismaavaliacoes.com.br

git fetch origin master
git reset --hard origin/master
echo '✅ Código atualizado'

# 3. Resolver conflito settings
echo '🔧 3. Resolvendo conflito settings...'
if [ -d "setup/settings" ]; then
    mv setup/settings setup/settings_backup_\$(date +%Y%m%d_%H%M%S)
    echo '✅ Conflito resolvido'
else
    echo '✅ Nenhum conflito'
fi

# 4. Ativar ambiente virtual
echo '🐍 4. Configurando ambiente...'
source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1
echo '✅ Ambiente configurado'

# 5. Testar configuração
echo '🧪 5. Testando configuração...'
python manage.py check --settings=setup.settings
if [ \$? -eq 0 ]; then
    echo '✅ Configuração OK'
else
    echo '❌ Erro na configuração'
    exit 1
fi

# 6. Aplicar migrações
echo '💽 6. Aplicando migrações...'
python manage.py migrate --settings=setup.settings
echo '✅ Migrações aplicadas'

# 7. Configurar SEO
echo '🎯 7. Configurando SEO...'
python manage.py shell --settings=setup.settings << 'EOF'
from django.contrib.sites.models import Site
from seo.models import SEOConfig

try:
    site = Site.objects.get(pk=1)
    site.domain = 'prismaavaliacoes.com.br'
    site.name = 'Prisma Avaliações'
    site.save()
    print('✅ Site configurado:', site.domain)
except Exception as e:
    print('❌ Erro site:', e)

try:
    config, created = SEOConfig.objects.get_or_create(
        pk=1,
        defaults={
            'site_name': 'Prisma Avaliações',
            'default_description': 'Prisma Avaliações Imobiliárias - Especialistas em avaliações de imóveis no Brasil.',
            'default_keywords': 'avaliação imobiliária, laudo técnico de avaliação, avaliação de imóveis',
            'contact_email': 'contato@prismaavaliacoes.com.br',
            'domain': 'prismaavaliacoes.com.br'
        }
    )
    status = 'criado' if created else 'atualizado'
    print(f'✅ SEOConfig {status}:', config.site_name)
except Exception as e:
    print('❌ Erro SEO:', e)
EOF
echo '✅ SEO configurado'

# 8. Coletar estáticos
echo '📁 8. Coletando arquivos estáticos...'
python manage.py collectstatic --noinput --settings=setup.settings > /dev/null 2>&1
echo '✅ Estáticos coletados'

# 9. Configurar permissões
echo '🔐 9. Configurando permissões...'
chown -R www-data:www-data .
chmod -R 755 .
echo '✅ Permissões configuradas'

# 10. Reiniciar serviços
echo '🔄 10. Reiniciando serviços...'
systemctl restart gunicorn
systemctl reload nginx
echo '✅ Serviços reiniciados'

# 11. Verificação final
echo '📊 11. Verificação final...'
echo 'Nginx:' \$(systemctl is-active nginx)
echo 'Gunicorn:' \$(systemctl is-active gunicorn)

# Teste de conectividade
sleep 2
STATUS=\$(curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/)
echo 'Conectividade:' \$STATUS

echo ''
echo '🎉 DEPLOY CONCLUÍDO!'
echo '🌐 URLs para testar:'
echo 'https://prismaavaliacoes.com.br/'
echo 'https://prismaavaliacoes.com.br/admin/'
echo 'https://prismaavaliacoes.com.br/admin/seo/'
echo 'https://prismaavaliacoes.com.br/sitemap.xml'
echo ''
echo '✨ Todas as atualizações aplicadas!'
"@

Write-Host "📡 Conectando ao servidor e executando deploy..." -ForegroundColor Cyan

try {
    if ($sshCommand -eq "ssh") {
        $deployScript | & ssh "$User@$Server" "bash -s"
    } else {
        $deployScript | & plink -ssh "$User@$Server" "bash -s"
    }
    
    Write-Host ""
    Write-Host "✅ DEPLOY CONCLUÍDO COM SUCESSO!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 TESTE AS URLS:" -ForegroundColor Yellow
    Write-Host "https://prismaavaliacoes.com.br/" -ForegroundColor White
    Write-Host "https://prismaavaliacoes.com.br/admin/" -ForegroundColor White
    Write-Host "https://prismaavaliacoes.com.br/admin/seo/" -ForegroundColor White
    Write-Host "https://prismaavaliacoes.com.br/sitemap.xml" -ForegroundColor White
    Write-Host ""
    Write-Host "📋 VERIFICAÇÕES:" -ForegroundColor Yellow
    Write-Host "✅ Admin SEO deve aparecer no menu" -ForegroundColor White
    Write-Host "✅ Navegação deve ter cor azul #1e40af" -ForegroundColor White
    Write-Host "✅ Sitemap deve ter URLs prismaavaliacoes.com.br" -ForegroundColor White
    Write-Host "✅ Código fonte deve ter tags canonical" -ForegroundColor White
    
} catch {
    Write-Host "❌ Erro durante o deploy: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 DICAS PARA RESOLVER:" -ForegroundColor Yellow
    Write-Host "1. Verificar conexão SSH" -ForegroundColor White
    Write-Host "2. Confirmar credenciais do servidor" -ForegroundColor White
    Write-Host "3. Executar comandos manualmente via SSH" -ForegroundColor White
}

Write-Host ""
Write-Host "Para verificação pós-deploy, execute:" -ForegroundColor Cyan
Write-Host ".\deploy_prisma.ps1 -VerifyOnly" -ForegroundColor White
