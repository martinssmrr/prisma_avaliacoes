#!/bin/bash
# Script para diagnosticar e resolver problemas do Git no servidor

echo "🔍 DIAGNÓSTICO DO GIT NO SERVIDOR"
echo "================================="

cd /var/www/prisma_avaliacoes || {
    echo "❌ Erro: Diretório /var/www/prisma_avaliacoes não encontrado"
    exit 1
}

echo "📁 Diretório atual: $(pwd)"

# 1. Verificar status do repositório Git
echo ""
echo "📊 STATUS DO REPOSITÓRIO:"
echo "========================"

if [ -d ".git" ]; then
    echo "✅ Repositório Git encontrado"
    
    # Verificar configuração remota
    echo ""
    echo "🔗 Repositórios remotos:"
    git remote -v
    
    # Verificar branch atual
    echo ""
    echo "🌿 Branch atual:"
    git branch -a
    
    # Verificar status
    echo ""
    echo "📋 Status do Git:"
    git status
    
    # Verificar últimos commits
    echo ""
    echo "📝 Últimos commits locais:"
    git log --oneline -5
    
    # Verificar se há mudanças locais
    echo ""
    echo "🔍 Verificando mudanças locais:"
    if git diff-index --quiet HEAD --; then
        echo "✅ Nenhuma mudança local"
    else
        echo "⚠️ Há mudanças locais não commitadas:"
        git diff --name-only
    fi
    
    # Verificar arquivos não rastreados
    untracked=$(git ls-files --others --exclude-standard)
    if [ -z "$untracked" ]; then
        echo "✅ Nenhum arquivo não rastreado"
    else
        echo "⚠️ Arquivos não rastreados:"
        echo "$untracked"
    fi
    
else
    echo "❌ Este não é um repositório Git!"
    echo "Verificando se há arquivos .git em outros locais..."
    find /var/www -name ".git" -type d 2>/dev/null
fi

# 2. Testar conectividade com GitHub
echo ""
echo "🌐 TESTANDO CONECTIVIDADE:"
echo "=========================="

echo "Testando conexão com GitHub..."
if ping -c 1 github.com &>/dev/null; then
    echo "✅ Conectividade com GitHub: OK"
else
    echo "❌ Sem conectividade com GitHub"
fi

# Testar SSH (se configurado)
echo ""
echo "🔑 Testando SSH do GitHub:"
ssh -T git@github.com -o StrictHostKeyChecking=no 2>&1 | head -3

# 3. Verificar espaço em disco
echo ""
echo "💾 ESPAÇO EM DISCO:"
echo "=================="
df -h /var/www

# 4. Verificar permissões
echo ""
echo "🔒 PERMISSÕES:"
echo "=============="
ls -la /var/www/prisma_avaliacoes/ | head -10

# 5. Tentar fetch manual
echo ""
echo "📥 TENTANDO FETCH MANUAL:"
echo "========================"
git fetch origin 2>&1 || echo "❌ Erro no git fetch"

# 6. Comparar commits remotos vs locais
echo ""
echo "📊 COMPARAÇÃO REMOTO vs LOCAL:"
echo "=============================="
echo "Último commit local:"
git log --oneline -1 2>/dev/null

echo ""
echo "Último commit remoto (origin/master):"
git log --oneline -1 origin/master 2>/dev/null

echo ""
echo "Commits à frente do remoto:"
git log --oneline origin/master..HEAD 2>/dev/null || echo "Nenhum ou erro"

echo ""
echo "Commits atrás do remoto:"
git log --oneline HEAD..origin/master 2>/dev/null || echo "Nenhum ou erro"

echo ""
echo "================================="
echo "📋 DIAGNÓSTICO CONCLUÍDO"
echo "================================="
echo ""
echo "🔧 POSSÍVEIS SOLUÇÕES:"
echo "1. Se há mudanças locais: git stash"
echo "2. Se está desatualizado: git reset --hard origin/master"
echo "3. Se há problemas de permissão: chown -R user:group ."
echo "4. Se não é repositório: git clone [URL]"
echo "5. Execute o script de correção: bash forcar_git_pull.sh"
