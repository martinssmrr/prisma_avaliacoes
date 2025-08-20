# 🚨 CORREÇÃO RÁPIDA - PythonAnywhere
## Imagem não aparece + Blog não funciona

### 🔥 EXECUTE ESTES COMANDOS NO CONSOLE DO PYTHONANYWHERE:

```bash
# 1. Navegue para o diretório do projeto
cd /home/prismaav/

# 2. Atualize o repositório
git pull origin master

# 3. Execute o diagnóstico
python3.10 diagnostico_pythonanywhere.py

# 4. Execute as correções
python3.10 corrigir_problemas_pythonanywhere.py

# 5. RELOAD da Web App (no painel do PythonAnywhere)
```

---

## 🎯 CORREÇÃO MANUAL SE OS SCRIPTS FALHAREM:

### PASSO 1: Corrigir arquivo .env
```bash
nano .env
```
**Cole EXATAMENTE isto (SEM caracteres especiais):**
```
SECRET_KEY=django-insecure-prisma-av-pythonanywhere-key-2025
DEBUG=False
ALLOWED_HOSTS=prismaav.pythonanywhere.com,localhost,127.0.0.1,testserver
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DJANGO_SUPERUSER_USERNAME=prismaav
DJANGO_SUPERUSER_PASSWORD=PrismaAv4002
DJANGO_SUPERUSER_EMAIL=admin@prismaavaliacoes.com
STATIC_URL=/static/
STATIC_ROOT=staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=media
```

### PASSO 2: Verificar WSGI file
```bash
nano /var/www/prismaav_pythonanywhere_com_wsgi.py
```
**Deve conter:**
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

### PASSO 3: Criar diretórios e executar comandos
```bash
# Criar diretórios
mkdir -p static/img
mkdir -p media/artigos/imagens
mkdir -p staticfiles

# Executar Django
python3.10 manage.py migrate --settings=setup.production_settings
python3.10 manage.py collectstatic --noinput --settings=setup.production_settings
```

### PASSO 4: Upload da imagem
1. Faça upload de `home2.jpg` para `/home/prismaav/static/img/`
2. Execute collectstatic novamente:
```bash
python3.10 manage.py collectstatic --noinput --settings=setup.production_settings
```

### PASSO 5: Verificar imagem
```bash
ls -la static/img/home2.jpg
ls -la staticfiles/img/home2.jpg
```

### PASSO 6: RELOAD Web App
1. Vá para **Web Apps** no painel
2. Clique em **Reload** 
3. Aguarde o reload completar

---

## 🧪 TESTES:

### ✅ Teste 1: Home page
- Acesse: https://prismaav.pythonanywhere.com
- **Deve**: Mostrar imagem de fundo

### ✅ Teste 2: Blog page  
- Acesse: https://prismaav.pythonanywhere.com/blog/
- **Deve**: Listar artigos (não erro 500)

### ✅ Teste 3: Admin
- Acesse: https://prismaav.pythonanywhere.com/admin/
- **Login**: prismaav / PrismaAv4002

---

## 🚨 SE AINDA NÃO FUNCIONAR:

### 1. Verificar Error Log
- Vá para **Web Apps** → **Error log**
- Veja os últimos erros

### 2. Problemas comuns:

**❌ ALLOWED_HOSTS error:**
```bash
# Verificar .env
cat .env | grep ALLOWED_HOSTS
```

**❌ Static files 404:**
```bash
# Verificar collectstatic
python3.10 manage.py collectstatic --noinput --settings=setup.production_settings
```

**❌ Import errors:**
```bash
# Testar settings
python3.10 manage.py check --settings=setup.production_settings
```

---

## 📞 RESUMO DA SOLUÇÃO:

### Root Cause: 
1. **Arquivo .env** com caracteres especiais causando erro de codificação
2. **WSGI** não usando production_settings
3. **Collectstatic** não executado ou imagem ausente

### Fix Applied:
1. ✅ .env limpo sem caracteres especiais
2. ✅ WSGI configurado para production_settings  
3. ✅ Collectstatic executado
4. ✅ Diretórios criados
5. ✅ Scripts de diagnóstico e correção

### Expected Result:
- 🖼️ **Imagem**: Aparece na home
- 📝 **Blog**: Funciona sem erro 500
- 🎯 **Site**: 100% operacional
