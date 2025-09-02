#!/usr/bin/env python
"""
Script para verificar dados do dashboard
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dev_settings')
django.setup()

from controle.models import Cliente, Venda

def verificar_dados():
    print("=== VERIFICAÇÃO DOS DADOS DO DASHBOARD ===")
    print(f"📊 Total de Clientes: {Cliente.objects.count()}")
    print(f"📊 Total de Vendas: {Venda.objects.count()}")
    
    if Venda.objects.count() > 0:
        print("\n=== VENDAS EXISTENTES ===")
        for venda in Venda.objects.all()[:5]:
            print(f"ID: {venda.id} | Cliente: {venda.cliente} | Valor: R$ {venda.valor_total} | Venda Fechada: {venda.venda}")
    
    print(f"\n📊 Vendas Fechadas: {Venda.objects.filter(venda=True).count()}")
    print(f"📊 Vendas em Andamento: {Venda.objects.filter(venda=False).count()}")
    
    # Verificar URLs disponíveis
    print("\n=== TESTANDO ACESSO AO DASHBOARD ===")
    try:
        from django.test import Client
        client = Client()
        
        # Criar usuário admin temporário se não existir
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
            print("✅ Usuário admin criado")
        
        # Fazer login
        client.login(username='admin', password='admin123')
        
        # Testar dashboard
        response = client.get('/admin/controle/dashboard/')
        print(f"📱 Dashboard Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Dashboard acessível!")
        else:
            print(f"❌ Erro no dashboard: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Erro ao testar dashboard: {e}")

if __name__ == '__main__':
    verificar_dados()
