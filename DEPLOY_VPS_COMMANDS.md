# 🚀 COMANDOS DE DEPLOY VPS - PRISMA AVALIAÇÕES
## Executar no VPS Ubuntu 24.04 como root

---

## ⚡ **DEPLOY RÁPIDO (Executar apenas isto):**

```bash
# 1. Copiar arquivos do projeto para o VPS
scp -r /caminho/local/Prisma_Avaliacoes/ root@SEU_IP:/var/www/

# 2. Conectar no VPS
ssh root@SEU_IP

# 3. Executar script de deploy
cd /var/www/Prisma_Avaliacoes
chmod +x deploy_vps_complete.sh
./deploy_vps_complete.sh
```

---

## 📋 **COMANDOS PASSO A PASSO (se preferir manual):**

### **1. Preparar Sistema**
```bash
apt update && apt upgrade -y
apt install python3-pip python3-venv python3-dev build-essential \
    libssl-dev libpq-dev nginx certbot python3-certbot-nginx git -y
```

### **2. Criar Estrutura**
```bash
mkdir -p /var/www/Prisma_Avaliacoes
mkdir -p /var/log/gunicorn
cd /var/www/Prisma_Avaliacoes
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

### **3. Instalar Dependências**
```bash
pip install django==5.2.5 gunicorn==21.2.0 django-jazzmin==3.0.1
pip install Pillow python-decouple pytz cryptography requests
```

### **4. Configurar Django**
```bash
export DJANGO_SETTINGS_MODULE=setup.settings.vps_production
python manage.py migrate --settings=setup.settings.vps_production
python manage.py collectstatic --noinput --settings=setup.settings.vps_production
```

### **5. Criar Superusuário**
```bash
python manage.py shell --settings=setup.settings.vps_production
# No shell Python:
from django.contrib.auth.models import User
User.objects.create_superuser('prismaav', 'contato@prismaavaliacoes.com.br', 'PrismaAv4002@--')
exit()
```

### **6. Configurar Gunicorn**
```bash
# Copiar arquivo gunicorn.service para /etc/systemd/system/
cp config/gunicorn.service /etc/systemd/system/

systemctl daemon-reload
systemctl start gunicorn
systemctl enable gunicorn
systemctl status gunicorn
```

### **7. Configurar Nginx**
```bash
# Copiar configuração do nginx
cp config/nginx_prismaavaliacoes.conf /etc/nginx/sites-available/prismaavaliacoes

ln -s /etc/nginx/sites-available/prismaavaliacoes /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

nginx -t
systemctl restart nginx
systemctl enable nginx
```

### **8. Configurar SSL**
```bash
certbot --nginx -d prismaavaliacoes.com.br -d www.prismaavaliacoes.com.br
systemctl reload nginx
```

### **9. Configurar Permissões**
```bash
chown -R root:www-data /var/www/Prisma_Avaliacoes/
chmod -R 755 /var/www/Prisma_Avaliacoes/
chmod 664 /var/www/Prisma_Avaliacoes/db.sqlite3
```

---

## 🔧 **COMANDOS DE MANUTENÇÃO:**

### **Reiniciar Serviços**
```bash
systemctl restart gunicorn
systemctl restart nginx
```

### **Ver Logs**
```bash
# Logs do Gunicorn
tail -f /var/log/gunicorn/error.log
tail -f /var/log/gunicorn/access.log

# Logs do Nginx
tail -f /var/log/nginx/prismaavaliacoes_error.log
tail -f /var/log/nginx/prismaavaliacoes_access.log

# Status dos serviços
systemctl status gunicorn
systemctl status nginx
```

### **Atualizar Projeto**
```bash
cd /var/www/Prisma_Avaliacoes
source venv/bin/activate
git pull origin main
pip install -r requirements_vps.txt
python manage.py migrate --settings=setup.settings.vps_production
python manage.py collectstatic --noinput --settings=setup.settings.vps_production
systemctl restart gunicorn
systemctl reload nginx
```

---

## 🎯 **VERIFICAÇÕES FINAIS:**

### **Testar Site**
```bash
curl -I http://localhost/
curl -I https://www.prismaavaliacoes.com.br/
```

### **Verificar Certificado SSL**
```bash
certbot certificates
```

### **Monitorar Recursos**
```bash
htop
df -h
free -h
```

---

## 📊 **ACESSO APÓS DEPLOY:**

- **Site**: https://www.prismaavaliacoes.com.br
- **Admin**: https://www.prismaavaliacoes.com.br/admin/
- **Usuário**: prismaav
- **Senha**: PrismaAv4002@--

---

## 🚨 **SOLUÇÃO DE PROBLEMAS:**

### **Se Gunicorn não iniciar:**
```bash
# Verificar logs
journalctl -u gunicorn -n 50

# Testar manualmente
cd /var/www/Prisma_Avaliacoes
source venv/bin/activate
gunicorn --bind 0.0.0.0:8000 setup.wsgi:application
```

### **Se Nginx der erro:**
```bash
# Testar configuração
nginx -t

# Verificar logs
tail -f /var/log/nginx/error.log
```

### **Se SSL não funcionar:**
```bash
# Renovar certificado
certbot renew --dry-run
certbot renew --force-renewal
```
