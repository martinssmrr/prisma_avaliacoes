# 🖼️ Correção: Imagens não aparecem no PythonAnywhere

## ❌ **PROBLEMA:**
A imagem da home não aparece no site do PythonAnywhere, mas funciona localmente.

## 🔍 **CAUSA:**
- Imagem estava sendo referenciada como `/media/home2.jpg` (caminho absoluto)
- No PythonAnywhere, arquivos estáticos precisam estar em `staticfiles/`
- Configuração de arquivos estáticos mal configurada

## ✅ **SOLUÇÕES APLICADAS:**

### 1. **Correção do Template**
**Arquivo**: `templates/Prisma_avaliacoes/home.html`

**ANTES (incorreto)**:
```html
<section style="background-image: url('/media/home2.jpg');">
```

**DEPOIS (correto)**:
```html
{% load static %}
<section style="background-image: url('{% static 'img/home2.jpg' %}');">
```

### 2. **Reorganização dos Arquivos**
- ✅ Movido `media/home2.jpg` → `static/img/home2.jpg`
- ✅ Imagem agora é um arquivo estático (não mídia)
- ✅ Será coletada pelo `collectstatic`

### 3. **Configuração de Arquivos Estáticos**

**Verificar no PythonAnywhere Web App:**

| URL | Directory | Status |
|-----|-----------|--------|
| `/static/` | `/home/prismaav/prisma_avaliacoes/staticfiles/` | ✅ |
| `/media/` | `/home/prismaav/prisma_avaliacoes/media/` | ✅ |

## 🚀 **DEPLOY NO PYTHONANYWHERE:**

### **Script Automático** (Recomendado):
```bash
cd ~/prisma_avaliacoes
git pull origin master
python deploy_emergencia.py
```

### **Comandos Manuais**:
```bash
cd ~/prisma_avaliacoes

# Atualizar código
git pull origin master

# Instalar dependências
pip3.10 install --user -r requirements.txt

# Coletar arquivos estáticos (incluindo imagens)
python3.10 manage.py collectstatic --noinput --settings=setup.production_settings

# Verificar se imagem foi coletada
ls -la staticfiles/img/
```

### **Verificação**:
```bash
# Deve mostrar home2.jpg
ls staticfiles/img/home2.jpg
```

## 🔧 **CONFIGURAÇÃO PYTHONANYWHERE**

### **Aba Web → Static Files:**

Certifique-se que está configurado:

```
URL: /static/
Directory: /home/prismaav/prisma_avaliacoes/staticfiles/
```

### **Teste de URL:**
- **Local**: http://127.0.0.1:8000/static/img/home2.jpg
- **Produção**: https://prismaav.pythonanywhere.com/static/img/home2.jpg

## ⚡ **SOLUÇÃO RÁPIDA (2 MINUTOS):**

1. **Console PythonAnywhere:**
```bash
cd ~/prisma_avaliacoes
git pull origin master
python3.10 manage.py collectstatic --noinput --settings=setup.production_settings
```

2. **Reload Web App**

3. **Teste**: https://prismaav.pythonanywhere.com

## 🚨 **TROUBLESHOOTING**

### **Imagem ainda não aparece?**

1. **Verificar arquivo coletado:**
```bash
ls -la ~/prisma_avaliacoes/staticfiles/img/home2.jpg
```

2. **Verificar URL direta:**
```
https://prismaav.pythonanywhere.com/static/img/home2.jpg
```

3. **Verificar configuração Static Files:**
   - Aba Web → Static files
   - URL: `/static/`
   - Directory: `/home/prismaav/prisma_avaliacoes/staticfiles/`

4. **Verificar Error Log:**
   - Aba Web → Error log

### **Erro 404 em imagens?**

Execute:
```bash
cd ~/prisma_avaliacoes
python3.10 manage.py findstatic img/home2.jpg --settings=setup.production_settings
```

### **Permissões de arquivo:**
```bash
chmod 644 ~/prisma_avaliacoes/staticfiles/img/home2.jpg
```

## 📁 **Estrutura Corrigida:**

```
prisma_avaliacoes/
├── static/
│   ├── css/
│   ├── js/
│   └── img/
│       └── home2.jpg          # ✅ Imagem aqui
├── staticfiles/               # ✅ Gerado pelo collectstatic
│   └── img/
│       └── home2.jpg          # ✅ Coletado automaticamente
├── media/                     # Para uploads de usuários
└── templates/
    └── Prisma_avaliacoes/
        └── home.html          # ✅ Template corrigido
```

## 🎯 **RESULTADO ESPERADO:**

Após a correção:
- ✅ Imagem aparece na home
- ✅ Template usa `{% static %}` corretamente  
- ✅ Arquivos estáticos organizados
- ✅ Deploy funciona no PythonAnywhere

## 📝 **RESUMO DAS ALTERAÇÕES:**

1. ✅ **Template corrigido** - usa `{% static %}` 
2. ✅ **Imagem movida** - `media/` → `static/img/`
3. ✅ **Script atualizado** - verifica imagens
4. ✅ **Documentação criada** - guia completo

---

## ⏰ **CRONOGRAMA:**

- ✅ **0-1 min**: Git pull + collectstatic
- ✅ **1-2 min**: Reload Web App  
- ✅ **2-3 min**: Teste do site
- ✅ **RESOLVIDO!** 🖼️✨
