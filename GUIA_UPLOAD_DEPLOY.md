# 📋 GUIA DE UPLOAD E DEPLOY - PRISMA AVALIAÇÕES

## 🎯 SITUAÇÃO ATUAL
- ✅ Projeto limpo e preparado para produção
- ✅ Arquivo ZIP criado: `prisma_projeto.zip` (12.96 MB)
- ✅ Scripts de deploy prontos
- 🔄 Próximo passo: Upload para VPS

## 🚀 OPÇÕES DE UPLOAD

### OPÇÃO 1: WinSCP (RECOMENDADO) 💯
1. **Baixar WinSCP**: https://winscp.net/eng/download.php
2. **Configurar conexão**:
   - Protocol: SFTP
   - Host: 72.60.144.18
   - Port: 22
   - Username: root
   - Password: sua_senha_vps
3. **Upload**:
   - Arrastar `prisma_projeto.zip` para `/tmp/`
   - Upload do script: Arrastar `deploy_via_zip.sh` para `/root/`

### OPÇÃO 2: PowerShell com curl
```powershell
# Se o VPS tiver servidor web temporário configurado
curl -T "prisma_projeto.zip" -u root:sua_senha ftp://72.60.144.18/tmp/
```

### OPÇÃO 3: Git Clone (Alternativa)
Se você tem um repositório Git, pode clonar diretamente no VPS.

### OPÇÃO 4: Upload via Painel de Controle
Se seu provedor VPS tem painel web com file manager.

## 🛠️ DEPLOY NO VPS

### 1. Conectar no VPS
```bash
ssh root@72.60.144.18
```

### 2. Preparar arquivos
```bash
# Se usou WinSCP, os arquivos já estão no lugar
# Tornar script executável
chmod +x /root/deploy_via_zip.sh

# Verificar se ZIP está em /tmp/
ls -la /tmp/prisma_projeto.zip
```

### 3. Executar Deploy
```bash
# Executar como root
./deploy_via_zip.sh
```

## 🎯 O QUE O SCRIPT FAZ AUTOMATICAMENTE

### ✅ Preparação do Sistema
- Atualiza Ubuntu 24.04
- Instala Python, Nginx, Certbot
- Instala dependências necessárias

### ✅ Configuração do Projeto
- Extrai ZIP para `/var/www/Prisma_Avaliacoes/`
- Cria ambiente virtual Python
- Instala dependências Django

### ✅ Configuração Django
- Executa migrações do banco
- Coleta arquivos estáticos
- Cria superusuário: `prismaav` / `PrismaAv4002@--`

### ✅ Configuração Gunicorn
- Configura serviço systemd
- 3 workers para performance
- Logs automáticos

### ✅ Configuração Nginx
- Proxy reverso para Gunicorn
- Configuração de arquivos estáticos
- Otimizações de cache

### ✅ Configuração SSL
- Certificado Let's Encrypt automático
- HTTPS forçado
- Renovação automática

### ✅ Testes Finais
- Verifica todos os serviços
- Testa conectividade
- Exibe resumo completo

## 🌐 RESULTADO FINAL

Após o deploy, você terá:

### Sites Funcionais:
- **HTTP**: http://www.prismaavaliacoes.com.br
- **HTTPS**: https://www.prismaavaliacoes.com.br (redirecionamento automático)

### Admin Django:
- **URL**: https://www.prismaavaliacoes.com.br/admin/
- **Usuário**: prismaav
- **Senha**: PrismaAv4002@--

### Dashboard:
- **URL**: https://www.prismaavaliacoes.com.br/

## 🔧 COMANDOS DE MANUTENÇÃO

### Verificar Status:
```bash
systemctl status gunicorn nginx
```

### Restart Serviços:
```bash
systemctl restart gunicorn nginx
```

### Ver Logs:
```bash
tail -f /var/log/gunicorn/error.log
tail -f /var/log/nginx/prismaavaliacoes_error.log
```

### Atualizar Projeto:
```bash
cd /var/www/Prisma_Avaliacoes/
source venv/bin/activate
git pull  # ou fazer novo upload
python manage.py migrate --settings=setup.settings.vps_production
python manage.py collectstatic --noinput --settings=setup.settings.vps_production
systemctl restart gunicorn
```

## ⚠️ VERIFICAÇÕES PRÉ-DEPLOY

### DNS Configurado:
- ✅ prismaavaliacoes.com.br → 72.60.144.18
- ✅ www.prismaavaliacoes.com.br → 72.60.144.18

### VPS Preparado:
- ✅ Ubuntu 24.04 LTS
- ✅ Acesso root via SSH
- ✅ Portas 80 e 443 abertas

### Arquivos Prontos:
- ✅ prisma_projeto.zip (12.96 MB)
- ✅ deploy_via_zip.sh
- ✅ Scripts de produção

## 🚨 SOLUÇÃO DE PROBLEMAS

### Se o deploy falhar:
```bash
# Ver logs do script
tail -f /var/log/syslog

# Verificar serviços
systemctl status gunicorn nginx

# Teste manual do Django
cd /var/www/Prisma_Avaliacoes/
source venv/bin/activate
python manage.py runserver 0.0.0.0:8001 --settings=setup.settings.vps_production
```

### Se SSL falhar:
```bash
# Configurar SSL manualmente
certbot --nginx -d prismaavaliacoes.com.br -d www.prismaavaliacoes.com.br
```

## 📞 SUPORTE

Se precisar de ajuda, me forneça:
1. Output do comando que falhou
2. Logs relevantes: `/var/log/gunicorn/error.log`
3. Status dos serviços: `systemctl status gunicorn nginx`

---

**🎉 Pronto! Escolha a opção de upload de sua preferência e execute o deploy!**
