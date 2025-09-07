# 🚨 PROBLEMA: git pull origin master não atualiza o projeto

## 🔍 **POSSÍVEIS CAUSAS:**

### **1. Mudanças Locais Conflitantes**
- Arquivos modificados localmente impedem o pull
- Git bloqueia para evitar perda de dados

### **2. Problemas de Permissões**
- Usuário sem permissão para escrever
- Proprietário dos arquivos incorreto

### **3. Repositório Corrompido**
- Índice Git corrompido
- Referências quebradas

### **4. Problemas de Conectividade**
- Sem acesso ao GitHub
- Firewall bloqueando

### **5. Branch Incorreta**
- Não está na branch master
- Tracking incorreto

---

## ⚡ **SOLUÇÕES IMEDIATAS:**

### **OPÇÃO 1 - Diagnóstico Primeiro (Recomendado):**
```bash
cd /var/www/prisma_avaliacoes
bash diagnosticar_git.sh
```
**Isso mostra:**
- Status do repositório
- Mudanças locais
- Conectividade
- Branch atual
- Permissões

### **OPÇÃO 2 - Força Atualização:**
```bash
cd /var/www/prisma_avaliacoes
bash forcar_git_pull.sh
```
**Isso faz:**
- Backup automático
- Salva mudanças locais
- Força reset para origin/master
- Re-clona se necessário

### **OPÇÃO 3 - Comandos Manuais:**
```bash
cd /var/www/prisma_avaliacoes

# Verificar status
git status

# Salvar mudanças locais
git stash

# Forçar atualização
git fetch origin
git reset --hard origin/master

# Verificar resultado
git log --oneline -3
```

### **OPÇÃO 4 - Re-clonar Completo:**
```bash
cd /var/www
mv prisma_avaliacoes prisma_avaliacoes_backup
git clone https://github.com/martinssmrr/prisma_avaliacoes.git
cd prisma_avaliacoes
```

---

## 🔧 **PROBLEMAS ESPECÍFICOS E SOLUÇÕES:**

### **"working tree is dirty"**
```bash
git stash
git pull origin master
```

### **"cannot lock ref"**
```bash
rm -rf .git/refs/heads/*
git fetch origin
git reset --hard origin/master
```

### **"Permission denied"**
```bash
sudo chown -R root:root /var/www/prisma_avaliacoes
cd /var/www/prisma_avaliacoes
git pull origin master
```

### **"fatal: not a git repository"**
```bash
cd /var/www
rm -rf prisma_avaliacoes
git clone https://github.com/martinssmrr/prisma_avaliacoes.git
```

### **"Network is unreachable"**
```bash
# Testar conectividade
ping github.com

# Usar HTTPS em vez de SSH
git remote set-url origin https://github.com/martinssmrr/prisma_avaliacoes.git
git pull origin master
```

---

## 🎯 **VERIFICAÇÃO DE SUCESSO:**

Após qualquer solução, verifique:

```bash
# 1. Arquivos atualizados existem?
ls -la corrigir_sem_logs.sh diagnosticar_servidor.sh

# 2. Último commit está correto?
git log --oneline -1

# 3. Branch está correta?
git branch

# 4. Arquivos específicos do SEO existem?
ls -la seo/ simple_sitemap.py
```

---

## 🚀 **SEQUÊNCIA RECOMENDADA:**

```bash
# 1. Diagnosticar
bash diagnosticar_git.sh

# 2. Se necessário, forçar
bash forcar_git_pull.sh

# 3. Aplicar correções do sitemap
bash corrigir_sem_logs.sh

# 4. Verificar resultado
curl https://prismaavaliacoes.com.br/sitemap.xml | grep -o "https://[^<]*" | head -3
```

---

## 💡 **DICAS IMPORTANTES:**

1. **Sempre fazer backup** antes de comandos destrutivos
2. **git stash** salva mudanças locais temporariamente
3. **git reset --hard** é destrutivo mas resolve a maioria dos problemas
4. **Re-clonar** é a solução mais radical mas sempre funciona
5. **Verificar permissões** se comandos falharem

---

## 📞 **SE NADA FUNCIONAR:**

```bash
# Última tentativa - re-clone forçado
cd /var/www
rm -rf prisma_avaliacoes
git clone https://github.com/martinssmrr/prisma_avaliacoes.git
chown -R root:root prisma_avaliacoes
cd prisma_avaliacoes
bash corrigir_sem_logs.sh
```

**⚡ Execute o diagnóstico primeiro para entender o problema específico!**
