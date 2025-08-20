# 🚨 SOLUÇÃO EMERGENCIAL - ALLOWED_HOSTS

## ❌ **ERRO PERSISTENTE:**
```
Host não permitido em /
Cabeçalho HTTP_HOST inválido: 'prismaav.pythonanywhere.com'
```

## 🚀 **SOLUÇÃO RÁPIDA (3 MINUTOS):**

### **Opção 1: Script Automático** ⚡

No **Console Bash** do PythonAnywhere:

```bash
cd ~/prisma_avaliacoes
git pull origin master
python deploy_emergencia.py
```

### **Opção 2: Correção Manual** 🔧

1. **Console Bash** do PythonAnywhere:
```bash
cd ~/prisma_avaliacoes
```

2. **Criar arquivo .env**:
```bash
cat > .env << 'EOF'
SECRET_KEY=django-insecure-(=-&$c%lq2!cxtmdwinj4uw&yftv$0*jsgn*)ew)%accjk@gk$
DEBUG=False
ALLOWED_HOSTS=prismaav.pythonanywhere.com,localhost,127.0.0.1
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DJANGO_SUPERUSER_USERNAME=prismaav
DJANGO_SUPERUSER_PASSWORD=PrismaAv4002@--
DJANGO_SUPERUSER_EMAIL=admin@prismaavaliacoes.com
EOF
```

3. **Instalar dependências**:
```bash
pip3.10 install --user python-decouple django pillow
```

4. **Executar migrações**:
```bash
python3.10 manage.py migrate --settings=setup.production_settings
```

5. **Coletar estáticos**:
```bash
python3.10 manage.py collectstatic --noinput --settings=setup.production_settings
```

### **Opção 3: Força Bruta** 💪

Se nada funcionar, edite diretamente o `production_settings.py`:

```bash
nano ~/prisma_avaliacoes/setup/production_settings.py
```

E force esta configuração no final do arquivo:
```python
# CORREÇÃO FORÇADA
ALLOWED_HOSTS = ['prismaav.pythonanywhere.com', 'localhost', '127.0.0.1', '*']
DEBUG = False
```

## ⚡ **PASSO FINAL OBRIGATÓRIO:**

Após QUALQUER correção:

1. **Aba Web** do PythonAnywhere
2. **Reload** `prismaav.pythonanywhere.com`
3. **Aguardar 30 segundos**
4. **Testar**: https://prismaav.pythonanywhere.com

## 🔍 **VERIFICAÇÃO:**

Teste se funcionou:
```bash
cd ~/prisma_avaliacoes
python3.10 -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.production_settings')
django.setup()
from django.conf import settings
print('ALLOWED_HOSTS:', settings.ALLOWED_HOSTS)
"
```

**Resultado esperado:**
```
ALLOWED_HOSTS: ['prismaav.pythonanywhere.com', 'localhost', '127.0.0.1']
```

## 🚨 **SE AINDA NÃO FUNCIONAR:**

1. **Verifique Error Log** na aba Web
2. **Confirme arquivo WSGI** (deve usar `setup.production_settings`)
3. **Execute**: `python3.10 manage.py check --deploy --settings=setup.production_settings`
4. **Reinicie** completamente a Web App

## 📱 **SUPORTE TÉCNICO:**

- **Error Log**: Aba Web → Error log
- **Server Log**: Aba Web → Server log  
- **Console**: Tasks → Consoles → Bash

---

## ⏰ **CRONOGRAMA DE AÇÃO:**

- ✅ **0-2 min**: Executar script ou correção manual
- ✅ **2-3 min**: Reload da Web App
- ✅ **3-4 min**: Teste do site
- ✅ **RESOLVIDO!** 🎉
