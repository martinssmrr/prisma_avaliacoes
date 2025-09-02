#!/usr/bin/env python3

from controle.models import Cliente
from django.contrib.auth.models import User

print("=== BUSCANDO CLIENTE TIAGO MARTINS ===")

# Buscar cliente pelo telefone
telefone = "77999515837"
print(f"Buscando cliente com telefone: {telefone}")

try:
    # Buscar cliente pelo telefone exato
    cliente = Cliente.objects.get(telefone=telefone)
    print(f"✅ Cliente encontrado:")
    print(f"   ID: {cliente.id}")
    print(f"   Nome: {cliente.nome}")
    print(f"   Telefone: {cliente.telefone}")
    print(f"   Email: {cliente.email}")
    print(f"   Usuário: {cliente.usuario}")
    
    if cliente.usuario:
        print(f"   Username: {cliente.usuario.username}")
        print(f"   Usuário ativo: {cliente.usuario.is_active}")
        print(f"   Último login: {cliente.usuario.last_login}")
        
        # Testar autenticação
        from django.contrib.auth import authenticate
        senha_padrao = telefone[-4:]  # Últimos 4 dígitos
        print(f"   Testando senha padrão: {senha_padrao}")
        
        user = authenticate(username=cliente.usuario.username, password=senha_padrao)
        if user:
            print("   ✅ Autenticação com senha padrão funcionou")
        else:
            print("   ❌ Autenticação com senha padrão falhou")
            
            # Testar outras possibilidades
            senhas_teste = [telefone, telefone.replace("77", "(77)"), telefone.replace("77", "(77) ")]
            for senha in senhas_teste:
                user = authenticate(username=cliente.usuario.username, password=senha)
                if user:
                    print(f"   ✅ Autenticação com senha '{senha}' funcionou")
                    break
            else:
                print("   ❌ Nenhuma senha testada funcionou")
    else:
        print("   ❌ Cliente não tem usuário associado")
        
except Cliente.DoesNotExist:
    print(f"❌ Cliente com telefone {telefone} não encontrado")
    
    # Buscar clientes similares
    print("\nBuscando clientes com telefones similares:")
    clientes_similares = Cliente.objects.filter(telefone__contains="77999515837")
    for c in clientes_similares:
        print(f"   - {c.nome}: {c.telefone}")
        
    # Buscar por nome
    print("\nBuscando por nome 'Tiago':")
    clientes_tiago = Cliente.objects.filter(nome__icontains="Tiago")
    for c in clientes_tiago:
        print(f"   - {c.nome}: {c.telefone}")

print("\n=== TODOS OS CLIENTES ===")
todos_clientes = Cliente.objects.all()
for c in todos_clientes:
    status_usuario = "✅ Com usuário" if c.usuario else "❌ Sem usuário"
    print(f"{c.id}: {c.nome} - {c.telefone} - {status_usuario}")
