# INSTRUÇÕES PARA CORRIGIR PRODUÇÃO - Django Settings Conflict

## PROBLEMA IDENTIFICADO
O mesmo conflito que tínhamos localmente está acontecendo no servidor:
- Existe `setup/settings.py` (arquivo)
- Existe `setup/settings/` (diretório)
- Django está importando o diretório vazio em vez do arquivo
- Resultado: "ImproperlyConfigured: settings.DATABASES is improperly configured"

## SOLUÇÃO - EXECUTAR NO SERVIDOR VIA SSH

### 1. Conectar ao servidor
```bash
ssh root@srv989739.hstgr.cloud
```

### 2. Navegar para o projeto
```bash
cd /var/www/html/prismaavaliacoes.com.br
```

### 3. Verificar o problema
```bash
# Listar arquivos para confirmar conflito
ls -la setup/
# Deve mostrar:
# - settings.py (arquivo)
# - settings/ (diretório)
```

### 4. Fazer backup
```bash
# Backup do projeto atual
cp -r . ../backup_$(date +%Y%m%d_%H%M%S)
```

### 5. Atualizar código do Git
```bash
# Buscar atualizações
git fetch origin master
git reset --hard origin/master
```

### 6. CORREÇÃO PRINCIPAL - Renomear diretório conflitante
```bash
# Esta é a correção principal!
mv setup/settings setup/settings_backup_$(date +%Y%m%d_%H%M%S)
```

### 7. Verificar se a correção funcionou
```bash
# Ativar ambiente virtual
source venv/bin/activate

# Testar configuração Django
python manage.py check --settings=setup.settings
```

### 8. Aplicar migrações (agora deve funcionar!)
```bash
python manage.py migrate --settings=setup.settings
```

### 9. Configurar SEO
```bash
python manage.py shell --settings=setup.settings
```

No shell Django, execute:
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
        'default_description': 'Prisma Avaliações Imobiliárias - Serviços profissionais de avaliação',
        'default_keywords': 'avaliação imobiliária, laudo de avaliação, prisma',
        'contact_email': 'contato@prismaavaliacoes.com.br',
        'domain': 'prismaavaliacoes.com.br'
    }
)

print(f"Site: {site.domain}")
print(f"SEO Config: {config.site_name}")

# Sair do shell
exit()
```

### 10. Coletar arquivos estáticos
```bash
python manage.py collectstatic --noinput --settings=setup.settings
```

### 11. Reiniciar serviços
```bash
systemctl reload nginx
systemctl restart gunicorn
```

### 12. Verificar status
```bash
systemctl status nginx
systemctl status gunicorn
```

## VERIFICAÇÃO FINAL

### Testar URLs:
- Site: https://prismaavaliacoes.com.br/
- Admin: https://prismaavaliacoes.com.br/admin/
- SEO Admin: https://prismaavaliacoes.com.br/admin/seo/
- Sitemap: https://prismaavaliacoes.com.br/sitemap.xml

### O que deve aparecer no admin:
- Seção "SEO" com "SEO Metas" e "SEO Configs"
- Possibilidade de criar/editar configurações SEO
- Sitemap gerando URLs com prismaavaliacoes.com.br

## SCRIPT AUTOMÁTICO (ALTERNATIVA)

Se preferir, use o script automático que criamos:
```bash
# Baixar e executar script
wget https://raw.githubusercontent.com/martinssmrr/prisma_avaliacoes/master/sincronizar_producao.sh
chmod +x sincronizar_producao.sh
./sincronizar_producao.sh
```

## RESUMO DA CORREÇÃO
✅ Resolver conflito: setup/settings.py vs setup/settings/
✅ Aplicar migrações Django
✅ Configurar domínio correto no SEO
✅ Reiniciar serviços
✅ Verificar admin funcionando

Após essas etapas, o SEO deve aparecer no Django admin!
