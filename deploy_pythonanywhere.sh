#!/bin/bash

# Script de Deploy para PythonAnywhere
# Execute este script no console Bash do PythonAnywhere

echo "🚀 Iniciando deploy da Prisma Avaliações..."

# 1. Clonar ou atualizar o repositório
if [ -d "prisma-avaliacoes" ]; then
    echo "📁 Atualizando repositório existente..."
    cd prisma-avaliacoes
    git pull origin master
else
    echo "📁 Clonando repositório..."
    git clone https://github.com/martinssmrr/prisma_avaliacoes.git prisma-avaliacoes
    cd prisma-avaliacoes
fi

# 2. Criar e ativar ambiente virtual
echo "🐍 Configurando ambiente virtual..."
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependências
echo "📦 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Executar migrações
echo "🗄️ Executando migrações do banco de dados..."
python manage.py migrate

# 5. Coletar arquivos estáticos
echo "📂 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# 6. Criar superusuário (se necessário)
echo "👤 Criando superusuário..."
python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@prisma.com', 'admin123')
    print('Superusuário criado!')
else:
    print('Superusuário já existe!')
EOF

# 7. Popular dados de exemplo
echo "📊 Populando dados de exemplo..."
python popular_dados.py

echo "✅ Deploy concluído!"
echo ""
echo "🔧 Próximos passos no PythonAnywhere:"
echo "1. Vá para a aba 'Web'"
echo "2. Clique em 'Add a new web app'"
echo "3. Escolha 'Manual configuration' com Python 3.10"
echo "4. Configure o WSGI file com o conteúdo de wsgi_pythonanywhere.py"
echo "5. Configure os diretórios estáticos:"
echo "   - URL: /static/ -> Directory: /home/seuusername/prisma-avaliacoes/staticfiles"
echo "   - URL: /media/ -> Directory: /home/seuusername/prisma-avaliacoes/media"
echo "6. Reload sua web app"
echo ""
echo "🌐 Sua aplicação estará disponível em: https://seuusername.pythonanywhere.com"
