# DIAGNÓSTICO E CORREÇÃO - SEO 404 NO ADMIN

## 🔍 PROBLEMA IDENTIFICADO
- URL `/admin/seo/` retorna 404
- App SEO não está sendo reconhecido pelo Django admin
- Migrações aplicadas, mas admin não carrega

## 🧪 DIAGNÓSTICO COMPLETO

Execute estes comandos no servidor para identificar o problema:

### 1. Verificar se app SEO está instalado:
```bash
python manage.py shell --settings=setup.settings
```

No shell Django:
```python
from django.apps import apps
from django.conf import settings

print("=== DIAGNÓSTICO SEO ===")
print("INSTALLED_APPS:")
for app in settings.INSTALLED_APPS:
    print(f"  - {app}")

print("\nApps carregados:")
for app in apps.get_app_configs():
    print(f"  - {app.name} ({app.label})")

print(f"\nSEO instalado: {'seo' in settings.INSTALLED_APPS}")
print(f"SEO carregado: {'seo' in [app.name for app in apps.get_app_configs()]}")

# Verificar modelos SEO
try:
    from seo.models import SEOMeta, SEOConfig
    print("✅ Modelos SEO importados com sucesso")
    print(f"SEOMeta: {SEOMeta.objects.count()} registros")
    print(f"SEOConfig: {SEOConfig.objects.count()} registros")
except Exception as e:
    print(f"❌ Erro ao importar modelos SEO: {e}")

# Verificar admin SEO
try:
    from seo.admin import SEOMetaAdmin, SEOConfigAdmin
    print("✅ Admin SEO importado com sucesso")
except Exception as e:
    print(f"❌ Erro ao importar admin SEO: {e}")

exit()
```

### 2. Verificar estrutura de arquivos:
```bash
ls -la seo/
ls -la seo/migrations/
```

### 3. Verificar configuração do settings:
```bash
python manage.py diffsettings --settings=setup.settings | grep -i seo
python manage.py diffsettings --settings=setup.settings | grep INSTALLED_APPS
```

## 🔧 POSSÍVEIS CORREÇÕES

### CORREÇÃO 1: Verificar INSTALLED_APPS
Se o SEO não aparecer na lista, adicione ao settings:

```bash
# Editar arquivo settings
nano setup/settings.py
```

Procure por INSTALLED_APPS e verifique se tem:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'Prisma_avaliacoes',
    'seo',  # <- DEVE ESTAR AQUI
]
```

### CORREÇÃO 2: Recriar migrações SEO
Se houver problema com migrações:

```bash
# Remover migrações SEO antigas
rm -rf seo/migrations/
mkdir seo/migrations/
echo "# SEO migrations" > seo/migrations/__init__.py

# Recriar migrações
python manage.py makemigrations seo --settings=setup.settings
python manage.py migrate --settings=setup.settings
```

### CORREÇÃO 3: Verificar arquivo admin.py
```bash
cat seo/admin.py
```

Deve conter:
```python
from django.contrib import admin
from .models import SEOMeta, SEOConfig

@admin.register(SEOMeta)
class SEOMetaAdmin(admin.ModelAdmin):
    # ... configurações

@admin.register(SEOConfig)
class SEOConfigAdmin(admin.ModelAdmin):
    # ... configurações
```

### CORREÇÃO 4: Forçar reload do Django
```bash
# Coletar estáticos
python manage.py collectstatic --noinput --settings=setup.settings

# Reiniciar completamente
systemctl stop gunicorn
systemctl start gunicorn
systemctl reload nginx

# Verificar logs
tail -f /var/log/gunicorn/error.log
```

### CORREÇÃO 5: Verificar URLs
```bash
python manage.py shell --settings=setup.settings
```

```python
from django.contrib import admin
from django.urls import reverse

print("URLs admin disponíveis:")
for url_pattern in admin.site.urls[0]:
    print(f"  {url_pattern}")

# Verificar se SEO está registrado
print(f"Modelos registrados no admin: {list(admin.site._registry.keys())}")

exit()
```

## 🎯 TESTE PASSO A PASSO

Execute na ordem:

1. **Diagnóstico completo** (comando 1 acima)
2. **Verificar arquivos** (comando 2)
3. **Aplicar correção necessária** (baseado no diagnóstico)
4. **Reiniciar serviços** (correção 4)
5. **Testar admin**: https://prismaavaliacoes.com.br/admin/

## 📋 RESULTADOS ESPERADOS

Após correção, você deve ver:
- ✅ Seção "SEO" no menu admin
- ✅ URL `/admin/seo/seometa/` funcionando
- ✅ URL `/admin/seo/seoconfig/` funcionando

Execute o diagnóstico primeiro e me informe os resultados!
