#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from controle.models import Cliente, Venda
from django.utils import timezone
from decimal import Decimal

def criar_dados_exemplo():
    print("Criando dados de exemplo...")
    
    # Criar clientes
    clientes_dados = [
        {
            'nome': 'João Silva',
            'telefone': '(11) 99999-1111',
            'email': 'joao.silva@email.com',
            'cidade': 'São Paulo',
            'estado': 'SP'
        },
        {
            'nome': 'Maria Santos',
            'telefone': '(21) 88888-2222',
            'email': 'maria.santos@email.com',
            'cidade': 'Rio de Janeiro',
            'estado': 'RJ'
        },
        {
            'nome': 'Pedro Costa',
            'telefone': '(31) 77777-3333',
            'email': 'pedro.costa@email.com',
            'cidade': 'Belo Horizonte',
            'estado': 'MG'
        },
        {
            'nome': 'Ana Oliveira',
            'telefone': '(41) 66666-4444',
            'email': 'ana.oliveira@email.com',
            'cidade': 'Curitiba',
            'estado': 'PR'
        },
        {
            'nome': 'Carlos Ferreira',
            'telefone': '(51) 55555-5555',
            'email': 'carlos.ferreira@email.com',
            'cidade': 'Porto Alegre',
            'estado': 'RS'
        }
    ]
    
    clientes = []
    for dados in clientes_dados:
        cliente, created = Cliente.objects.get_or_create(
            nome=dados['nome'],
            defaults=dados
        )
        clientes.append(cliente)
        if created:
            print(f"Cliente criado: {cliente.nome}")
        else:
            print(f"Cliente já existe: {cliente.nome}")
    
    # Criar vendas com diferentes status
    vendas_dados = [
        {
            'cliente': clientes[0],
            'valor_total': Decimal('150000.00'),
            'orcamento': True,
            'venda': True,
            'documentacao': True,
            'sinal_1': True,
            'confeccao': True,
            'sinal_2': True,
            'envio': True,  # Venda concluída
            'observacoes': 'Venda finalizada com sucesso'
        },
        {
            'cliente': clientes[1],
            'valor_total': Decimal('200000.00'),
            'orcamento': True,
            'venda': True,
            'documentacao': True,
            'sinal_1': False,  # Em andamento
            'confeccao': False,
            'sinal_2': False,
            'envio': False,
            'observacoes': 'Cliente em processo de análise'
        },
        {
            'cliente': clientes[2],
            'valor_total': Decimal('180000.00'),
            'orcamento': True,
            'venda': False,  # Início do processo
            'documentacao': False,
            'sinal_1': False,
            'confeccao': False,
            'sinal_2': False,
            'envio': False,
            'observacoes': 'Orçamento aprovado, aguardando documentação'
        },
        {
            'cliente': clientes[3],
            'valor_total': Decimal('220000.00'),
            'orcamento': True,
            'venda': True,
            'documentacao': True,
            'sinal_1': True,
            'confeccao': True,
            'sinal_2': False,  # Quase concluída
            'envio': False,
            'observacoes': 'Aguardando segundo sinal'
        },
        {
            'cliente': clientes[4],
            'valor_total': Decimal('175000.00'),
            'orcamento': False,  # Apenas iniciada
            'venda': False,
            'documentacao': False,
            'sinal_1': False,
            'confeccao': False,
            'sinal_2': False,
            'envio': False,
            'observacoes': 'Contato inicial realizado'
        }
    ]
    
    for dados in vendas_dados:
        venda, created = Venda.objects.get_or_create(
            cliente=dados['cliente'],
            valor_total=dados['valor_total'],
            defaults=dados
        )
        if created:
            print(f"Venda criada: {venda.cliente.nome} - {venda.status_geral} ({venda.progresso_percentual}%)")
        else:
            print(f"Venda já existe: {venda.cliente.nome}")
    
    print("\nDados de exemplo criados com sucesso!")
    print(f"Total de clientes: {Cliente.objects.count()}")
    print(f"Total de vendas: {Venda.objects.count()}")
    
    # Estatísticas
    vendas_concluidas = Venda.objects.filter(envio=True).count()
    vendas_em_andamento = Venda.objects.exclude(
        orcamento=False, venda=False, documentacao=False,
        sinal_1=False, confeccao=False, sinal_2=False, envio=False
    ).exclude(envio=True).count()
    vendas_iniciadas = Venda.objects.filter(
        orcamento=False, venda=False, documentacao=False,
        sinal_1=False, confeccao=False, sinal_2=False, envio=False
    ).count()
    
    print(f"Vendas concluídas: {vendas_concluidas}")
    print(f"Vendas em andamento: {vendas_em_andamento}")
    print(f"Vendas iniciadas: {vendas_iniciadas}")

if __name__ == '__main__':
    criar_dados_exemplo()
