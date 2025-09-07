# 🚨 PROBLEMA IDENTIFICADO: URLs com example.com no sitemap

## 📋 SITUAÇÃO ATUAL
```xml
<loc>https://example.com/blog/avaliacao-de-imoveis...</loc>
<loc>https://example.com/blog/</loc>
<loc>https://example.com/</loc>
```

## ⚡ SOLUÇÃO IMEDIATA - Execute no servidor:

### OPÇÃO 1: Correção específica para example.com
```bash
ssh root@srv989739.hstgr.cloud
cd /var/www/prisma_avaliacoes
git pull origin master
bash corrigir_example_com.sh
```

### OPÇÃO 2: Se git pull não funcionou, forçar atualização
```bash
ssh root@srv989739.hstgr.cloud
cd /var/www/prisma_avaliacoes
bash forcar_atualizacao_sitemap.sh
```

### OPÇÃO 3: Correção manual rápida
```bash
ssh root@srv989739.hstgr.cloud
cd /var/www/prisma_avaliacoes

# Corrigir Sites framework
python3 manage.py shell --settings=setup.settings_production -c "
from django.contrib.sites.models import Site
site = Site.objects.get_current()
site.domain = 'prismaavaliacoes.com.br'
site.name = 'Prisma Avaliações Imobiliárias'
site.save()
print('Site corrigido:', site.domain)
"

# Corrigir SEO Config
python3 manage.py shell --settings=setup.settings_production -c "
from seo.models import SEOConfig
config, created = SEOConfig.objects.get_or_create(defaults={
    'site_name': 'Prisma Avaliações Imobiliárias',
    'site_domain': 'prismaavaliacoes.com.br',
    'site_description': 'Avaliações imobiliárias profissionais'
})
config.site_domain = 'prismaavaliacoes.com.br'
config.save()
print('SEO Config corrigido:', config.site_domain)
"

# Reiniciar serviços
sudo systemctl restart gunicorn nginx
```

## 🎯 RESULTADO ESPERADO

Após executar qualquer script acima, o sitemap mostrará:
```xml
<loc>https://prismaavaliacoes.com.br/blog/avaliacao-de-imoveis...</loc>
<loc>https://prismaavaliacoes.com.br/blog/</loc>
<loc>https://prismaavaliacoes.com.br/</loc>
```

## ⏱️ TEMPO DE APLICAÇÃO
- Execução: 2-3 minutos
- Efeito no sitemap: Imediato
- Aguardar 5-10 minutos para propagação completa

## 🔍 VERIFICAÇÃO
```bash
# Testar sitemap
curl https://prismaavaliacoes.com.br/sitemap.xml | grep -o "https://[^<]*"

# Deve mostrar apenas URLs com prismaavaliacoes.com.br
```

## 📞 RESUBMETER NO GOOGLE
1. Acesse Google Search Console
2. Vá em Sitemaps
3. Remova sitemap antigo
4. Adicione: `https://prismaavaliacoes.com.br/sitemap.xml`
5. Aguarde processamento

**⚡ Execute AGORA um dos scripts para resolver o problema!**
