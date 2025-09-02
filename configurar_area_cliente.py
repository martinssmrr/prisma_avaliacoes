import os
import sys
import django

# Adicionar o diretório do projeto ao Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.contrib.auth.models import User
from controle.models import Cliente, Venda
from decimal import Decimal
import re


def criar_usuarios_para_clientes():
    """Criar usuários para todos os clientes existentes"""
    clientes_sem_usuario = Cliente.objects.filter(usuario__isnull=True)
    
    print(f"📱 Criando usuários para {clientes_sem_usuario.count()} clientes...")
    
    for cliente in clientes_sem_usuario:
        # Extrair apenas números do telefone
        telefone_numeros = re.sub(r'\D', '', cliente.telefone)
        
        if len(telefone_numeros) >= 4:
            # Criar username único baseado no telefone
            username = telefone_numeros
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{telefone_numeros}_{counter}"
                counter += 1
            
            # Senha padrão: últimos 4 dígitos do telefone
            senha_padrao = telefone_numeros[-4:]
            
            # Criar usuário
            user = User.objects.create_user(
                username=username,
                email=cliente.email or '',
                password=senha_padrao,
                first_name=cliente.nome.split()[0] if cliente.nome else '',
                last_name=' '.join(cliente.nome.split()[1:]) if len(cliente.nome.split()) > 1 else ''
            )
            
            # Associar ao cliente
            cliente.usuario = user
            cliente.save()
            
            print(f"✅ Usuário criado para {cliente.nome}")
            print(f"   📞 Login: {cliente.telefone}")
            print(f"   🔑 Senha: {senha_padrao}")
            print(f"   👤 Username: {username}")
            print()


def atualizar_vendas_exemplo():
    """Adicionar campos novos às vendas existentes"""
    vendas = Venda.objects.all()
    
    print(f"📊 Atualizando {vendas.count()} vendas com novos campos...")
    
    for i, venda in enumerate(vendas):
        # Simular alguns cenários diferentes
        if venda.confeccao:  # Se confecção está concluída
            if i % 3 == 0:  # 1/3 das vendas: segundo sinal pago
                venda.segundo_sinal_pago = True
                print(f"✅ Venda #{venda.id}: 2º sinal marcado como pago")
            else:  # 2/3 das vendas: pode pagar segundo sinal
                venda.segundo_sinal_pago = False
                print(f"💰 Venda #{venda.id}: disponível para pagamento do 2º sinal")
        
        venda.save()


def mostrar_resumo():
    """Mostrar resumo dos dados criados"""
    print("\n" + "="*50)
    print("📈 RESUMO DA ÁREA DO CLIENTE")
    print("="*50)
    
    total_clientes = Cliente.objects.count()
    clientes_com_usuario = Cliente.objects.filter(usuario__isnull=False).count()
    total_vendas = Venda.objects.count()
    vendas_pode_pagar = Venda.objects.filter(confeccao=True, segundo_sinal_pago=False).count()
    vendas_pode_baixar = Venda.objects.filter(confeccao=True, segundo_sinal_pago=True).count()
    
    print(f"👥 Total de Clientes: {total_clientes}")
    print(f"🔐 Clientes com Acesso: {clientes_com_usuario}")
    print(f"🛒 Total de Vendas: {total_vendas}")
    print(f"💳 Vendas Podem Pagar 2º Sinal: {vendas_pode_pagar}")
    print(f"📄 Vendas Podem Baixar Documento: {vendas_pode_baixar}")
    
    print("\n📋 CREDENCIAIS DE ACESSO:")
    print("-" * 30)
    
    for cliente in Cliente.objects.filter(usuario__isnull=False)[:5]:
        telefone_numeros = re.sub(r'\D', '', cliente.telefone)
        senha = telefone_numeros[-4:] if len(telefone_numeros) >= 4 else '0000'
        
        print(f"👤 {cliente.nome}")
        print(f"   📞 Login: {cliente.telefone}")
        print(f"   🔑 Senha: {senha}")
        print(f"   🌐 URL: http://127.0.0.1:8000/area-cliente/")
        print()


def main():
    print("🚀 CONFIGURANDO ÁREA DO CLIENTE")
    print("=" * 40)
    
    # Criar usuários para clientes
    criar_usuarios_para_clientes()
    
    # Atualizar vendas
    atualizar_vendas_exemplo()
    
    # Mostrar resumo
    mostrar_resumo()
    
    print("✨ Configuração concluída!")
    print("\n💡 PRÓXIMOS PASSOS:")
    print("1. Acesse: http://127.0.0.1:8000/area-cliente/")
    print("2. Use o telefone como login e os últimos 4 dígitos como senha")
    print("3. Teste as funcionalidades da área do cliente")
    print("4. Configure documentos PDF no Django Admin")


if __name__ == "__main__":
    main()
