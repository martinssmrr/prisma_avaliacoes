# 🚨 CHECKLIST EMERGENCIAL - PythonAnywhere

## ❌ AINDA NÃO FUNCIONA? Execute EXATAMENTE isto:

### 🔥 PASSO 1: Atualizar e diagnosticar
```bash
cd /home/prismaav
git pull origin master
python3.10 diagnostico_emergencial.py
```

### 🔥 PASSO 2: Correção de emergência (cole tudo de uma vez)
```bash
# Recriar .env sem problemas de encoding
cat > .env << 'EOF'
SECRET_KEY=django-insecure-emergency-key-2025
DEBUG=False
ALLOWED_HOSTS=prismaav.pythonanywhere.com,localhost,127.0.0.1,testserver
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
STATIC_URL=/static/
STATIC_ROOT=staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=media
EOF

# Garantir dependências
pip3.10 install --user django python-decouple Pillow

# Criar production_settings se não existir
cp setup/settings.py setup/production_settings.py

# Aplicar migrations
python3.10 manage.py migrate --settings=setup.production_settings

# Collectstatic FORÇADO
rm -rf staticfiles
python3.10 manage.py collectstatic --noinput --settings=setup.production_settings

# Verificar se funciona
python3.10 manage.py check --settings=setup.production_settings
```

### 🔥 PASSO 3: Configuração Web App (CRÍTICO!)
**No painel PythonAnywhere → Web Apps:**

1. **Static files** (seção Static files):
   - URL: `/static/` → Directory: `/home/prismaav/staticfiles`
   - URL: `/media/` → Directory: `/home/prismaav/media`

2. **WSGI file** (clique no link do WSGI file):
   ```python
   import os
   import sys
   
   path = '/home/prismaav'
   if path not in sys.path:
       sys.path.append(path)
   
   os.environ['DJANGO_SETTINGS_MODULE'] = 'setup.production_settings'
   
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

3. **Reload** (botão verde grande)

### 🔥 PASSO 4: Verificação final
```bash
# Verificar se imagem foi coletada
ls -la /home/prismaav/staticfiles/img/home2.jpg

# Testar Django diretamente
python3.10 -c "
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'setup.production_settings'
import django
django.setup()
from artigos.models import Artigo
print(f'Artigos: {Artigo.objects.count()}')
from django.conf import settings
print(f'ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}')
"
```

---

## 🚨 SE AINDA NÃO FUNCIONAR:

### Error Log Analysis
```bash
# Ver últimos erros
tail -n 50 /home/prismaav/logs/*.error.log

# OU no painel: Web Apps → Error log
```

### Problemas mais comuns:

**❌ Imagem não aparece:**
- Static files mapping AUSENTE no Web tab
- Collectstatic não executado
- Imagem não está em `/home/prismaav/static/img/home2.jpg`

**❌ Blog erro 500:**
- WSGI não usando production_settings
- Migrations não aplicadas
- .env com encoding corrompido
- Dependências faltando (Pillow)

**❌ Site não carrega:**
- ALLOWED_HOSTS incorreto
- WSGI file com erro de sintaxe
- Django não consegue importar settings

---

## 📞 ÚLTIMA TENTATIVA - Manual Override

Se NADA funcionar, force configuração manual:

```bash
# 1. Deletar tudo e recomeçar
rm -f .env
rm -rf staticfiles

# 2. Configuração mínima
echo "SECRET_KEY=emergency-key" > .env
echo "DEBUG=False" >> .env
echo "ALLOWED_HOSTS=prismaav.pythonanywhere.com" >> .env

# 3. Usar settings padrão temporariamente
python3.10 manage.py migrate
python3.10 manage.py collectstatic --noinput

# 4. No WSGI, usar:
# os.environ['DJANGO_SETTINGS_MODULE'] = 'setup.settings'
```

---

## 🎯 RESULTADO ESPERADO

Após executar tudo:
- ✅ Home: https://prismaav.pythonanywhere.com (com imagem)
- ✅ Blog: https://prismaav.pythonanywhere.com/blog/ (sem erro 500)

Se ainda falhar, copie o output do `diagnostico_emergencial.py` e as últimas linhas do Error log.
