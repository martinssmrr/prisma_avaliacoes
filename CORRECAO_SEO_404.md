# COMANDOS RÁPIDOS PARA CORRIGIR SEO 404

## 🚨 PROBLEMA IDENTIFICADO
URL retorna 404: https://prismaavaliacoes.com.br/admin/seo/
Erro: `django.contrib.admin.sites.catch_all_view`

## ⚡ CORREÇÃO RÁPIDA (Uma linha)

```bash
ssh root@srv989739.hstgr.cloud "cd /var/www/html/prismaavaliacoes.com.br && source venv/bin/activate && python manage.py shell --settings=setup.settings -c \"from django.conf import settings; print('SEO em INSTALLED_APPS:', 'seo' in settings.INSTALLED_APPS)\" && systemctl restart gunicorn"
```

## 🔧 CORREÇÃO COMPLETA

### Opção 1: Script automático
```bash
ssh root@srv989739.hstgr.cloud
wget https://raw.githubusercontent.com/martinssmrr/prisma_avaliacoes/master/corrigir_seo_404.sh
chmod +x corrigir_seo_404.sh
./corrigir_seo_404.sh
```

### Opção 2: Comandos manuais
```bash
ssh root@srv989739.hstgr.cloud
cd /var/www/html/prismaavaliacoes.com.br
source venv/bin/activate

# 1. Verificar se SEO está em INSTALLED_APPS
python manage.py shell --settings=setup.settings -c "
from django.conf import settings
print('INSTALLED_APPS:')
for app in settings.INSTALLED_APPS:
    print('  -', app)
print('SEO presente:', 'seo' in settings.INSTALLED_APPS)
"

# 2. Se não estiver, adicionar
grep -q "seo" setup/settings.py || echo "PROBLEMA: SEO não está em INSTALLED_APPS"

# 3. Aplicar migrações
python manage.py migrate --settings=setup.settings

# 4. Reiniciar serviços
systemctl restart gunicorn
systemctl reload nginx
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
