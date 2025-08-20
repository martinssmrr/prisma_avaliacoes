"""
Comando Django personalizado para criar superusuário a partir de variáveis de ambiente
Execute: python manage.py criar_superuser_env
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decouple import config
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = 'Cria superusuário usando variáveis de ambiente do arquivo .env'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Força a criação mesmo se o usuário já existir (atualiza senha)',
        )

    def handle(self, *args, **options):
        # Obter credenciais das variáveis de ambiente
        username = config('DJANGO_SUPERUSER_USERNAME', default='admin')
        password = config('DJANGO_SUPERUSER_PASSWORD', default='admin123')
        email = config('DJANGO_SUPERUSER_EMAIL', default='admin@exemplo.com')
        
        self.stdout.write(
            self.style.SUCCESS('🏢 Prisma Avaliações - Criação de Superusuário')
        )
        self.stdout.write('=' * 50)
        self.stdout.write(f'📧 Username: {username}')
        self.stdout.write(f'📧 Email: {email}')
        
        # Verificar se usuário já existe
        if User.objects.filter(username=username).exists():
            if options['force']:
                user = User.objects.get(username=username)
                user.set_password(password)
                user.email = email
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Superusuário "{username}" atualizado!')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Superusuário "{username}" já existe!')
                )
                self.stdout.write(
                    'Use --force para atualizar ou escolha outro username no .env'
                )
            return
        
        try:
            # Validar dados
            if len(password) < 8:
                raise ValidationError('Senha deve ter pelo menos 8 caracteres')
            
            # Criar superusuário
            user = User.objects.create_superuser(
                username=username,
                password=password,
                email=email
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Superusuário "{username}" criado com sucesso!')
            )
            self.stdout.write(f'🔑 Username: {username}')
            self.stdout.write(f'🔒 Password: {"*" * len(password)}')
            self.stdout.write(f'📧 Email: {email}')
            self.stdout.write('')
            self.stdout.write('🌐 Acesse o admin em: http://127.0.0.1:8000/admin/')
            
        except ValidationError as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro de validação: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro ao criar superusuário: {e}')
            )
