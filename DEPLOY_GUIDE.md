# 🚀 Guia Completo de Deploy - PythonAnywhere

Este guia fornece instruções passo a passo para fazer o deploy da **Prisma Avaliações Imobiliárias** no PythonAnywhere.

## 📋 Pré-requisitos

1. Conta no PythonAnywhere (gratuita ou paga)
2. Repositório Git atualizado
3. Arquivos de configuração criados:
   - `production_settings.py`
   - `wsgi_pythonanywhere.py`
   - `requirements.txt`

## 🔧 Passo 1: Configuração Inicial no PythonAnywhere

### 1.1 Acesse o Console Bash
- Faça login no PythonAnywhere
- Vá para **Tasks** → **Consoles**
- Clique em **Bash**

### 1.2 Clone o Repositório
```bash
git clone https://github.com/martinssmrr/prisma_avaliacoes.git
cd prisma_avaliacoes
```

### 1.3 Crie e Ative o Ambiente Virtual
```bash
python3.10 -m venv venv
source venv/bin/activate
```

### 1.4 Instale as Dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 🗄️ Passo 2: Configuração do Banco de Dados

### 2.1 Execute as Migrações
```bash
python manage.py migrate --settings=setup.production_settings
```

### 2.2 Crie um Superusuário
```bash
python manage.py createsuperuser --settings=setup.production_settings
```

### 2.3 Colete Arquivos Estáticos
```bash
python manage.py collectstatic --noinput --settings=setup.production_settings
```

### 2.4 Popule Dados de Exemplo (Opcional)
```bash
python popular_dados.py
```

## 🌐 Passo 3: Configuração da Web App

### 3.1 Criar Nova Web App
1. Vá para a aba **Web**
2. Clique em **Add a new web app**
3. Escolha **Manual configuration**
4. Selecione **Python 3.10**

### 3.2 Configurar o WSGI File
1. Na seção **Code**, clique no link do arquivo WSGI
2. **Substitua** todo o conteúdo pelo conteúdo do arquivo `wsgi_pythonanywhere.py`
3. **Importante**: Altere `'seuusername'` pelo seu username real do PythonAnywhere
4. Salve o arquivo

### 3.3 Configurar o Virtual Environment
1. Na seção **Virtualenv**, insira o caminho:
   ```
   /home/seuusername/prisma_avaliacoes/venv
   ```
   (Substitua `seuusername` pelo seu username)

### 3.4 Configurar Arquivos Estáticos
Na seção **Static files**, adicione:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/seuusername/prisma_avaliacoes/staticfiles/` |
| `/media/` | `/home/seuusername/prisma_avaliacoes/media/` |

**Importante**: Substitua `seuusername` pelo seu username real.

## 🔐 Passo 4: Variáveis de Ambiente (Opcional)

Para maior segurança, configure variáveis de ambiente:

### 4.1 No Console Bash, edite o arquivo .bashrc:
```bash
nano ~/.bashrc
```

### 4.2 Adicione as variáveis:
```bash
export SECRET_KEY='sua-secret-key-aqui'
export DEBUG=False
export ALLOWED_HOSTS='seuusername.pythonanywhere.com'
```

### 4.3 Recarregue as variáveis:
```bash
source ~/.bashrc
```

## 🎯 Passo 5: Finalizando o Deploy

### 5.1 Reload da Web App
1. Volte para a aba **Web**
2. Clique no botão verde **Reload seuusername.pythonanywhere.com**

### 5.2 Teste a Aplicação
1. Acesse: `https://seuusername.pythonanywhere.com`
2. Verifique se a página inicial carrega
3. Teste o admin: `https://seuusername.pythonanywhere.com/admin/`
4. Teste o blog: `https://seuusername.pythonanywhere.com/artigos/`

## 📊 Passo 6: Monitoramento e Logs

### 6.1 Verificar Logs de Erro
Na aba **Web**, seção **Log files**:
- **Error log**: Mostra erros da aplicação
- **Server log**: Mostra logs do servidor

### 6.2 Comandos Úteis de Manutenção
```bash
# Ativar ambiente virtual
source ~/prisma_avaliacoes/venv/bin/activate

# Atualizar código
cd ~/prisma_avaliacoes
git pull origin master

# Executar migrações
python manage.py migrate --settings=setup.production_settings

# Coletar estáticos
python manage.py collectstatic --noinput --settings=setup.production_settings

# Criar backup do banco
cp db.sqlite3 db_backup_$(date +%Y%m%d).sqlite3
```

## 🚨 Solução de Problemas Comuns

### Problema: ImportError ou ModuleNotFoundError
**Solução**: Verifique se todas as dependências estão instaladas:
```bash
pip install -r requirements.txt
```

### Problema: Static files não carregam
**Solução**: 
1. Execute `collectstatic` novamente
2. Verifique os caminhos na configuração de Static files

### Problema: 500 Internal Server Error
**Solução**:
1. Verifique o Error log na aba Web
2. Confirme se o WSGI file está correto
3. Verifique se as variáveis de ambiente estão configuradas

### Problema: Database locked
**Solução**:
```bash
# No console Bash
fuser db.sqlite3
# Se houver processos, mate-os e tente novamente
```

## 🔄 Atualizações Futuras

Para atualizar a aplicação:

1. **Atualizar código:**
```bash
cd ~/prisma_avaliacoes
git pull origin master
```

2. **Instalar novas dependências:**
```bash
pip install -r requirements.txt
```

3. **Executar migrações:**
```bash
python manage.py migrate --settings=setup.production_settings
```

4. **Coletar estáticos:**
```bash
python manage.py collectstatic --noinput --settings=setup.production_settings
```

5. **Reload da Web App** na interface do PythonAnywhere

## 📞 Suporte

- **Documentação PythonAnywhere**: https://help.pythonanywhere.com/
- **Fórum PythonAnywhere**: https://www.pythonanywhere.com/forums/
- **Django Documentation**: https://docs.djangoproject.com/

---

## 🎉 Parabéns!

Sua aplicação **Prisma Avaliações Imobiliárias** está agora online e acessível em:
`https://seuusername.pythonanywhere.com`

Não se esqueça de:
- ✅ Testar todas as funcionalidades
- ✅ Configurar um domínio personalizado (se necessário)
- ✅ Fazer backups regulares do banco de dados
- ✅ Monitorar logs regularmente
