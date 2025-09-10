# 🚀 GUIA DE DEPLOY - HOSTINGER VPS

## 📋 PRÉ-REQUISITOS

1. **VPS Hostinger** configurada com Ubuntu 22.04
2. **Acesso SSH** ao servidor
3. **Domínio** configurado apontando para o IP da VPS
4. **Repositório GitHub** atualizado

## 🔧 PASSOS DO DEPLOY

### 1. CONECTAR NA VPS VIA SSH
```bash
ssh root@SEU_IP_DA_VPS
```

### 2. EXECUTAR SCRIPT DE DEPLOY
```bash
# Fazer upload do script de deploy
wget https://raw.githubusercontent.com/martinssmrr/prisma_avaliacoes/master/deploy_hostinger.sh

# Dar permissão de execução
chmod +x deploy_hostinger.sh

# Executar o deploy
./deploy_hostinger.sh
```

### 3. CONFIGURAÇÕES ESPECÍFICAS

#### A. Configurar DNS no Hostinger
- **Tipo A**: prismaavaliacoes.com.br → IP_DA_VPS
- **Tipo A**: www.prismaavaliacoes.com.br → IP_DA_VPS

#### B. Verificar Firewall
```bash
ufw status
ufw allow 22    # SSH
ufw allow 80    # HTTP
ufw allow 443   # HTTPS
```

#### C. Configurar SSL (Automático no script)
```bash
# O script já executa, mas se precisar refazer:
certbot --nginx -d prismaavaliacoes.com.br -d www.prismaavaliacoes.com.br
```

## 🔍 VERIFICAÇÕES PÓS-DEPLOY

### 1. Status dos Serviços
```bash
systemctl status nginx
systemctl status gunicorn
systemctl status postgresql
```

### 2. Logs para Debugging
```bash
# Logs do Gunicorn
journalctl -u gunicorn -f

# Logs do Nginx
tail -f /var/log/nginx/error.log

# Logs do Django
tail -f /var/www/prisma_avaliacoes/logs/django.log
```

### 3. Testes de Conectividade
```bash
# Teste local
curl -I http://localhost/

# Teste do domínio
curl -I https://prismaavaliacoes.com.br/
```

## 🎯 ACESSO AO SISTEMA

- **Site:** https://prismaavaliacoes.com.br
- **Admin:** https://prismaavaliacoes.com.br/admin
- **Usuário:** admin
- **Senha:** admin123 *(ALTERAR IMEDIATAMENTE)*

## 🔧 COMANDOS ÚTEIS

### Reiniciar Serviços
```bash
systemctl restart gunicorn
systemctl restart nginx
```

### Atualizar Código
```bash
cd /var/www/prisma_avaliacoes
git pull origin master
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
systemctl restart gunicorn
```

### Backup do Banco
```bash
sudo -u postgres pg_dump prisma_db > backup_$(date +%Y%m%d).sql
```

## 🚨 TROUBLESHOOTING

### Erro 502 Bad Gateway
```bash
# Verificar gunicorn
systemctl status gunicorn
journalctl -u gunicorn -n 50

# Reiniciar serviços
systemctl restart gunicorn nginx
```

### Erro de Permissão
```bash
chown -R www-data:www-data /var/www/prisma_avaliacoes
chmod -R 755 /var/www/prisma_avaliacoes
```

### SSL não funciona
```bash
# Renovar certificado
certbot renew
systemctl reload nginx
```

## 📱 CONTATOS DE SUPORTE

- **Hostinger:** Painel de controle da VPS
- **Certbot:** Para renovação SSL automática
- **GitHub:** Para atualizações do código
