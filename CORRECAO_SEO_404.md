# COMANDOS RÁPIDOS PARA CORRIGIR SEO 404

## 🚨 PROBLEMA IDENTIFICADO
URL retorna 404: https://prismaavaliacoes.com.br/admin/seo/
Erro: `django.contrib.admin.sites.catch_all_view`

## ⚡ CORREÇÃO RÁPIDA (PowerShell Windows)

Execute este comando no PowerShell:

```powershell
ssh root@srv989739.hstgr.cloud "cd /var/www/html/prismaavaliacoes.com.br && source venv/bin/activate && python manage.py makemigrations seo --settings=setup.settings && python manage.py migrate --settings=setup.settings && systemctl restart gunicorn"
```

Se não funcionar, problema pode ser no INSTALLED_APPS:

```powershell
ssh root@srv989739.hstgr.cloud "cd /var/www/html/prismaavaliacoes.com.br && source venv/bin/activate && grep -n 'seo' setup/settings.py || echo 'SEO não encontrado em settings'"
```

## 🔧 CORREÇÃO COMPLETA

### Opção 1: Script via PowerShell
```powershell
# Baixar e executar script de correção via PowerShell
ssh root@srv989739.hstgr.cloud "wget https://raw.githubusercontent.com/martinssmrr/prisma_avaliacoes/master/migrar_seo_apenas.sh -O migrar_seo.sh && chmod +x migrar_seo.sh && ./migrar_seo.sh"
```

### Opção 2: Comandos passo a passo (Só migração)
```bash
ssh root@srv989739.hstgr.cloud
cd /var/www/html/prismaavaliacoes.com.br
source venv/bin/activate

# 1. Criar migrações SEO
python manage.py makemigrations seo --settings=setup.settings

# 2. Aplicar migrações
python manage.py migrate --settings=setup.settings

# 3. Reiniciar serviços
systemctl restart gunicorn
systemctl reload nginx

# 4. Verificar se funcionou
curl -s -o /dev/null -w "%{http_code}" https://prismaavaliacoes.com.br/admin/seo/
```

## 🧪 VERIFICAÇÃO RÁPIDA

```bash
ssh root@srv989739.hstgr.cloud
wget https://raw.githubusercontent.com/martinssmrr/prisma_avaliacoes/master/verificar_seo_rapido.sh
chmod +x verificar_seo_rapido.sh
./verificar_seo_rapido.sh
```

## 🎯 POSSÍVEIS CAUSAS DO ERRO 404

1. **App 'seo' não está em INSTALLED_APPS** (mais provável)
2. **Migrações não aplicadas**
3. **Modelos não registrados no admin**
4. **Cache do Gunicorn/Django**
5. **Problema de import dos models**

## ✅ VERIFICAÇÃO PÓS-CORREÇÃO

Após execução, estas URLs devem funcionar:
- ✅ https://prismaavaliacoes.com.br/admin/
- ✅ https://prismaavaliacoes.com.br/admin/seo/
- ✅ https://prismaavaliacoes.com.br/admin/seo/seometa/
- ✅ https://prismaavaliacoes.com.br/admin/seo/seoconfig/

## 📞 SE PROBLEMA PERSISTIR

1. **Verificar logs:**
```bash
tail -f /var/log/gunicorn/error.log
```

2. **Verificar estrutura do app:**
```bash
ls -la seo/
cat seo/admin.py
```

3. **Verificar settings.py:**
```bash
grep -A 20 "INSTALLED_APPS" setup/settings.py
```

## 🚀 DEPLOY FRESH (Última opção)

Se nada funcionar, fazer deploy fresh:
```bash
ssh root@srv989739.hstgr.cloud
wget https://raw.githubusercontent.com/martinssmrr/prisma_avaliacoes/master/deploy_hostinger_completo.sh
chmod +x deploy_hostinger_completo.sh
./deploy_hostinger_completo.sh
```

---

**💡 TIP:** Execute sempre a verificação rápida primeiro para identificar a causa exata!
