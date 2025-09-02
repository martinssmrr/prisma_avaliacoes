#!/bin/bash

# =============================================================================
# SCRIPT DE DEPLOY VIA ZIP - PRISMA AVALIAÇÕES
# Execute este script no VPS após fazer upload do ZIP
# =============================================================================

echo "🚀 INICIANDO DEPLOY VIA ZIP"
echo "=================================================="

# Verificar se estamos como root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Execute como root (sudo su)"
    exit 1
fi

# =============================================================================
# 1. PREPARAR SISTEMA
# =============================================================================

echo "📦 Preparando sistema..."
apt update && apt upgrade -y
apt install python3-pip python3-venv python3-dev build-essential \
    libssl-dev libpq-dev nginx certbot python3-certbot-nginx \
    git curl wget htop nano vim unzip -y

# =============================================================================
# 2. BAIXAR E EXTRAIR PROJETO
# =============================================================================

echo "📁 Configurando projeto..."

# Ir para diretório web
cd /var/www/

# Se já existe, fazer backup
if [ -d "Prisma_Avaliacoes" ]; then
    echo "⚠️ Fazendo backup da instalação anterior..."
    mv Prisma_Avaliacoes Prisma_Avaliacoes_backup_$(date +%Y%m%d_%H%M%S)
fi

# OPÇÃO 1: Se você fez upload manual do ZIP
if [ -f "/tmp/prisma_projeto.zip" ]; then
    echo "📦 Extraindo projeto do ZIP..."
    unzip /tmp/prisma_projeto.zip -d /var/www/
    mv "/var/www/Prisma Avaliações Imobiliarias" /var/www/Prisma_Avaliacoes
fi

# OPÇÃO 2: Download direto (se você hospedar o ZIP online)
# echo "📦 Baixando projeto..."
# wget -O prisma_projeto.zip "SUA_URL_DO_ZIP_AQUI"
# unzip prisma_projeto.zip
# mv "Prisma Avaliações Imobiliarias" Prisma_Avaliacoes

# OPÇÃO 3: Clone do Git (se disponível)
# git clone https://github.com/SEU_USUARIO/prisma_avaliacoes.git Prisma_Avaliacoes

# Verificar se projeto existe
if [ ! -d "Prisma_Avaliacoes" ]; then
    echo "❌ Erro: Projeto não encontrado!"
    echo "📋 INSTRUÇÕES:"
    echo "1. Faça upload do prisma_projeto.zip para /tmp/"
    echo "2. Ou edite este script com URL do download"
    echo "3. Execute novamente"
    exit 1
fi

cd Prisma_Avaliacoes
echo "✅ Projeto configurado em: $(pwd)"

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
    pip install django==5.2.5 gunicorn==21.2.0 django-jazzmin==3.0.1
    pip install Pillow python-decouple pytz cryptography requests
fi

echo "✅ Ambiente Python configurado!"

# =============================================================================
# 4. CONFIGURAR DJANGO
# =============================================================================

echo "⚙️ Configurando Django..."

# Definir settings
export DJANGO_SETTINGS_MODULE=setup.settings.vps_production

# Criar diretório de logs se não existir
mkdir -p logs

# Executar migrações
echo "🗄️ Executando migrações..."
python manage.py migrate --settings=setup.settings.vps_production

# Coletar arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --settings=setup.settings.vps_production

# Criar superusuário
echo "👤 Criando superusuário..."
python manage.py shell --settings=setup.settings.vps_production << 'EOF'
from django.contrib.auth.models import User
if not User.objects.filter(username='prismaav').exists():
    User.objects.create_superuser('prismaav', 'contato@prismaavaliacoes.com.br', 'PrismaAv4002@--')
    print("✅ Superusuário 'prismaav' criado!")
else:
    print("ℹ️ Superusuário 'prismaav' já existe.")
EOF

echo "✅ Django configurado!"

# =============================================================================
# 5. CONFIGURAR GUNICORN
# =============================================================================

echo "🔥 Configurando Gunicorn..."

# Criar diretório de logs
mkdir -p /var/log/gunicorn

# Criar arquivo de serviço
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

# Ativar e iniciar serviço
systemctl daemon-reload
systemctl enable gunicorn
systemctl start gunicorn

# Verificar status
echo "📊 Status do Gunicorn:"
systemctl status gunicorn --no-pager -l

echo "✅ Gunicorn configurado!"

# =============================================================================
# 6. CONFIGURAR NGINX
# =============================================================================

echo "🌐 Configurando Nginx..."

# Criar configuração do site
cat << 'EOF' > /etc/nginx/sites-available/prismaavaliacoes
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
        alias /var/www/Prisma_Avaliacoes/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/Prisma_Avaliacoes/media/;
        expires 30d;
        add_header Cache-Control "public";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/Prisma_Avaliacoes/gunicorn.sock;
        
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    client_max_body_size 50M;
}
EOF

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

chown -R root:www-data /var/www/Prisma_Avaliacoes/
chmod -R 755 /var/www/Prisma_Avaliacoes/
chmod 664 /var/www/Prisma_Avaliacoes/db.sqlite3 2>/dev/null || true

chown -R www-data:www-data /var/log/gunicorn/
chmod -R 755 /var/log/gunicorn/

echo "✅ Permissões configuradas!"

# =============================================================================
# 8. CONFIGURAR SSL
# =============================================================================

echo "🔒 Configurando SSL..."

# Instalar certificado
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
curl -s -o /dev/null -w "%{http_code}" http://localhost/ || echo "Erro na conectividade"

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
echo "- Projeto: /var/www/Prisma_Avaliacoes/"
echo "- Logs: /var/log/gunicorn/ e /var/log/nginx/"
echo ""
echo "🔧 COMANDOS ÚTEIS:"
echo "- Reiniciar: systemctl restart gunicorn nginx"
echo "- Logs: tail -f /var/log/gunicorn/error.log"
echo ""
