# 🔧 Solução de Problemas - PythonAnywhere

## ❌ Erro: "Host não permitido em /"

### 🔍 Diagnóstico:
```
Host não permitido em /
Cabeçalho HTTP_HOST inválido: 'prismaav.pythonanywhere.com'. 
Talvez seja necessário adicionar 'prismaav.pythonanywhere.com' a ALLOWED_HOSTS.
```

### ✅ **SOLUÇÕES IMPLEMENTADAS:**

#### 1. **Arquivo `.env` corrigido:**
```env
# Hosts permitidos (separados por vírgula)
ALLOWED_HOSTS=localhost,127.0.0.1,prismaav.pythonanywhere.com
```
> ⚠️ **Removido espaço em branco** que causava o erro

#### 2. **`production_settings.py` atualizado:**
```python
# Hosts permitidos - PythonAnywhere
ALLOWED_HOSTS = [
    'prismaav.pythonanywhere.com',  # Host correto
    'localhost',
    '127.0.0.1',
]
```

#### 3. **`wsgi_pythonanywhere.py` corrigido:**
```python
# Caminho correto no PythonAnywhere
path = '/home/prismaav/prisma_avaliacoes'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.production_settings')
```

## 🚀 **INSTRUÇÕES DE DEPLOY CORRIGIDAS**

### 1. **No Console Bash do PythonAnywhere:**

```bash
# Navegar para o diretório do projeto
cd ~/prisma_avaliacoes

# Executar script de verificação
python config_pythonanywhere.py

# Instalar dependências
pip install -r requirements.txt

# Executar migrações
python manage.py migrate --settings=setup.production_settings

# Coletar arquivos estáticos
python manage.py collectstatic --noinput --settings=setup.production_settings

# Verificar configuração
python manage.py check --settings=setup.production_settings --deploy
```

### 2. **Configurar Web App:**

#### **Arquivo WSGI** (copie conteúdo de `wsgi_pythonanywhere.py`):
```python
import os
import sys

path = '/home/prismaav/prisma_avaliacoes'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.production_settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

#### **Arquivos Estáticos:**
| URL | Directory |
|-----|-----------|
| `/static/` | `/home/prismaav/prisma_avaliacoes/staticfiles/` |
| `/media/` | `/home/prismaav/prisma_avaliacoes/media/` |

#### **Virtual Environment:**
```
/home/prismaav/.virtualenvs/prismaav.pythonanywhere.com/
```

### 3. **Reload da Web App**
- Clique no botão verde **"Reload prismaav.pythonanywhere.com"**

## 🔍 **VERIFICAÇÕES FINAIS**

### ✅ Checklist pós-deploy:

- [ ] Arquivo WSGI configurado corretamente
- [ ] Virtual Environment configurado
- [ ] Arquivos estáticos configurados
- [ ] Reload da Web App executado
- [ ] Site acessível em https://prismaav.pythonanywhere.com

### 🧪 **Testar Localmente:**

```bash
# Testar configuração local
python -c "from decouple import config; print('ALLOWED_HOSTS:', config('ALLOWED_HOSTS').split(','))"

# Testar Django settings
python manage.py check --settings=setup.production_settings
```

## 🚨 **Outros Problemas Comuns**

### **Erro 500 - Internal Server Error**
1. Verifique **Error log** na aba Web
2. Confirme se todas as dependências estão instaladas
3. Verifique se `DEBUG=False` em produção

### **Static Files não carregam**
1. Execute `collectstatic` novamente
2. Verifique configuração de diretórios estáticos
3. Confirme permissões dos arquivos

### **Database Error**
1. Execute migrações: `python manage.py migrate --settings=setup.production_settings`
2. Verifique se banco SQLite foi copiado
3. Crie superusuário se necessário

### **ImportError**
1. Verifique se ambiente virtual está ativo
2. Reinstale dependências: `pip install -r requirements.txt`
3. Confirme Python version (3.10)

## 📞 **Scripts de Diagnóstico**

### **Verificação completa:**
```bash
python config_pythonanywhere.py
```

### **Verificação de banco:**
```bash
python verificar_banco.py
```

### **Teste manual de configurações:**
```bash
python manage.py shell --settings=setup.production_settings
>>> from django.conf import settings
>>> print(settings.ALLOWED_HOSTS)
>>> print(settings.DEBUG)
```

## 🎯 **Status Atual**

### ✅ **Correções Aplicadas:**
- ✅ ALLOWED_HOSTS corrigido
- ✅ Espaços em branco removidos
- ✅ production_settings.py atualizado
- ✅ wsgi_pythonanywhere.py corrigido
- ✅ Scripts de diagnóstico criados

### 🚀 **Próximos Passos:**
1. Fazer commit das correções
2. Fazer push para o repositório
3. No PythonAnywhere: `git pull origin master`
4. Reload da Web App
5. Testar: https://prismaav.pythonanywhere.com

---

## 📝 **Log de Correções**

**Data**: 20 de agosto de 2025  
**Problema**: Host não permitido - prismaav.pythonanywhere.com  
**Causa**: Espaço em branco no final de ALLOWED_HOSTS no .env  
**Solução**: Removido espaço extra e atualizado todos os arquivos de configuração  
**Status**: ✅ **CORRIGIDO**
