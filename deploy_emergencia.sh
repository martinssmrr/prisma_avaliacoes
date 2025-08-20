#!/bin/bash

# =============================================================================
# SCRIPT DE EMERGÊNCIA - DEPLOY PYTHONANYWHERE
# =============================================================================
# Execute este script no console Bash do PythonAnywhere para corrigir o erro

echo "🚨 SCRIPT DE EMERGÊNCIA - Corrigindo ALLOWED_HOSTS"
echo "=================================================="

# Navegar para o diretório do projeto
cd ~/prisma_avaliacoes || { echo "❌ Erro: Diretório não encontrado"; exit 1; }

echo "📁 Diretório atual: $(pwd)"

# Atualizar código do repositório
echo "🔄 Atualizando código do repositório..."
git pull origin master

# Verificar se arquivo .env existe
if [ ! -f .env ]; then
    echo "📝 Criando arquivo .env de produção..."
    cat > .env << 'EOF'
SECRET_KEY=django-insecure-(=-&$c%lq2!cxtmdwinj4uw&yftv$0*jsgn*)ew)%accjk@gk$
DEBUG=False
ALLOWED_HOSTS=prismaav.pythonanywhere.com,localhost,127.0.0.1
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DJANGO_SUPERUSER_USERNAME=prismaav
DJANGO_SUPERUSER_PASSWORD=PrismaAv4002@--
DJANGO_SUPERUSER_EMAIL=admin@prismaavaliacoes.com
EOF
    echo "✅ Arquivo .env criado"
else
    echo "📋 Arquivo .env já existe"
fi

# Verificar conteúdo do ALLOWED_HOSTS
echo "🔍 Verificando ALLOWED_HOSTS..."
grep "ALLOWED_HOSTS" .env

# Instalar/atualizar dependências
echo "📦 Instalando dependências..."
pip install --user -r requirements.txt

# Executar migrações
echo "🗄️ Executando migrações..."
python manage.py migrate --settings=setup.production_settings

# Coletar arquivos estáticos
echo "📂 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --settings=setup.production_settings

# Verificar configuração
echo "🔧 Verificando configuração..."
python manage.py check --settings=setup.production_settings

# Testar ALLOWED_HOSTS
echo "🧪 Testando ALLOWED_HOSTS..."
python -c "
import os
import sys
import django

# Adicionar path do projeto
sys.path.insert(0, '/home/prismaav/prisma_avaliacoes')

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.production_settings')
django.setup()

from django.conf import settings
print('✅ ALLOWED_HOSTS configurado:', settings.ALLOWED_HOSTS)
print('✅ DEBUG:', settings.DEBUG)
"

echo ""
echo "=================================================="
echo "✅ SCRIPT EXECUTADO COM SUCESSO!"
echo "=================================================="
echo ""
echo "🔄 PRÓXIMO PASSO OBRIGATÓRIO:"
echo "1. Vá para a aba 'Web' no PythonAnywhere"
echo "2. Clique no botão verde 'Reload prismaav.pythonanywhere.com'"
echo "3. Aguarde alguns segundos"
echo "4. Teste: https://prismaav.pythonanywhere.com"
echo ""
echo "📞 Se o problema persistir:"
echo "1. Verifique o Error log na aba Web"
echo "2. Confirme se o arquivo WSGI está correto"
echo "3. Execute: python config_pythonanywhere.py"
echo ""
