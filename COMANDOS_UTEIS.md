# 🛠️ Comandos Úteis - PythonAnywhere

Este arquivo contém comandos úteis para gerenciar sua aplicação Django no PythonAnywhere.

## 🔧 Comandos de Setup Inicial

```bash
# Clonar repositório
git clone https://github.com/martinssmrr/prisma_avaliacoes.git
cd prisma_avaliacoes

# Criar e ativar ambiente virtual
python3.10 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# Configuração automática
python setup_pythonanywhere.py
```

## 🗄️ Comandos de Banco de Dados

```bash
# Executar migrações
python manage.py migrate --settings=setup.production_settings

# Criar superusuário
python manage.py createsuperuser --settings=setup.production_settings

# Shell do Django
python manage.py shell --settings=setup.production_settings

# Fazer backup do banco
cp db.sqlite3 backup_$(date +%Y%m%d_%H%M%S).sqlite3

# Restaurar backup
cp backup_YYYYMMDD_HHMMSS.sqlite3 db.sqlite3
```

## 📂 Comandos de Arquivos Estáticos

```bash
# Coletar arquivos estáticos
python manage.py collectstatic --noinput --settings=setup.production_settings

# Limpar arquivos estáticos
rm -rf staticfiles/*

# Re-coletar arquivos estáticos
python manage.py collectstatic --noinput --clear --settings=setup.production_settings
```

## 🔄 Comandos de Atualização

```bash
# Atualizar código do Git
git pull origin master

# Instalar novas dependências
pip install -r requirements.txt

# Executar novas migrações
python manage.py migrate --settings=setup.production_settings

# Coletar novos arquivos estáticos
python manage.py collectstatic --noinput --settings=setup.production_settings

# Após atualizações, faça reload na Web App do PythonAnywhere
```

## 📊 Comandos de Monitoramento

```bash
# Verificar status dos processos
ps aux | grep python

# Verificar uso de espaço
du -h ~/prisma_avaliacoes/

# Verificar logs do Django (se configurado)
tail -f logs/django.log

# Verificar tamanho do banco de dados
ls -lh db.sqlite3

# Listar arquivos estáticos
ls -la staticfiles/
```

## 🐛 Comandos de Debug

```bash
# Verificar configurações
python manage.py check --settings=setup.production_settings

# Verificar URLs
python manage.py show_urls --settings=setup.production_settings

# Verificar migrações pendentes
python manage.py showmigrations --settings=setup.production_settings

# Testar email (se configurado)
python manage.py sendtestemail test@example.com --settings=setup.production_settings
```

## 📦 Gerenciamento de Dependências

```bash
# Listar pacotes instalados
pip list

# Verificar dependências desatualizadas
pip list --outdated

# Instalar pacote específico
pip install nome_do_pacote

# Atualizar requirements.txt
pip freeze > requirements.txt

# Verificar dependências de segurança
pip audit
```

## 🔐 Comandos de Segurança

```bash
# Verificar configurações de segurança
python manage.py check --deploy --settings=setup.production_settings

# Gerar nova SECRET_KEY (execute no shell do Django)
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())

# Limpar cache (se configurado)
python manage.py clear_cache --settings=setup.production_settings
```

## 📝 Comandos de Conteúdo

```bash
# Popular dados de exemplo
python popular_dados.py

# Exportar dados
python manage.py dumpdata artigos --settings=setup.production_settings > backup_artigos.json

# Importar dados
python manage.py loaddata backup_artigos.json --settings=setup.production_settings

# Listar artigos
python manage.py shell --settings=setup.production_settings
>>> from artigos.models import Artigo
>>> Artigo.objects.all()
```

## 🌐 Comandos de Deploy

```bash
# Script completo de deploy
./deploy_pythonanywhere.sh

# Deploy manual passo a passo
git pull origin master
pip install -r requirements.txt
python manage.py migrate --settings=setup.production_settings
python manage.py collectstatic --noinput --settings=setup.production_settings
# Fazer reload na Web App
```

## 🔍 Comandos de Análise

```bash
# Verificar estrutura do projeto
tree -I '__pycache__|*.pyc|venv|staticfiles'

# Contar linhas de código
find . -name "*.py" -not -path "./venv/*" | xargs wc -l

# Verificar TODO's no código
grep -r "TODO" --include="*.py" .

# Verificar imports não utilizados
python -m autoflake --check --imports=django,requests --recursive .
```

## 📋 Checklist de Deploy

- [ ] Código atualizado no Git
- [ ] requirements.txt atualizado
- [ ] Migrações criadas e testadas
- [ ] Arquivos estáticos coletados
- [ ] Configurações de produção testadas
- [ ] Backup do banco de dados realizado
- [ ] WSGI file configurado corretamente
- [ ] Variáveis de ambiente configuradas
- [ ] Domínio e SSL configurados (se aplicável)
- [ ] Logs monitorados

## 🆘 Em Caso de Emergência

```bash
# Reverter para versão anterior
git log --oneline  # Encontrar commit anterior
git reset --hard COMMIT_HASH

# Restaurar banco de backup
cp backup_YYYYMMDD_HHMMSS.sqlite3 db.sqlite3

# Reiniciar aplicação
# Fazer reload na Web App do PythonAnywhere

# Verificar logs de erro
# Acessar Error log na aba Web do PythonAnywhere
```

## 📞 Links Úteis

- **PythonAnywhere Help**: https://help.pythonanywhere.com/
- **Django Documentation**: https://docs.djangoproject.com/
- **Git Documentation**: https://git-scm.com/doc
- **Python Documentation**: https://docs.python.org/
