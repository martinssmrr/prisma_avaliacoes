# PRÓXIMOS PASSOS - SEO FUNCIONANDO NO SERVIDOR

## ✅ CORREÇÃO APLICADA COM SUCESSO!

As migrações funcionaram, o que significa:
- ✅ Conflito setup/settings resolvido
- ✅ Django consegue importar configurações
- ✅ Banco de dados conectado corretamente
- ✅ App SEO reconhecido pelo Django

## 🔍 VERIFICAÇÕES NECESSÁRIAS

Execute os comandos abaixo no servidor para configurar completamente o SEO:

### 1. Verificar se tabelas SEO existem:
```bash
python manage.py shell --settings=setup.settings
```

No shell Django:
```python
# Verificar se modelos SEO estão funcionando
from seo.models import SEOMeta, SEOConfig
print("SEOMeta count:", SEOMeta.objects.count())
print("SEOConfig count:", SEOConfig.objects.count())

# Verificar Sites framework
from django.contrib.sites.models import Site
site = Site.objects.get(pk=1)
print(f"Site atual: {site.domain} - {site.name}")
```

### 2. Se as tabelas existem mas estão vazias, configurar:
```python
# Configurar site correto
from django.contrib.sites.models import Site
site = Site.objects.get(pk=1)
site.domain = 'prismaavaliacoes.com.br'
site.name = 'Prisma Avaliações'
site.save()
print(f"✅ Site configurado: {site.domain}")

# Criar configuração SEO padrão
from seo.models import SEOConfig
config, created = SEOConfig.objects.get_or_create(
    pk=1,
    defaults={
        'site_name': 'Prisma Avaliações',
        'default_description': 'Prisma Avaliações Imobiliárias - Serviços profissionais de avaliação de imóveis',
        'default_keywords': 'avaliação imobiliária, laudo de avaliação, prisma avaliações',
        'contact_email': 'contato@prismaavaliacoes.com.br',
        'domain': 'prismaavaliacoes.com.br',
        'default_image': '/static/img/logo-prisma.jpg'
    }
)

if created:
    print(f"✅ SEOConfig criado: {config.site_name}")
else:
    print(f"✅ SEOConfig já existe: {config.site_name}")

# Sair do shell
exit()
```

### 3. Coletar arquivos estáticos (importante!):
```bash
python manage.py collectstatic --noinput --settings=setup.settings
```

### 4. Reiniciar serviços:
```bash
systemctl restart gunicorn
systemctl reload nginx
```

### 5. Verificar logs se necessário:
```bash
# Log do Gunicorn
tail -f /var/log/gunicorn/error.log

# Log do Nginx
tail -f /var/log/nginx/error.log
```

## 🌐 VERIFICAÇÃO FINAL

Depois dos passos acima, teste estas URLs:

1. **Admin principal**: https://prismaavaliacoes.com.br/admin/
2. **SEO Admin**: https://prismaavaliacoes.com.br/admin/seo/
3. **SEO Metas**: https://prismaavaliacoes.com.br/admin/seo/seometa/
4. **SEO Configs**: https://prismaavaliacoes.com.br/admin/seo/seoconfig/
5. **Sitemap**: https://prismaavaliacoes.com.br/sitemap.xml

## 🎯 O QUE VOCÊ DEVE VER NO ADMIN:

- Seção "SEO" no menu principal
- Subseções "SEO Metas" e "SEO Configs"
- Possibilidade de criar/editar configurações SEO
- Sitemap XML funcionando com URLs corretas

## ❓ SE ALGO NÃO FUNCIONAR:

Execute o diagnóstico:
```bash
python manage.py shell --settings=setup.settings -c "
from django.apps import apps
print('Apps instalados:', [app.name for app in apps.get_app_configs()])
print('SEO app carregado:', 'seo' in [app.name for app in apps.get_app_configs()])
"
```
