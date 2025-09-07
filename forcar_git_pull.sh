#!/bin/bash
# Script para FORÇAR atualização quando git pull não funciona

echo "🚀 FORÇANDO ATUALIZAÇÃO DO GIT"
echo "=============================="

cd /var/www/prisma_avaliacoes || {
    echo "❌ Erro: Diretório não encontrado"
    exit 1
}

# 1. Backup completo antes de qualquer mudança
echo "💾 Criando backup de segurança..."
backup_name="backup_antes_forcaer_git_$(date +%Y%m%d_%H%M%S)"
tar -czf "/tmp/$backup_name.tar.gz" . 2>/dev/null
echo "✅ Backup criado: /tmp/$backup_name.tar.gz"

# 2. Salvar mudanças locais se houver
echo ""
echo "💼 Salvando mudanças locais..."
if ! git diff-index --quiet HEAD --; then
    echo "⚠️ Há mudanças locais, salvando..."
    git stash push -m "Backup automático antes de forçar pull - $(date)"
    echo "✅ Mudanças salvas no stash"
else
    echo "✅ Nenhuma mudança local para salvar"
fi

# 3. Limpar arquivos não rastreados
echo ""
echo "🧹 Limpando arquivos não rastreados..."
git clean -fd 2>/dev/null || echo "Nenhum arquivo para limpar"

# 4. FORÇAR fetch do repositório remoto
echo ""
echo "📥 Forçando fetch do repositório..."
git fetch origin --force 2>&1

# 5. Resetar para o commit remoto (FORÇA atualização)
echo ""
echo "🔄 FORÇANDO reset para origin/master..."
git reset --hard origin/master 2>&1

# Verificar se deu certo
if [ $? -eq 0 ]; then
    echo "✅ Reset forçado com sucesso"
else
    echo "❌ Erro no reset, tentando abordagem alternativa..."
    
    # Abordagem alternativa: re-clonar
    echo "🔄 Tentando re-clonar repositório..."
    
    cd /var/www
    mv prisma_avaliacoes "prisma_avaliacoes_old_$(date +%Y%m%d_%H%M%S)"
    
    git clone https://github.com/martinssmrr/prisma_avaliacoes.git
    
    if [ $? -eq 0 ]; then
        echo "✅ Repositório re-clonado com sucesso"
        cd prisma_avaliacoes
    else
        echo "❌ Erro ao re-clonar, restaurando backup..."
        mv prisma_avaliacoes_old_* prisma_avaliacoes
        cd prisma_avaliacoes
    fi
fi

# 6. Verificar se arquivos específicos existem
echo ""
echo "📁 Verificando arquivos atualizados:"
files_to_check=(
    "corrigir_sem_logs.sh"
    "diagnosticar_servidor.sh" 
    "CORRIGIR_EXAMPLE_COM_URGENTE.md"
    "simple_sitemap.py"
)

for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file encontrado"
    else
        echo "❌ $file NÃO encontrado"
    fi
done

# 7. Verificar último commit
echo ""
echo "📝 Último commit após atualização:"
git log --oneline -1 2>/dev/null

# 8. Verificar se estamos na branch correta
echo ""
echo "🌿 Branch atual:"
git branch 2>/dev/null | grep '*'

# 9. Listar arquivos modificados recentemente
echo ""
echo "📅 Arquivos modificados recentemente:"
find . -name "*.py" -o -name "*.sh" -o -name "*.md" | head -10 | xargs ls -la

echo ""
echo "=============================="
echo "🎉 ATUALIZAÇÃO FORÇADA CONCLUÍDA"
echo "=============================="
echo ""
echo "📋 PRÓXIMOS PASSOS:"
echo "1. Verificar se arquivos esperados existem"
echo "2. Executar script de correção do sitemap"
echo "3. Testar funcionamento"
echo ""
echo "💡 Se problemas persistirem:"
echo "- Verificar permissões: ls -la"
echo "- Verificar proprietário: chown -R root:root ."
echo "- Executar: bash corrigir_sem_logs.sh"
