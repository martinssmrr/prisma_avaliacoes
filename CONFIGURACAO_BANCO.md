# 🗄️ Configuração de Banco de Dados - Prisma Avaliações

Este documento explica como configurar diferentes tipos de banco de dados no projeto Django da Prisma Avaliações Imobiliárias.

## 📋 Configuração Atual (SQLite)

O projeto está configurado para usar **SQLite** por padrão, que é ideal para desenvolvimento local.

### ⚙️ Configuração no `.env`:
```env
# Banco de dados SQLite (desenvolvimento local)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

### 🔧 Configuração no `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': config('DB_NAME', default=BASE_DIR / 'db.sqlite3'),
        'USER': config('DB_USER', default=''),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default=''),
        'PORT': config('DB_PORT', default=''),
    }
}
```

## 🚀 Comandos Básicos SQLite

### Executar Migrações:
```bash
python manage.py migrate
```

### Criar Superusuário:
```bash
python manage.py criar_superuser_env
```

### Backup do Banco:
```bash
# Criar backup
cp db.sqlite3 backup_$(date +%Y%m%d_%H%M%S).sqlite3

# No Windows PowerShell
Copy-Item db.sqlite3 "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').sqlite3"
```

### Restaurar Backup:
```bash
# Substituir banco atual
cp backup_20250820_153000.sqlite3 db.sqlite3
```

## 🗄️ Outras Configurações de Banco

### PostgreSQL (Recomendado para Produção)

#### 1. Instalar dependências:
```bash
pip install psycopg2-binary
```

#### 2. Configurar no `.env`:
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=prisma_avaliacoes_db
DB_USER=postgres_user
DB_PASSWORD=sua_senha_forte
DB_HOST=localhost
DB_PORT=5432
```

#### 3. Criar banco no PostgreSQL:
```sql
CREATE DATABASE prisma_avaliacoes_db;
CREATE USER postgres_user WITH PASSWORD 'sua_senha_forte';
GRANT ALL PRIVILEGES ON DATABASE prisma_avaliacoes_db TO postgres_user;
```

### MySQL/MariaDB

#### 1. Instalar dependências:
```bash
pip install mysqlclient
```

#### 2. Configurar no `.env`:
```env
DB_ENGINE=django.db.backends.mysql
DB_NAME=prisma_avaliacoes_db
DB_USER=mysql_user
DB_PASSWORD=sua_senha_forte
DB_HOST=localhost
DB_PORT=3306
```

#### 3. Criar banco no MySQL:
```sql
CREATE DATABASE prisma_avaliacoes_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'mysql_user'@'localhost' IDENTIFIED BY 'sua_senha_forte';
GRANT ALL PRIVILEGES ON prisma_avaliacoes_db.* TO 'mysql_user'@'localhost';
FLUSH PRIVILEGES;
```

## 🔐 Segurança de Banco de Dados

### ✅ Boas Práticas Implementadas:

1. **Arquivo SQLite no `.gitignore`**:
```gitignore
# Banco de dados local
*.sqlite3
*.sqlite3-journal
db.sqlite3
db.sqlite3-journal
```

2. **Credenciais em variáveis de ambiente**:
```env
# Nunca versionar senhas no código!
DB_PASSWORD=senha_forte_aqui
```

3. **Configurações flexíveis**:
```python
# settings.py usa defaults seguros
'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3')
```

### 🛡️ Para Produção:

1. **Use bancos dedicados** (PostgreSQL/MySQL)
2. **Senhas fortes** com caracteres especiais
3. **Conexões SSL** quando possível
4. **Backups automáticos** regulares
5. **Acesso restrito** ao banco

## 📊 Monitoramento e Manutenção

### Verificar Tamanho do Banco:
```bash
# SQLite
ls -lh db.sqlite3

# Windows
Get-ChildItem db.sqlite3 | Select-Object Name, Length
```

### Verificar Migrações:
```bash
python manage.py showmigrations
```

### Exportar/Importar Dados:
```bash
# Exportar
python manage.py dumpdata > backup_data.json

# Importar
python manage.py loaddata backup_data.json
```

### Shell do Banco:
```bash
# SQLite
python manage.py dbshell

# Ou usar sqlite3 diretamente
sqlite3 db.sqlite3
```

## 🔄 Migração Entre Bancos

### SQLite → PostgreSQL:

1. **Exportar dados do SQLite**:
```bash
python manage.py dumpdata > dados_sqlite.json
```

2. **Configurar PostgreSQL no `.env`**
3. **Executar migrações**:
```bash
python manage.py migrate
```

4. **Importar dados**:
```bash
python manage.py loaddata dados_sqlite.json
```

## 🚨 Troubleshooting

### Erro "database is locked":
```bash
# Verificar processos usando o banco
fuser db.sqlite3

# Ou reiniciar o servidor Django
python manage.py runserver
```

### Erro de migração:
```bash
# Resetar migrações (CUIDADO - perde dados!)
python manage.py migrate app_name zero
python manage.py migrate
```

### Erro de permissão:
```bash
# Verificar permissões do arquivo
chmod 664 db.sqlite3
```

## 📈 Performance

### SQLite Otimizado:
```python
# Para SQLite com melhor performance
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 60,
            'check_same_thread': False,
        }
    }
}
```

### Para sites com alto tráfego:
- Use **PostgreSQL** ou **MySQL**
- Configure **connection pooling**
- Implemente **cache** (Redis/Memcached)
- Use **read replicas** se necessário

## 📞 Suporte

Para problemas com banco de dados:
1. Verifique logs: `python manage.py check`
2. Teste conexão: `python manage.py dbshell`
3. Verifique permissões de arquivo
4. Consulte documentação Django: https://docs.djangoproject.com/en/5.2/ref/databases/
