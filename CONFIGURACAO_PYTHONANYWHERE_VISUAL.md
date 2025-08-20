# 🛠️ GUIA VISUAL - Configuração PythonAnywhere

## 🚨 PROBLEMA: Imagem não aparece + Blog erro 500

### ✅ CHECKLIST DE CONFIGURAÇÃO PYTHONANYWHERE

---

## 📋 PASSO 1: Console Commands
**Acesse: PythonAnywhere → Console → Bash**

```bash
# Navegar para projeto
cd /home/prismaav

# Atualizar código
git pull origin master

# Verificar status atual
python3.10 verificar_status_pythonanywhere.py

# Instalar dependências
pip3.10 install --user -r requirements.txt

# Migrações
python3.10 manage.py migrate --settings=setup.production_settings

# Coletar estáticos (IMPORTANTE!)
python3.10 manage.py collectstatic --noinput --settings=setup.production_settings

# Verificar configuração
python3.10 manage.py check --settings=setup.production_settings
```

---

## 📋 PASSO 2: Web App Configuration
**Acesse: PythonAnywhere → Web Apps → prismaav.pythonanywhere.com**

### 2.1 WSGI Configuration
- Clique em **"WSGI configuration file"**
- Verifique se contém:
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

### 2.2 Static Files Mapping (CRÍTICO!)
- Na seção **"Static files"**
- Adicione estas entradas:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/prismaav/staticfiles` |
| `/media/` | `/home/prismaav/media` |

**⚠️ SEM esta configuração, imagens NUNCA aparecerão!**

### 2.3 Source Code
- Verifique se **"Source code"** aponta para: `/home/prismaav`

---

## 📋 PASSO 3: Arquivo .env
**No console, edite o .env:**

```bash
nano .env
```

**Cole EXATAMENTE isto (sem acentos!):**
```env
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
**Salve:** `Ctrl+X`, `Y`, `Enter`

---

## 📋 PASSO 4: Upload da Imagem
**Se a imagem não estiver no servidor:**

1. **Via Files tab:**
   - Acesse: Files → `/home/prismaav/static/img/`
   - Upload `home2.jpg`

2. **Ou via console:**
```bash
# Criar diretório se não existir
mkdir -p /home/prismaav/static/img

# Verificar se imagem existe
ls -la /home/prismaav/static/img/home2.jpg
```

---

## 📋 PASSO 5: Reload & Test
1. **Web Apps → Reload** (botão verde)
2. **Aguarde** o reload completar
3. **Teste:**
   - Home: https://prismaav.pythonanywhere.com
   - Blog: https://prismaav.pythonanywhere.com/blog/

---

## 🚨 TROUBLESHOOTING

### Se IMAGEM ainda não aparece:
```bash
# Verificar se imagem foi coletada
ls -la /home/prismaav/staticfiles/img/home2.jpg

# Se não existir, executar collectstatic novamente
python3.10 manage.py collectstatic --noinput --settings=setup.production_settings

# Verificar Static Files mapping no Web tab
```

### Se BLOG ainda dá erro 500:
```bash
# Ver últimos erros
tail -n 50 /home/prismaav/logs/*.error.log

# Ou verificar Error log no Web tab
```

### Comandos de emergência:
```bash
# Resetar staticfiles
rm -rf /home/prismaav/staticfiles
python3.10 manage.py collectstatic --noinput --settings=setup.production_settings

# Verificar se Django funciona
python3.10 manage.py shell --settings=setup.production_settings
```

---

## 🎯 PONTOS CRÍTICOS

### ✅ Deve estar correto:
- [ ] **Static Files mapping:** `/static/` → `/home/prismaav/staticfiles`
- [ ] **WSGI file:** usando `setup.production_settings`
- [ ] **Arquivo .env:** sem caracteres especiais, com ALLOWED_HOSTS correto
- [ ] **Collectstatic:** executado com sucesso
- [ ] **Imagem:** em `/home/prismaav/static/img/home2.jpg`

### ❌ Erros comuns:
- **Static Files não mapeados** → Imagem 404
- **WSGI usando settings** → Não carrega .env
- **Collectstatic não executado** → Arquivos não servidos
- **Encoding .env** → Django não inicia

---

## 📞 RESULTADO ESPERADO
- ✅ **Home:** Imagem de fundo aparece
- ✅ **Blog:** Lista artigos sem erro 500
- ✅ **Admin:** Login funciona (prismaav/PrismaAv4002)
