#!/bin/bash

echo "=== DEPLOY HOSTINGER VPS - PRISMA AVALIAÇÕES ==="

# Configurações
PROJECT_NAME="prisma_avaliacoes"
DOMAIN="prismaavaliacoes.com.br"
PROJECT_DIR="/var/www/$PROJECT_NAME"
REPO_URL="https://github.com/martinssmrr/prisma_avaliacoes.git"

echo "1. ATUALIZANDO SISTEMA:"
apt update && apt upgrade -y

echo "2. INSTALANDO DEPENDÊNCIAS DO SISTEMA:"
apt install -y python3 python3-pip python3-venv python3-dev
apt install -y nginx sqlite3
apt install -y git curl wget
apt install -y build-essential
apt install -y certbot python3-certbot-nginx

echo "3. PREPARANDO DIRETÓRIO PARA BANCO SQLITE:"
mkdir -p /var/lib/sqlite
chown www-data:www-data /var/lib/sqlite
chmod 755 /var/lib/sqlite

echo "4. CLONANDO PROJETO:"
rm -rf $PROJECT_DIR
git clone $REPO_URL $PROJECT_DIR
cd $PROJECT_DIR

echo "5. CRIANDO VIRTUAL ENVIRONMENT:"
python3 -m venv venv
source venv/bin/activate

echo "6. INSTALANDO DEPENDÊNCIAS PYTHON:"
pip install --upgrade pip
pip install -r requirements.txt

echo "7. CONFIGURANDO VARIÁVEIS DE AMBIENTE:"
cat > .env << EOF
DEBUG=False
SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN,127.0.0.1,localhost

# Database SQLite
DATABASE_PATH=/var/lib/sqlite/prisma_db.sqlite3

# Security
SECURE_SSL_REDIRECT=True
SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https
CSRF_TRUSTED_ORIGINS=https://$DOMAIN,https://www.$DOMAIN
EOF

echo "8. COPIANDO BANCO DE DADOS SQLITE DO LOCALHOST:"
# Se existe db.sqlite3 local, copia para produção
if [ -f "db.sqlite3" ]; then
    echo "Copiando banco SQLite existente..."
    cp db.sqlite3 /var/lib/sqlite/prisma_db.sqlite3
    chown www-data:www-data /var/lib/sqlite/prisma_db.sqlite3
    chmod 664 /var/lib/sqlite/prisma_db.sqlite3
    echo "✓ Banco SQLite copiado com sucesso"
else
    echo "Banco SQLite não encontrado, criando novo..."
fi

echo "9. EXECUTANDO MIGRAÇÕES:"
python manage.py makemigrations
python manage.py migrate

echo "10. COLETANDO ARQUIVOS ESTÁTICOS:"
python manage.py collectstatic --noinput

echo "11. CRIANDO SUPERUSUÁRIO (se não existir):"
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@prismaavaliacoes.com.br', 'admin123')
    print('Superusuário criado: admin/admin123')
else:
    print('Superusuário já existe')
"

echo "12. CONFIGURANDO PERMISSÕES:"
chown -R www-data:www-data $PROJECT_DIR
chmod -R 755 $PROJECT_DIR
# Permissões especiais para o banco SQLite
chown www-data:www-data /var/lib/sqlite/prisma_db.sqlite3
chmod 664 /var/lib/sqlite/prisma_db.sqlite3

echo "13. CONFIGURANDO GUNICORN SERVICE:"
cat > /etc/systemd/system/gunicorn.service << EOF
[Unit]
Description=Gunicorn daemon for Prisma Avaliações
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:$PROJECT_DIR/gunicorn.sock setup.wsgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

echo "14. INICIANDO GUNICORN:"
systemctl daemon-reload
systemctl start gunicorn
systemctl enable gunicorn

echo "15. CONFIGURANDO NGINX:"
cat > /etc/nginx/sites-available/$PROJECT_NAME << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root $PROJECT_DIR;
    }
    
    location /media/ {
        root $PROJECT_DIR;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$PROJECT_DIR/gunicorn.sock;
    }
}
EOF

# Ativar site
ln -sf /etc/nginx/sites-available/$PROJECT_NAME /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

echo "16. TESTANDO E INICIANDO NGINX:"
nginx -t
systemctl restart nginx
systemctl enable nginx

echo "17. CONFIGURANDO SSL (CERTBOT):"
certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

echo "18. CONFIGURANDO FIREWALL:"
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable

echo "19. VERIFICANDO STATUS DOS SERVIÇOS:"
systemctl status gunicorn --no-pager
systemctl status nginx --no-pager

echo "20. VERIFICANDO BANCO SQLITE:"
ls -la /var/lib/sqlite/prisma_db.sqlite3
echo "Tabelas no banco:"
sqlite3 /var/lib/sqlite/prisma_db.sqlite3 ".tables"

echo "21. TESTE FINAL:"
curl -I http://localhost/ || echo "Site não responde localmente"
curl -I https://$DOMAIN/ || echo "Site não responde via HTTPS"

echo ""
echo "=== DEPLOY CONCLUÍDO ==="
echo "Site: https://$DOMAIN"
echo "Admin: https://$DOMAIN/admin"
echo "Usuário: admin"
echo "Senha: admin123"
echo ""
echo "Logs úteis:"
echo "- Gunicorn: journalctl -u gunicorn -f"
echo "- Nginx: tail -f /var/log/nginx/error.log"
echo "- Django: tail -f $PROJECT_DIR/logs/django.log"
