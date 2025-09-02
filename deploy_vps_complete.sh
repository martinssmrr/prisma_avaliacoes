#!/bin/bash

# =============================================================================
# SCRIPT DE DEPLOY COMPLETO - VPS UBUNTU 24.04 + NGINX + GUNICORN
# Prisma Avaliações - www.prismaavaliacoes.com.br
# =============================================================================

set -e  # Sair em caso de erro

echo "🚀 INICIANDO DEPLOY NO VPS UBUNTU 24.04"
echo "=================================================="

# =============================================================================
# 1. ATUALIZAR SISTEMA E INSTALAR DEPENDÊNCIAS
# =============================================================================

echo "📦 Atualizando sistema e instalando dependências..."
apt update && apt upgrade -y
apt install python3-pip python3-venv python3-dev build-essential \
    libssl-dev libpq-dev nginx certbot python3-certbot-nginx \
    git curl wget htop nano vim supervisor -y

# Instalar Node.js (se necessário para frontend)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt-get install -y nodejs

echo "✅ Dependências instaladas com sucesso!"

# =============================================================================
# 2. CONFIGURAR ESTRUTURA DO PROJETO
# =============================================================================

echo "📁 Configurando estrutura do projeto..."

# Criar diretórios
mkdir -p /var/www/Prisma_Avaliacoes
mkdir -p /var/log/gunicorn
mkdir -p /var/log/nginx
mkdir -p /var/www/Prisma_Avaliacoes/logs

# Navegar para diretório do projeto
cd /var/www/Prisma_Avaliacoes

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Atualizar pip
pip install --upgrade pip

echo "✅ Estrutura do projeto configurada!"

# =============================================================================
# 3. INSTALAR DEPENDÊNCIAS PYTHON
# =============================================================================

echo "🐍 Instalando dependências Python..."

# Instalar dependências básicas
pip install django==5.2.5 gunicorn==21.2.0 django-jazzmin==3.0.1
pip install Pillow python-decouple pytz cryptography requests

# Se usar PostgreSQL:
# pip install psycopg2-binary

echo "✅ Dependências Python instaladas!"

# =============================================================================
# 4. CONFIGURAR DJANGO
# =============================================================================

echo "⚙️ Configurando Django..."

# Definir variável de ambiente
export DJANGO_SETTINGS_MODULE=setup.settings.vps_production

# Executar migrações
python manage.py migrate --settings=setup.settings.vps_production

# Coletar arquivos estáticos
python manage.py collectstatic --noinput --settings=setup.settings.vps_production

# Criar superusuário (opcional - pode ser feito depois)
echo "Criando superusuário..."
cat << EOF | python manage.py shell --settings=setup.settings.vps_production
from django.contrib.auth.models import User
if not User.objects.filter(username='prismaav').exists():
    User.objects.create_superuser('prismaav', 'contato@prismaavaliacoes.com.br', 'PrismaAv4002@--')
    print("Superusuário 'prismaav' criado!")
else:
    print("Superusuário 'prismaav' já existe.")
EOF

echo "✅ Django configurado!"

# =============================================================================
# 5. CONFIGURAR GUNICORN
# =============================================================================

echo "🔥 Configurando Gunicorn..."

# Copiar arquivo de serviço
cat << 'EOF' > /etc/systemd/system/gunicorn.service
[Unit]
Description=gunicorn daemon for Prisma Avaliações
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/Prisma_Avaliacoes
Environment="PATH=/var/www/Prisma_Avaliacoes/venv/bin"
ExecStart=/var/www/Prisma_Avaliacoes/venv/bin/gunicorn \
    --access-logfile /var/log/gunicorn/access.log \
    --error-logfile /var/log/gunicorn/error.log \
    --workers 3 \
    --worker-class gthread \
    --threads 2 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 30 \
    --keep-alive 2 \
    --bind unix:/var/www/Prisma_Avaliacoes/gunicorn.sock \
    setup.wsgi:application

ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

# Recarregar systemd e iniciar serviço
systemctl daemon-reload
systemctl start gunicorn
systemctl enable gunicorn

# Verificar status
systemctl status gunicorn --no-pager

echo "✅ Gunicorn configurado e em execução!"

# =============================================================================
# 6. CONFIGURAR NGINX
# =============================================================================

echo "🌐 Configurando Nginx..."

# Criar configuração do site
cat << 'EOF' > /etc/nginx/sites-available/prismaavaliacoes
server {
    listen 80;
    server_name www.prismaavaliacoes.com.br prismaavaliacoes.com.br;
    
    # Logs
    access_log /var/log/nginx/prismaavaliacoes_access.log;
    error_log /var/log/nginx/prismaavaliacoes_error.log;

    # Favicon
    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Arquivos estáticos
    location /static/ {
        alias /var/www/Prisma_Avaliacoes/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Arquivos de media
    location /media/ {
        alias /var/www/Prisma_Avaliacoes/media/;
        expires 30d;
        add_header Cache-Control "public";
    }

    # Proxy para Gunicorn
    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/Prisma_Avaliacoes/gunicorn.sock;
        
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Limitar tamanho de upload
    client_max_body_size 50M;
}
EOF

# Ativar site
ln -sf /etc/nginx/sites-available/prismaavaliacoes /etc/nginx/sites-enabled/

# Remover site padrão
rm -f /etc/nginx/sites-enabled/default

# Testar configuração
nginx -t

# Reiniciar nginx
systemctl restart nginx
systemctl enable nginx

echo "✅ Nginx configurado!"

# =============================================================================
# 7. CONFIGURAR PERMISSÕES
# =============================================================================

echo "🔐 Configurando permissões..."

# Alterar proprietário dos arquivos
chown -R root:www-data /var/www/Prisma_Avaliacoes/
chmod -R 755 /var/www/Prisma_Avaliacoes/

# Permissões específicas
chmod 664 /var/www/Prisma_Avaliacoes/db.sqlite3
chmod 755 /var/www/Prisma_Avaliacoes/manage.py

# Permissões para logs
chown -R www-data:www-data /var/log/gunicorn/
chmod -R 755 /var/log/gunicorn/

echo "✅ Permissões configuradas!"

# =============================================================================
# 8. CONFIGURAR SSL COM CERTBOT
# =============================================================================

echo "🔒 Configurando SSL com Let's Encrypt..."

# Obter certificado SSL
certbot --nginx -d prismaavaliacoes.com.br -d www.prismaavaliacoes.com.br --non-interactive --agree-tos --email contato@prismaavaliacoes.com.br

# Recarregar nginx
systemctl reload nginx

# Configurar renovação automática
(crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -

echo "✅ SSL configurado!"

# =============================================================================
# 9. CRIAR SCRIPT DE ATUALIZAÇÃO
# =============================================================================

echo "📝 Criando script de atualização..."

cat << 'EOF' > /var/www/Prisma_Avaliacoes/update.sh
#!/bin/bash
# Script para atualizar o projeto

cd /var/www/Prisma_Avaliacoes
source venv/bin/activate

echo "🔄 Atualizando código..."
git pull origin main

echo "📦 Instalando dependências..."
pip install -r requirements_vps.txt

echo "🗄️ Executando migrações..."
python manage.py migrate --settings=setup.settings.vps_production

echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --settings=setup.settings.vps_production

echo "🔄 Reiniciando serviços..."
systemctl restart gunicorn
systemctl reload nginx

echo "✅ Atualização concluída!"
EOF

chmod +x /var/www/Prisma_Avaliacoes/update.sh

# =============================================================================
# 10. VERIFICAÇÕES FINAIS
# =============================================================================

echo "🔍 Realizando verificações finais..."

# Verificar status dos serviços
echo "Status do Gunicorn:"
systemctl is-active gunicorn

echo "Status do Nginx:"
systemctl is-active nginx

# Testar conectividade
echo "Testando conectividade local:"
curl -I http://localhost/ || echo "Erro na conectividade local"

# =============================================================================
# 11. RESUMO FINAL
# =============================================================================

echo ""
echo "🎉 DEPLOY CONCLUÍDO COM SUCESSO!"
echo "=================================================="
echo ""
echo "🌐 SITE DISPONÍVEL EM:"
echo "- HTTP: http://www.prismaavaliacoes.com.br"
echo "- HTTPS: https://www.prismaavaliacoes.com.br"
echo ""
echo "📊 ADMIN DISPONÍVEL EM:"
echo "- https://www.prismaavaliacoes.com.br/admin/"
echo "- Usuário: prismaav"
echo "- Senha: PrismaAv4002@--"
echo ""
echo "📁 LOCALIZAÇÃO DOS ARQUIVOS:"
echo "- Projeto: /var/www/Prisma_Avaliacoes/"
echo "- Logs Gunicorn: /var/log/gunicorn/"
echo "- Logs Nginx: /var/log/nginx/"
echo ""
echo "🔧 COMANDOS ÚTEIS:"
echo "- Reiniciar Gunicorn: systemctl restart gunicorn"
echo "- Reiniciar Nginx: systemctl restart nginx"
echo "- Ver logs: tail -f /var/log/gunicorn/error.log"
echo "- Atualizar projeto: /var/www/Prisma_Avaliacoes/update.sh"
echo ""
echo "✅ DEPLOY FINALIZADO!"
