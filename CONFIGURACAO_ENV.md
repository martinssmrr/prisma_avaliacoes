# 🔧 Configuração de Variáveis de Ambiente - Prisma Avaliações

Este documento explica como configurar e usar variáveis de ambiente no projeto Django da Prisma Avaliações Imobiliárias.

## 📋 Arquivos Criados

### 1. `.env` - Variáveis de Ambiente
Contém todas as configurações sensíveis do projeto:
- `SECRET_KEY`: Chave secreta do Django
- `DEBUG`: Modo de debug (True/False)
- `ALLOWED_HOSTS`: Hosts permitidos
- `DB_*`: Configurações do banco de dados
- `DJANGO_SUPERUSER_*`: Credenciais do superusuário

### 2. `.gitignore` - Arquivos Ignorados pelo Git
Lista completa de arquivos que não devem ser versionados:
- Arquivos `.env`
- Banco de dados SQLite
- Cache do Python
- Arquivos de log
- Diretórios de ambiente virtual

### 3. `settings.py` - Configurações Atualizadas
Agora usa variáveis de ambiente via `python-decouple`

### 4. Scripts de Criação de Superusuário
- `criar_superuser.py`: Script standalone
- `management/commands/criar_superuser_env.py`: Comando Django

## 🚀 Como Usar

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente
O arquivo `.env` já está criado com as configurações solicitadas:
- **Username**: `prismaav`
- **Password**: `PrismaAv4002@--`
- **Email**: `admin@prismaavaliacoes.com`

### 3. Executar Migrações
```bash
python manage.py migrate
```

### 4. Criar Superusuário (3 Métodos)

#### Método 1: Comando Django Personalizado (Recomendado)
```bash
python manage.py criar_superuser_env
```

Para forçar atualização se já existir:
```bash
python manage.py criar_superuser_env --force
```

#### Método 2: Script Standalone
```bash
python criar_superuser.py
```

#### Método 3: Comando Django Nativo
```bash
python manage.py createsuperuser
```
(Este método pedirá para digitar manualmente)

### 5. Iniciar Servidor
```bash
python manage.py runserver
```

### 6. Acessar Admin
- URL: http://127.0.0.1:8000/admin/
- Username: `prismaav`
- Password: `PrismaAv4002@--`

## 🔐 Configurações de Segurança

### Variáveis de Ambiente Principais

```env
# Segurança
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,seudominio.com

# Banco de Dados
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Superusuário
DJANGO_SUPERUSER_USERNAME=prismaav
DJANGO_SUPERUSER_PASSWORD=PrismaAv4002@--
DJANGO_SUPERUSER_EMAIL=admin@prismaavaliacoes.com
```

### Para Produção

1. **Altere as configurações**:
```env
DEBUG=False
SECRET_KEY=gere-uma-nova-chave-secreta
ALLOWED_HOSTS=seudominio.com,www.seudominio.com
```

2. **Para PostgreSQL**:
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=prisma_avaliacoes_db
DB_USER=postgres_user
DB_PASSWORD=senha_forte
DB_HOST=localhost
DB_PORT=5432
```

3. **Para MySQL**:
```env
DB_ENGINE=django.db.backends.mysql
DB_NAME=prisma_avaliacoes_db
DB_USER=mysql_user
DB_PASSWORD=senha_forte
DB_HOST=localhost
DB_PORT=3306
```

## 📁 Estrutura de Arquivos

```
projeto/
├── .env                          # ✅ Variáveis de ambiente (NÃO versionar)
├── .gitignore                    # ✅ Arquivos ignorados pelo Git
├── requirements.txt              # ✅ Dependências atualizadas
├── criar_superuser.py           # ✅ Script de criação de superusuário
├── setup/
│   └── settings.py              # ✅ Configurações com variáveis de ambiente
└── Prisma_avaliacoes/
    └── management/
        └── commands/
            └── criar_superuser_env.py  # ✅ Comando Django personalizado
```

## 🛠️ Comandos Úteis

### Verificar Configurações
```bash
python manage.py check
```

### Ver Configurações do Banco
```bash
python manage.py shell
>>> from django.conf import settings
>>> print(settings.DATABASES)
```

### Gerar Nova SECRET_KEY
```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
```

### Listar Usuários
```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.all()
```

### Alterar Senha do Superusuário
```bash
python manage.py changepassword prismaav
```

## 🚨 Boas Práticas de Segurança

### ✅ Faça
- Mantenha o `.env` fora do controle de versão
- Use senhas fortes para produção
- Gere nova `SECRET_KEY` para produção
- Configure `DEBUG=False` em produção
- Use HTTPS em produção

### ❌ Não Faça
- Não commite arquivos `.env`
- Não use senhas fracas
- Não deixe `DEBUG=True` em produção
- Não exponha informações sensíveis em logs

## 🔄 Atualizando Configurações

### Para alterar credenciais do superusuário:
1. Edite o arquivo `.env`
2. Execute: `python manage.py criar_superuser_env --force`

### Para adicionar novas variáveis:
1. Adicione no `.env`
2. Importe no `settings.py`:
```python
NOVA_VARIAVEL = config('NOVA_VARIAVEL', default='valor_padrao')
```

## 📞 Suporte

Para dúvidas sobre configuração:
1. Verifique se o `.env` está no diretório raiz
2. Confirme se `python-decouple` está instalado
3. Teste as configurações com `python manage.py check`

## 🎯 Próximos Passos

1. ✅ Configurações básicas concluídas
2. ⏳ Teste todas as funcionalidades
3. ⏳ Configure email SMTP (se necessário)
4. ⏳ Prepare para deploy em produção
