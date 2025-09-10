# Script PowerShell para corrigir SEO 404 no admin
# Execute este script no Windows PowerShell

param(
    [string]$Server = "srv989739.hstgr.cloud",
    [string]$User = "root"
)

Write-Host "🔧 CORREÇÃO SEO 404 - PRISMA AVALIAÇÕES" -ForegroundColor Yellow
Write-Host "=======================================" -ForegroundColor Yellow
Write-Host "Servidor: $Server" -ForegroundColor Cyan
Write-Host "URL com erro: https://prismaavaliacoes.com.br/admin/seo/" -ForegroundColor Red
Write-Host ""

# Verificar se SSH está disponível
if (-not (Get-Command ssh -ErrorAction SilentlyContinue)) {
    Write-Host "❌ SSH não encontrado" -ForegroundColor Red
    Write-Host "Instale OpenSSH: winget install Microsoft.OpenSSH.Beta" -ForegroundColor Yellow
    exit 1
}

Write-Host "🔍 1. VERIFICANDO STATUS ATUAL..." -ForegroundColor Green

# Verificar conectividade
$statusCheck = @"
cd /var/www/html/prismaavaliacoes.com.br
source venv/bin/activate
echo "=== DIAGNÓSTICO RÁPIDO ==="
echo "Diretório atual: \$(pwd)"
echo "App SEO existe: \$([ -d 'seo' ] && echo 'SIM' || echo 'NÃO')"
echo "SEO em settings: \$(grep -q 'seo' setup/settings.py && echo 'SIM' || echo 'NÃO')"
echo "Status admin SEO: \$(curl -s -o /dev/null -w '%{http_code}' https://prismaavaliacoes.com.br/admin/seo/)"
echo "=========================="
"@

Write-Host "Executando verificação..." -ForegroundColor Cyan
ssh "$User@$Server" $statusCheck

Write-Host ""
Write-Host "🔧 2. APLICANDO CORREÇÃO..." -ForegroundColor Green

# Script de correção completa
$fixScript = @"
cd /var/www/html/prismaavaliacoes.com.br
source venv/bin/activate

echo "📍 Verificando estrutura..."
ls -la seo/ | head -5

echo "🔍 Verificando INSTALLED_APPS..."
if grep -q "'seo'" setup/settings.py; then
    echo "✅ SEO encontrado em INSTALLED_APPS"
else
    echo "❌ SEO não encontrado em INSTALLED_APPS"
    echo "🔧 Adicionando SEO..."
    
    # Backup do settings
    cp setup/settings.py setup/settings.py.backup_\$(date +%Y%m%d_%H%M%S)
    
    # Adicionar 'seo' antes do fechamento da lista INSTALLED_APPS
    sed -i "/INSTALLED_APPS = \[/,/\]/ {
        /\]/i\\    'seo',
    }" setup/settings.py
    
    echo "✅ SEO adicionado ao INSTALLED_APPS"
fi

echo "🔧 Criando migrações SEO..."
python manage.py makemigrations seo --settings=setup.settings

echo "💽 Aplicando migrações..."
python manage.py migrate --settings=setup.settings

echo "🔄 Reiniciando Gunicorn..."
systemctl restart gunicorn

echo "⏱️ Aguardando estabilização..."
sleep 3

echo "🧪 Testando admin SEO..."
STATUS=\$(curl -s -o /dev/null -w '%{http_code}' https://prismaavaliacoes.com.br/admin/seo/)
echo "Status final: \$STATUS"

if [ "\$STATUS" = "200" ] || [ "\$STATUS" = "302" ]; then
    echo "✅ SUCCESS! Admin SEO funcionando!"
else
    echo "⚠️ Status \$STATUS - verificar se é redirecionamento de login"
fi

echo ""
echo "🎉 CORREÇÃO CONCLUÍDA!"
echo "Teste: https://prismaavaliacoes.com.br/admin/seo/"
"@

Write-Host "Aplicando correção completa..." -ForegroundColor Cyan
ssh "$User@$Server" $fixScript

Write-Host ""
Write-Host "🧪 3. VERIFICAÇÃO FINAL..." -ForegroundColor Green

# Verificação final
$finalCheck = @"
cd /var/www/html/prismaavaliacoes.com.br
source venv/bin/activate

echo "=== VERIFICAÇÃO FINAL ==="
echo "Status dos serviços:"
echo "  Nginx: \$(systemctl is-active nginx)"
echo "  Gunicorn: \$(systemctl is-active gunicorn)"
echo ""

echo "URLs de teste:"
echo "  Admin principal: \$(curl -s -o /dev/null -w '%{http_code}' https://prismaavaliacoes.com.br/admin/)"
echo "  Admin SEO: \$(curl -s -o /dev/null -w '%{http_code}' https://prismaavaliacoes.com.br/admin/seo/)"
echo "  SEO Metas: \$(curl -s -o /dev/null -w '%{http_code}' https://prismaavaliacoes.com.br/admin/seo/seometa/)"
echo "  SEO Configs: \$(curl -s -o /dev/null -w '%{http_code}' https://prismaavaliacoes.com.br/admin/seo/seoconfig/)"
echo "========================"
"@

ssh "$User@$Server" $finalCheck

Write-Host ""
Write-Host "✅ CORREÇÃO SEO 404 CONCLUÍDA!" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "🌐 TESTE ESTAS URLs NO NAVEGADOR:" -ForegroundColor Yellow
Write-Host "https://prismaavaliacoes.com.br/admin/" -ForegroundColor White
Write-Host "https://prismaavaliacoes.com.br/admin/seo/" -ForegroundColor White
Write-Host "https://prismaavaliacoes.com.br/admin/seo/seometa/" -ForegroundColor White
Write-Host "https://prismaavaliacoes.com.br/admin/seo/seoconfig/" -ForegroundColor White
Write-Host ""
Write-Host "📋 NO ADMIN DJANGO VOCÊ DEVE VER:" -ForegroundColor Yellow
Write-Host "✅ Seção 'SEO' no menu lateral" -ForegroundColor Green
Write-Host "✅ Submenus 'SEO metas' e 'SEO configs'" -ForegroundColor Green
Write-Host ""

if ($LASTEXITCODE -eq 0) {
    Write-Host "🎉 Script executado com sucesso!" -ForegroundColor Green
} else {
    Write-Host "⚠️ Houve alguns problemas. Verifique as mensagens acima." -ForegroundColor Yellow
}
