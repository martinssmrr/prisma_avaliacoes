# PowerShell Script para corrigir produção remotamente
# Execute este script se tiver PuTTY/plink configurado

param(
    [string]$Server = "srv989739.hstgr.cloud",
    [string]$User = "root"
)

Write-Host "=== CORREÇÃO DJANGO PRODUÇÃO ===" -ForegroundColor Yellow
Write-Host "Servidor: $Server" -ForegroundColor Cyan
Write-Host "Usuário: $User" -ForegroundColor Cyan
Write-Host ""

# Verificar se plink está disponível
$plinkPath = Get-Command plink -ErrorAction SilentlyContinue

if ($plinkPath) {
    Write-Host "✅ PuTTY plink encontrado" -ForegroundColor Green
    
    $commands = @(
        "cd /var/www/html/prismaavaliacoes.com.br",
        "echo '🔍 Verificando problema...'",
        "ls -la setup/ | grep settings",
        "echo '💾 Fazendo backup...'",
        "cp -r . ../backup_$(date +%Y%m%d_%H%M%S)",
        "echo '📥 Atualizando Git...'",
        "git fetch origin master",
        "git reset --hard origin/master",
        "echo '🔧 Corrigindo conflito settings...'",
        "if [ -d 'setup/settings' ]; then mv setup/settings setup/settings_backup_$(date +%Y%m%d_%H%M%S); echo 'Conflito resolvido'; fi",
        "echo '🐍 Ativando ambiente virtual...'",
        "source venv/bin/activate",
        "echo '🧪 Testando configuração...'",
        "python manage.py check --settings=setup.settings",
        "echo '🔄 Aplicando migrações...'",
        "python manage.py migrate --settings=setup.settings",
        "echo '🔄 Reiniciando serviços...'",
        "systemctl reload nginx",
        "systemctl restart gunicorn",
        "echo '✅ Correção concluída!'"
    )
    
    foreach ($cmd in $commands) {
        Write-Host "Executando: $cmd" -ForegroundColor Yellow
        & plink -ssh "$User@$Server" $cmd
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Erro ao executar: $cmd" -ForegroundColor Red
        }
    }
    
} else {
    Write-Host "❌ PuTTY plink não encontrado" -ForegroundColor Red
    Write-Host ""
    Write-Host "OPÇÕES ALTERNATIVAS:" -ForegroundColor Yellow
    Write-Host "1. Instalar PuTTY e configurar keys SSH"
    Write-Host "2. Usar cliente SSH manual (PuTTY GUI)"
    Write-Host "3. Executar comandos manualmente via SSH"
    Write-Host ""
    Write-Host "COMANDOS PARA EXECUTAR MANUALMENTE:" -ForegroundColor Cyan
    Write-Host "ssh root@srv989739.hstgr.cloud" -ForegroundColor White
    Write-Host "cd /var/www/html/prismaavaliacoes.com.br" -ForegroundColor White
    Write-Host "git fetch origin master && git reset --hard origin/master" -ForegroundColor White
    Write-Host "mv setup/settings setup/settings_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')" -ForegroundColor White
    Write-Host "source venv/bin/activate" -ForegroundColor White
    Write-Host "python manage.py migrate --settings=setup.settings" -ForegroundColor White
    Write-Host "systemctl restart gunicorn && systemctl reload nginx" -ForegroundColor White
}

Write-Host ""
Write-Host "=== VERIFICAÇÃO PÓS-CORREÇÃO ===" -ForegroundColor Yellow
Write-Host "🌐 Admin: https://prismaavaliacoes.com.br/admin/" -ForegroundColor Green
Write-Host "🔧 SEO: https://prismaavaliacoes.com.br/admin/seo/" -ForegroundColor Green
Write-Host "🗺️ Sitemap: https://prismaavaliacoes.com.br/sitemap.xml" -ForegroundColor Green
