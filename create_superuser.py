import os
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.contrib.auth.models import User

# Criar superusuário
if not User.objects.filter(username='prismaav').exists():
    User.objects.create_superuser(
        username='prismaav',
        email='admin@prismaavaliacoes.com.br',
        password='PrismaAV4002@--'
    )
    print("✅ Superusuário 'prismaav' criado com sucesso!")
else:
    print("⚠️ Usuário 'prismaav' já existe.")
