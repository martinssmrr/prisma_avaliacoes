#!/bin/bash

# CORREÇÃO RÁPIDA - Git Dubious Ownership
# Resolve o erro "fatal: detected dubious ownership in repository"

echo "🔧 CORREÇÃO GIT DUBIOUS OWNERSHIP"
echo "================================="
echo "Data: $(date)"
echo ""

# Configurações
SERVER_PATH="/var/www/html/prismaavaliacoes.com.br"

echo "📍 Navegando para o diretório do projeto..."
cd "$SERVER_PATH" || exit 1

echo "🔐 Verificando ownership atual..."
ls -la . | head -5

echo ""
echo "🛠️  Aplicando correções..."

# 1. Adicionar diretório como seguro no Git
echo "1. Configurando diretório como seguro no Git..."
git config --global --add safe.directory /var/www/html/prismaavaliacoes.com.br
echo "✅ Safe directory configurado"

# 2. Verificar se Git agora funciona
echo ""
echo "2. Testando comando Git..."
if git status > /dev/null 2>&1; then
    echo "✅ Git funcionando corretamente"
else
    echo "⚠️  Git ainda com problemas, aplicando correção adicional..."
    
    # 3. Corrigir ownership se necessário
    echo "3. Corrigindo ownership dos arquivos..."
    chown -R root:root .
    echo "✅ Ownership corrigido"
    
    # 4. Testar novamente
    if git status > /dev/null 2>&1; then
        echo "✅ Git funcionando após correção de ownership"
    else
        echo "❌ Problema persiste, pode ser necessária intervenção manual"
    fi
fi

echo ""
echo "🧪 Testando comandos Git básicos..."
echo "Status:" $(git status --porcelain | wc -l) "arquivos modificados"
echo "Branch:" $(git branch --show-current)
echo "Remote:" $(git remote get-url origin)

echo ""
echo "📥 Testando fetch do repositório..."
if git fetch origin master > /dev/null 2>&1; then
    echo "✅ Fetch funcionando"
else
    echo "❌ Problema no fetch"
fi

echo ""
echo "🎉 CORREÇÃO CONCLUÍDA!"
echo "================================="
echo "Agora você pode executar os comandos Git normalmente:"
echo "  git fetch origin master"
echo "  git reset --hard origin/master"
echo ""
echo "Para continuar com o deploy, execute:"
echo "  ./deploy_hostinger_completo.sh"
