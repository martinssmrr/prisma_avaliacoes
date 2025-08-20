#!/usr/bin/env python
"""
Script para criar superusuário automaticamente usando variáveis de ambiente
Execute: python criar_superuser.py
"""

import os
import django
from decouple import config

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.contrib.auth.models import User

def criar_superuser():
    """Cria superusuário usando variáveis de ambiente"""
    
    # Obter credenciais do arquivo .env
    username = config('DJANGO_SUPERUSER_USERNAME', default='admin')
    password = config('DJANGO_SUPERUSER_PASSWORD', default='admin123')
    email = config('DJANGO_SUPERUSER_EMAIL', default='admin@exemplo.com')
    
    print("🔐 Criando superusuário...")
    print(f"📧 Username: {username}")
    print(f"📧 Email: {email}")
    
    # Verificar se já existe
    if User.objects.filter(username=username).exists():
        print(f"⚠️  Superusuário '{username}' já existe!")
        
        # Perguntar se quer atualizar
        resposta = input("Deseja atualizar a senha? (s/N): ").lower()
        if resposta == 's':
            user = User.objects.get(username=username)
            user.set_password(password)
            user.email = email
            user.save()
            print("✅ Senha do superusuário atualizada!")
        else:
            print("❌ Operação cancelada.")
        return
    
    try:
        # Criar superusuário
        user = User.objects.create_superuser(
            username=username,
            password=password,
            email=email
        )
        
        print("✅ Superusuário criado com sucesso!")
        print(f"🔑 Username: {username}")
        print(f"🔒 Password: {'*' * len(password)}")
        print(f"📧 Email: {email}")
        print("\n🌐 Acesse o admin em: http://127.0.0.1:8000/admin/")
        
    except Exception as e:
        print(f"❌ Erro ao criar superusuário: {e}")

if __name__ == '__main__':
    print("🏢 Prisma Avaliações Imobiliárias - Criação de Superusuário")
    print("=" * 60)
    criar_superuser()
