# GUIA COMPLETO DE DEPLOY - PRISMA AVALIAÇÕES HOSTINGER

## 📋 RESUMO DAS ATUALIZAÇÕES PREPARADAS

Este deploy inclui TODAS as melhorias implementadas localmente:

✅ **Correção do conflito setup/settings** (problema principal em produção)  
✅ **App SEO completo** com models, admin e sitemaps  
✅ **Tags canonical** implementadas em todos os templates  
✅ **Cores atualizadas** para azul padrão #1e40af em toda navegação  
✅ **Sites Framework** configurado com domínio correto  
✅ **Arquivos estáticos** com CSS customizado  

## 🚀 EXECUÇÃO DO DEPLOY

### Opção 1: Script Automático (Recomendado)

1. **Conectar ao servidor via SSH:**
```bash
ssh root@srv989739.hstgr.cloud
```

2. **Baixar e executar o script de deploy:**
```bash
# Baixar script
wget https://raw.githubusercontent.com/martinssmrr/prisma_avaliacoes/master/deploy_hostinger_completo.sh

# Dar permissão de execução
chmod +x deploy_hostinger_completo.sh

# Executar deploy completo
./deploy_hostinger_completo.sh
```

3. **Executar verificação pós-deploy:**
```bash
# Baixar script de verificação
wget https://raw.githubusercontent.com/martinssmrr/prisma_avaliacoes/master/verificar_deploy.sh
chmod +x verificar_deploy.sh

# Executar verificação
./verificar_deploy.sh
```

### Opção 2: Execução Manual

Se preferir executar passo a passo:

```bash
# 1. Conectar ao servidor
ssh root@srv989739.hstgr.cloud

# 2. Navegar para o projeto
cd /var/www/html/prismaavaliacoes.com.br

# 3. Fazer backup
cp -r . ../backup_$(date +%Y%m%d_%H%M%S)

# 4. Atualizar código
git fetch origin master
git reset --hard origin/master

# 5. CORREÇÃO CRÍTICA: Resolver conflito settings
mv setup/settings setup/settings_backup_$(date +%Y%m%d_%H%M%S)

# 6. Ativar ambiente virtual
source venv/bin/activate

# 7. Instalar dependências
pip install -r requirements.txt

# 8. Testar configuração
python manage.py check --settings=setup.settings

# 9. Aplicar migrações
python manage.py migrate --settings=setup.settings

# 10. Configurar SEO (ver seção abaixo)

# 11. Coletar estáticos
python manage.py collectstatic --noinput --settings=setup.settings

# 12. Reiniciar serviços
systemctl restart gunicorn
systemctl reload nginx
```

## 🎯 CONFIGURAÇÃO SEO (Passo 10 detalhado)

```bash
python manage.py shell --settings=setup.settings
```

No shell Django:
```python
from django.contrib.sites.models import Site
from seo.models import SEOConfig

# Configurar Site correto
site = Site.objects.get(pk=1)
site.domain = 'prismaavaliacoes.com.br'
site.name = 'Prisma Avaliações'
site.save()

# Configurar SEO
config, created = SEOConfig.objects.get_or_create(
    pk=1,
    defaults={
        'site_name': 'Prisma Avaliações',
        'default_description': 'Prisma Avaliações Imobiliárias - Especialistas em avaliações de imóveis no Brasil. Laudos técnicos, agilidade e confiabilidade comprovada.',
        'default_keywords': 'avaliação imobiliária, laudo técnico de avaliação, avaliação de imóveis, laudo de avaliação de imóveis, avaliação de um imóvel, modelo de avaliação de imóveis',
        'contact_email': 'contato@prismaavaliacoes.com.br',
        'domain': 'prismaavaliacoes.com.br'
    }
)

print(f"Site: {site.domain}")
print(f"SEO Config: {config.site_name}")

# Sair do shell
exit()
```

## ✅ VERIFICAÇÃO PÓS-DEPLOY

Após a execução, verificar estas URLs:

1. **Site principal:** https://prismaavaliacoes.com.br/
2. **Admin Django:** https://prismaavaliacoes.com.br/admin/
3. **SEO Admin:** https://prismaavaliacoes.com.br/admin/seo/
4. **SEO Configs:** https://prismaavaliacoes.com.br/admin/seo/seoconfig/
5. **Sitemap XML:** https://prismaavaliacoes.com.br/sitemap.xml

### O que você deve ver após o deploy:

✅ **Site carregando normalmente**  
✅ **Admin acessível** com login funcionando  
✅ **Seção "SEO"** visível no menu admin  
✅ **Navegação com cores azuis** (#1e40af)  
✅ **Sitemap** gerando URLs com prismaavaliacoes.com.br  
✅ **Tags canonical** no código fonte das páginas  

## 🔧 RESOLUÇÃO DE PROBLEMAS

### Se o admin SEO não aparecer:
```bash
# Verificar se app está instalado
python manage.py shell --settings=setup.settings -c "
from django.apps import apps
print([app.name for app in apps.get_app_configs()])
"

# Se não aparecer 'seo', verificar INSTALLED_APPS no settings.py
```

### Se as cores não atualizaram:
```bash
# Forçar coleta de estáticos
python manage.py collectstatic --clear --noinput --settings=setup.settings

# Reiniciar serviços
systemctl restart gunicorn nginx
```

### Se sitemap ainda mostra example.com:
```bash
# Verificar configuração do Sites
python manage.py shell --settings=setup.settings -c "
from django.contrib.sites.models import Site
site = Site.objects.get(pk=1)
print(f'Domain: {site.domain}')
"
```

## 📝 LOGS PARA DEBUGGING

Se algo não funcionar, verificar logs:

```bash
# Log do Gunicorn
tail -f /var/log/gunicorn/error.log

# Log do Nginx
tail -f /var/log/nginx/error.log

# Status dos serviços
systemctl status gunicorn
systemctl status nginx
```

## 🎉 RESULTADO ESPERADO

Após o deploy bem-sucedido:

- ✅ **Site funcionando** com todas as páginas carregando
- ✅ **Admin SEO funcionando** com interface limpa
- ✅ **Navegação com cores consistentes** em azul padrão
- ✅ **SEO otimizado** com canonical tags e sitemap correto
- ✅ **Sistema estável** e responsivo

## 📞 SUPORTE

Se encontrar problemas durante o deploy:

1. **Verificar logs** dos serviços (comandos acima)
2. **Executar script de verificação** para diagnóstico
3. **Comparar com ambiente local** funcionando
4. **Usar backup** para reverter se necessário

---

**💡 DICA:** Execute sempre o script de verificação após o deploy para confirmar que tudo está funcionando corretamente!
