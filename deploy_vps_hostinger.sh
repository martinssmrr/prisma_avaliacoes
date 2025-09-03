#!/bin/bash

# =============================================================================
# SCRIPT DE DEPLOY COMPLETO - PRISMA AVALIAÇÕES VPS HOSTINGER
# Execute este script no VPS para fazer deploy automático
# =============================================================================

echo "🚀 INICIANDO DEPLOY AUTOMÁTICO - PRISMA AVALIAÇÕES"
echo "=================================================="

# Verificar se estamos como root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Execute como root: sudo su"
    exit 1
fi

# =============================================================================
# 1. PREPARAR SISTEMA
# =============================================================================

echo "📦 Atualizando sistema..."
apt update && apt upgrade -y

echo "📦 Instalando dependências..."
apt install python3-pip python3-venv python3-dev build-essential \
    libssl-dev libpq-dev nginx certbot python3-certbot-nginx \
    git curl wget htop nano vim unzip tree -y

# =============================================================================
# 2. CONFIGURAR PROJETO
# =============================================================================

echo "📁 Configurando projeto..."

# Criar diretório
mkdir -p /var/www/prisma_avaliacoes
cd /var/www/prisma_avaliacoes

# OPÇÃO 1: Se você fez upload via SCP
if [ -f "/tmp/prisma_projeto.zip" ]; then
    echo "📦 Extraindo projeto do ZIP..."
    unzip /tmp/prisma_projeto.zip -d /var/www/
    mv "/var/www/Prisma Avaliações Imobiliarias"/* /var/www/prisma_avaliacoes/
    rmdir "/var/www/Prisma Avaliações Imobiliarias"
fi

# OPÇÃO 2: Clone do GitHub
if [ ! -f "manage.py" ]; then
    echo "📦 Clonando projeto do GitHub..."
    git clone https://github.com/martinssmrr/prisma_avaliacoes.git .
fi

# Verificar se projeto existe
if [ ! -f "manage.py" ]; then
    echo "❌ Erro: manage.py não encontrado!"
    echo "📋 Faça upload do projeto ou clone do GitHub primeiro"
    exit 1
fi

echo "✅ Projeto encontrado: $(pwd)"

# =============================================================================
# 3. CONFIGURAR AMBIENTE PYTHON
# =============================================================================

echo "🐍 Configurando ambiente Python..."

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Atualizar pip
pip install --upgrade pip

# Instalar dependências
if [ -f "requirements_vps.txt" ]; then
    pip install -r requirements_vps.txt
else
    # Instalar dependências básicas
    pip install Django==5.2.5 gunicorn==21.2.0 django-jazzmin==3.0.1 \
                Pillow python-decouple pytz cryptography requests whitenoise
fi

echo "✅ Ambiente Python configurado!"

# =============================================================================
# 4. CONFIGURAR DJANGO
# =============================================================================

echo "⚙️ Configurando Django..."

# Criar diretório de logs
mkdir -p logs
mkdir -p /var/log/gunicorn

# Copiar arquivo .env se existir
if [ -f ".env.production" ]; then
    cp .env.production .env
fi

# Executar migrações
echo "🗄️ Executando migrações..."
python manage.py migrate --settings=setup.settings.vps_hostinger

# Coletar arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --settings=setup.settings.vps_hostinger

# Criar superusuário se não existir
echo "👤 Configurando superusuário..."
python manage.py shell --settings=setup.settings.vps_hostinger << 'EOF'
from django.contrib.auth.models import User
import os

username = 'prismaav'
email = 'contato@prismaavaliacoes.com.br'
password = 'PrismaAv4002@--'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"✅ Superusuário '{username}' criado!")
else:
    print(f"ℹ️ Superusuário '{username}' já existe.")
EOF

echo "✅ Django configurado!"

# =============================================================================
# 5. CONFIGURAR GUNICORN
# =============================================================================

echo "🔥 Configurando Gunicorn..."

# Copiar arquivo de serviço
if [ -f "config/gunicorn.service" ]; then
    cp config/gunicorn.service /etc/systemd/system/
else
    # Criar arquivo de serviço
    cat << 'GUNICORN_EOF' > /etc/systemd/system/gunicorn.service
[Unit]
Description=gunicorn daemon for Prisma Avaliações
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/prisma_avaliacoes
Environment="PATH=/var/www/prisma_avaliacoes/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=setup.settings.vps_hostinger"
ExecStart=/var/www/prisma_avaliacoes/venv/bin/gunicorn \
    --access-logfile /var/log/gunicorn/access.log \
    --error-logfile /var/log/gunicorn/error.log \
    --workers 3 \
    --worker-class gthread \
    --threads 2 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 30 \
    --keep-alive 2 \
    --bind unix:/var/www/prisma_avaliacoes/gunicorn.sock \
    setup.wsgi:application

ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
GUNICORN_EOF
fi

# Ativar e iniciar serviço
systemctl daemon-reload
systemctl enable gunicorn
systemctl start gunicorn

echo "📊 Status do Gunicorn:"
systemctl status gunicorn --no-pager -l

echo "✅ Gunicorn configurado!"

# =============================================================================
# 6. CONFIGURAR NGINX
# =============================================================================

echo "🌐 Configurando Nginx..."

# Copiar configuração do site
if [ -f "config/nginx_prismaavaliacoes.conf" ]; then
    cp config/nginx_prismaavaliacoes.conf /etc/nginx/sites-available/prismaavaliacoes
else
    # Criar configuração básica
    cat << 'NGINX_EOF' > /etc/nginx/sites-available/prismaavaliacoes
server {
    listen 80;
    server_name www.prismaavaliacoes.com.br prismaavaliacoes.com.br;
    
    access_log /var/log/nginx/prismaavaliacoes_access.log;
    error_log /var/log/nginx/prismaavaliacoes_error.log;

    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /static/ {
        alias /var/www/prisma_avaliacoes/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/prisma_avaliacoes/media/;
        expires 30d;
        add_header Cache-Control "public";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/prisma_avaliacoes/gunicorn.sock;
        
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    client_max_body_size 50M;
}
NGINX_EOF
fi

# Ativar site
ln -sf /etc/nginx/sites-available/prismaavaliacoes /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Testar e reiniciar nginx
nginx -t && systemctl restart nginx && systemctl enable nginx

echo "✅ Nginx configurado!"

# =============================================================================
# 7. CONFIGURAR PERMISSÕES
# =============================================================================

echo "🔐 Configurando permissões..."

chown -R root:www-data /var/www/prisma_avaliacoes/
chmod -R 755 /var/www/prisma_avaliacoes/
chmod 664 /var/www/prisma_avaliacoes/db.sqlite3 2>/dev/null || true

chown -R www-data:www-data /var/log/gunicorn/
chmod -R 755 /var/log/gunicorn/

echo "✅ Permissões configuradas!"

# =============================================================================
# 8. CONFIGURAR SSL
# =============================================================================

echo "🔒 Configurando SSL..."

# Configurar firewall
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable

# Instalar certificado SSL
certbot --nginx -d prismaavaliacoes.com.br -d www.prismaavaliacoes.com.br \
    --non-interactive --agree-tos --email contato@prismaavaliacoes.com.br

# Recarregar nginx
systemctl reload nginx

# Configurar renovação automática
(crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -

echo "✅ SSL configurado!"

# =============================================================================
# 9. VERIFICAÇÕES FINAIS
# =============================================================================

echo "🔍 Verificações finais..."

echo "Status dos serviços:"
echo "- Gunicorn: $(systemctl is-active gunicorn)"
echo "- Nginx: $(systemctl is-active nginx)"

echo "Testando conectividade:"
curl -s -o /dev/null -w "%{http_code}" http://localhost/ || echo "Erro na conectividade local"

# =============================================================================
# 10. RESUMO FINAL
# =============================================================================

echo ""
echo "🎉 DEPLOY CONCLUÍDO COM SUCESSO!"
echo "=================================================="
echo ""
echo "🌐 SITE:"
echo "- HTTP: http://www.prismaavaliacoes.com.br"
echo "- HTTPS: https://www.prismaavaliacoes.com.br"
echo ""
echo "📊 ADMIN:"
echo "- URL: https://www.prismaavaliacoes.com.br/admin/"
echo "- Usuário: prismaav"
echo "- Senha: PrismaAv4002@--"
echo ""
echo "📁 LOCALIZAÇÃO:"
echo "- Projeto: /var/www/prisma_avaliacoes/"
echo "- Logs: /var/log/gunicorn/ e /var/log/nginx/"
echo ""
echo "🔧 COMANDOS ÚTEIS:"
echo "- Reiniciar: systemctl restart gunicorn nginx"
echo "- Logs: tail -f /var/log/gunicorn/error.log"
echo "- Status: systemctl status gunicorn nginx"
echo ""
echo "🔄 ATUALIZAR PROJETO:"
echo "cd /var/www/prisma_avaliacoes"
echo "source venv/bin/activate"
echo "git pull  # ou reupload arquivos"
echo "python manage.py migrate --settings=setup.settings.vps_hostinger"
echo "python manage.py collectstatic --noinput --settings=setup.settings.vps_hostinger"
echo "systemctl restart gunicorn"
echo ""
