# 🚀 GUIA DE DEPLOY - VPS HOSTINGER

## 📋 RESUMO
O projeto está **100% PRONTO** para deploy no VPS Hostinger!

## 📁 ARQUIVOS CRIADOS

### ✅ Configurações Django:
- `setup/settings/vps_hostinger.py` - Settings de produção VPS
- `.env.production` - Variáveis de ambiente

### ✅ Configurações Servidor:
- `config/gunicorn.service` - Serviço Gunicorn
- `config/nginx_prismaavaliacoes.conf` - Configuração Nginx
- `requirements_vps.txt` - Dependências Python

### ✅ Scripts Deploy:
- `deploy_vps_hostinger.sh` - Script automático completo

## 🚀 PASSOS PARA DEPLOY

### 1️⃣ CONECTAR NO VPS
```bash
ssh root@72.60.144.18
```

### 2️⃣ FAZER UPLOAD DO PROJETO

**Opção A - Via SCP:**
```bash
# No Windows
scp -r "C:\Users\teste\OneDrive\Desktop\Prisma Avaliações Imobiliarias" root@72.60.144.18:/tmp/prisma_projeto
```

**Opção B - Via Git:**
```bash
# No VPS
cd /var/www
git clone https://github.com/martinssmrr/prisma_avaliacoes.git prisma_avaliacoes
```

**Opção C - Via ZIP:**
```bash
# 1. Comprimir projeto no Windows
# 2. Upload via WinSCP para /tmp/prisma_projeto.zip
```

### 3️⃣ EXECUTAR DEPLOY AUTOMÁTICO
```bash
# No VPS
cd /var/www/prisma_avaliacoes
chmod +x deploy_vps_hostinger.sh
./deploy_vps_hostinger.sh
```

## ✅ RESULTADO FINAL

Após o deploy:

### 🌐 Sites:
- **HTTP**: http://www.prismaavaliacoes.com.br
- **HTTPS**: https://www.prismaavaliacoes.com.br

### 🔐 Admin:
- **URL**: https://www.prismaavaliacoes.com.br/admin/
- **Usuário**: prismaav
- **Senha**: PrismaAv4002@--

### 📊 Dashboard:
- **URL**: https://www.prismaavaliacoes.com.br/

## 🔧 COMANDOS DE MANUTENÇÃO

### Reiniciar Serviços:
```bash
systemctl restart gunicorn nginx
```

### Ver Logs:
```bash
tail -f /var/log/gunicorn/error.log
tail -f /var/log/nginx/prismaavaliacoes_error.log
```

### Status dos Serviços:
```bash
systemctl status gunicorn nginx
```

### Atualizar Projeto:
```bash
cd /var/www/prisma_avaliacoes
source venv/bin/activate
git pull  # ou reupload
python manage.py migrate --settings=setup.settings.vps_hostinger
python manage.py collectstatic --noinput --settings=setup.settings.vps_hostinger
systemctl restart gunicorn
```

## 🎯 CARACTERÍSTICAS DO DEPLOY

### ✅ Performance:
- **Gunicorn** com 3 workers
- **Nginx** como proxy reverso
- **Gzip** compression
- **Cache** headers otimizados

### ✅ Segurança:
- **HTTPS** forçado (SSL/TLS)
- **Security headers** configurados
- **Rate limiting** no admin
- **Firewall** UFW configurado

### ✅ Monitoramento:
- **Logs** detalhados
- **Systemd** service management
- **Auto-restart** em caso de falha

### ✅ Backup:
- **SQLite** database (fácil backup)
- **Media files** organizados
- **Static files** servidos pelo Nginx

## 🆘 SOLUÇÃO DE PROBLEMAS

### Se Gunicorn não iniciar:
```bash
systemctl status gunicorn
journalctl -u gunicorn -f
```

### Se Nginx der erro:
```bash
nginx -t
systemctl status nginx
```

### Se SSL falhar:
```bash
certbot --nginx -d prismaavaliacoes.com.br -d www.prismaavaliacoes.com.br
```

## 📞 SUPORTE

Para problemas, verifique:
1. **Logs**: `/var/log/gunicorn/` e `/var/log/nginx/`
2. **Status**: `systemctl status gunicorn nginx`
3. **Conectividade**: `curl -I http://localhost`

---

**🎉 PROJETO 100% PRONTO PARA PRODUÇÃO!**
