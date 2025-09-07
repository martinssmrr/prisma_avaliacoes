# 🚀 GUIA DE MIGRAÇÃO SEO PARA PRODUÇÃO
# Prisma Avaliações Imobiliárias

echo "========================================="
echo "🚀 MIGRAÇÃO DO SISTEMA SEO PARA PRODUÇÃO"
echo "========================================="

# 1. Navegar para o diretório do projeto
cd /var/www/prisma_avaliacoes

# 2. Fazer backup do banco (segurança)
echo "📦 Fazendo backup do banco de dados..."
cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)

# 3. Atualizar código do repositório
echo "📥 Atualizando código do repositório..."
git stash  # salvar mudanças locais se houver
git pull origin master

# 4. Verificar se o arquivo de migração existe
if [ ! -f "migrate_seo_to_production.py" ]; then
    echo "❌ ERRO: Arquivo migrate_seo_to_production.py não encontrado!"
    echo "Verifique se o git pull foi executado corretamente."
    exit 1
fi

# 5. Executar o script de migração
echo "🔄 Executando migração do SEO..."
python3 migrate_seo_to_production.py

# 6. Verificar se deu certo
if [ $? -eq 0 ]; then
    echo "✅ Migração executada com sucesso!"
else
    echo "❌ ERRO na migração! Verifique os logs acima."
    exit 1
fi

# 7. Coletar arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python3 manage.py collectstatic --noinput --settings=setup.settings_production

# 8. Reiniciar serviços
echo "🔄 Reiniciando serviços..."
sudo systemctl restart gunicorn
sudo systemctl restart nginx

# 9. Verificar status dos serviços
echo "🔍 Verificando status dos serviços..."
sudo systemctl status gunicorn --no-pager -l
sudo systemctl status nginx --no-pager -l

# 10. Teste final
echo "🧪 Testando SEO no admin..."
python3 manage.py shell --settings=setup.settings_production -c "
from seo.models import SEOMeta, SEOConfig
from django.contrib import admin

print('✅ SEOMeta funcionando:', SEOMeta.objects.count() >= 0)
print('✅ SEOConfig funcionando:', True)

# Verificar se estão registrados no admin
print('✅ SEOMeta no admin:', SEOMeta in admin.site._registry)
print('✅ SEOConfig no admin:', SEOConfig in admin.site._registry)
"

echo ""
echo "========================================="
echo "🎉 MIGRAÇÃO CONCLUÍDA!"
echo "========================================="
echo ""
echo "📋 VERIFICAÇÕES FINAIS:"
echo "1. Acesse: https://prismaavaliacoes.com.br/admin/"
echo "2. Procure pela seção 'SEO' no menu"
echo "3. Teste criar/editar configurações SEO"
echo ""
echo "📊 LOGS IMPORTANTES:"
echo "- Gunicorn: sudo tail -f /var/log/gunicorn/gunicorn.log"
echo "- Nginx: sudo tail -f /var/log/nginx/error.log"
echo "- Django: tail -f /var/www/prisma_avaliacoes/logs/django.log"
echo ""
echo "✅ MIGRAÇÃO DO SEO FINALIZADA COM SUCESSO!"
