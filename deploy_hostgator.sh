#!/bin/bash

# =============================================================================
# SCRIPT DE DEPLOY PARA HOSTGATOR - PRISMA AVALIAÇÕES
# =============================================================================

echo "🚀 Iniciando deploy no HostGator..."

# Verificar se estamos no diretório correto
if [ ! -f "manage.py" ]; then
    echo "❌ Erro: manage.py não encontrado. Execute o script no diretório raiz do projeto."
    exit 1
fi

# =============================================================================
# 1. CONFIGURAR ENVIRONMENT
# =============================================================================

echo "📋 Configurando environment..."
export DJANGO_SETTINGS_MODULE=setup.settings.production

# =============================================================================
# 2. INSTALAR DEPENDÊNCIAS
# =============================================================================

echo "📦 Instalando dependências Python..."
python3 -m pip install --user -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências"
    exit 1
fi

# =============================================================================
# 3. EXECUTAR MIGRAÇÕES
# =============================================================================

echo "🗄️ Executando migrações do banco de dados..."
python3 manage.py migrate --settings=setup.settings.production

if [ $? -ne 0 ]; then
    echo "❌ Erro ao executar migrações"
    exit 1
fi

# =============================================================================
# 4. COLETAR ARQUIVOS ESTÁTICOS
# =============================================================================

echo "📁 Coletando arquivos estáticos..."
python3 manage.py collectstatic --noinput --settings=setup.settings.production

if [ $? -ne 0 ]; then
    echo "❌ Erro ao coletar arquivos estáticos"
    exit 1
fi

# =============================================================================
# 5. CRIAR SUPERUSUÁRIO (se não existir)
# =============================================================================

echo "👤 Verificando superusuário..."
python3 manage.py shell --settings=setup.settings.production << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='prismaav').exists():
    User.objects.create_superuser('prismaav', 'contato@prismavaliacoes.com.br', 'PrismaAv4002@--')
    print("✅ Superusuário 'prismaav' criado")
else:
    print("ℹ️ Superusuário 'prismaav' já existe")
EOF

# =============================================================================
# 6. VERIFICAR CONFIGURAÇÕES
# =============================================================================

echo "🔍 Verificando configurações..."
python3 manage.py check --deploy --settings=setup.settings.production

# =============================================================================
# 7. VERIFICAR URLS
# =============================================================================

echo "🌐 Testando URLs..."
python3 manage.py shell --settings=setup.settings.production << EOF
from django.core.management import execute_from_command_line
from django.test import Client
from django.urls import reverse

try:
    client = Client()
    response = client.get('/')
    print(f"✅ Página inicial: Status {response.status_code}")
except Exception as e:
    print(f"⚠️ Erro ao testar página inicial: {e}")
EOF

# =============================================================================
# 8. CONFIGURAR PERMISSÕES
# =============================================================================

echo "🔐 Configurando permissões de arquivos..."
find . -type f -name "*.py" -exec chmod 644 {} \;
find . -type d -exec chmod 755 {} \;
chmod 644 .htaccess
chmod 644 passenger_wsgi.py
chmod 755 manage.py

# Proteger arquivo de banco de dados
if [ -f "db.sqlite3" ]; then
    chmod 600 db.sqlite3
fi

# =============================================================================
# 9. LIMPEZA
# =============================================================================

echo "🧹 Limpando arquivos temporários..."
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# =============================================================================
# 10. RESUMO FINAL
# =============================================================================

echo ""
echo "✅ DEPLOY CONCLUÍDO COM SUCESSO!"
echo ""
echo "📋 PRÓXIMOS PASSOS NO CPANEL:"
echo "1. Upload dos arquivos para /home/USERNAME/prismavaliacoes/"
echo "2. Apontar domínio para a pasta do projeto"
echo "3. Configurar AutoSSL/Let's Encrypt"
echo "4. Testar o site em https://prismavaliacoes.com.br"
echo ""
echo "🔧 CONFIGURAÇÕES IMPORTANTES:"
echo "- Ajustar USERNAME no .htaccess"
echo "- Configurar SECRET_KEY em production.py"
echo "- Configurar email no cPanel"
echo ""
echo "📊 ACESSO AO ADMIN:"
echo "- URL: https://prismavaliacoes.com.br/admin/"
echo "- Usuário: prismaav"
echo "- Senha: PrismaAv4002@-- (ALTERE IMEDIATAMENTE)"
echo ""
