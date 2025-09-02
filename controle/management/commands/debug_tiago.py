from django.core.management.base import BaseCommand
from controle.models import Cliente
from django.contrib.auth import authenticate

class Command(BaseCommand):
    help = 'Debug cliente Tiago Martins'

    def handle(self, *args, **options):
        telefone = "77999515837"
        self.stdout.write(f"=== BUSCANDO CLIENTE COM TELEFONE {telefone} ===")
        
        try:
            # Buscar cliente pelo telefone exato
            cliente = Cliente.objects.get(telefone=telefone)
            self.stdout.write(self.style.SUCCESS(f"✅ Cliente encontrado:"))
            self.stdout.write(f"   ID: {cliente.id}")
            self.stdout.write(f"   Nome: {cliente.nome}")
            self.stdout.write(f"   Telefone: {cliente.telefone}")
            self.stdout.write(f"   Email: {cliente.email}")
            self.stdout.write(f"   Usuário: {cliente.usuario}")
            
            if cliente.usuario:
                self.stdout.write(f"   Username: {cliente.usuario.username}")
                self.stdout.write(f"   Usuário ativo: {cliente.usuario.is_active}")
                self.stdout.write(f"   Último login: {cliente.usuario.last_login}")
                
                # Testar autenticação
                senha_padrao = telefone[-4:]  # Últimos 4 dígitos
                self.stdout.write(f"   Testando senha padrão: {senha_padrao}")
                
                user = authenticate(username=cliente.usuario.username, password=senha_padrao)
                if user:
                    self.stdout.write(self.style.SUCCESS("   ✅ Autenticação com senha padrão funcionou"))
                else:
                    self.stdout.write(self.style.ERROR("   ❌ Autenticação com senha padrão falhou"))
                    
                    # Testar outras possibilidades
                    senhas_teste = [telefone, f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"]
                    for senha in senhas_teste:
                        user = authenticate(username=cliente.usuario.username, password=senha)
                        if user:
                            self.stdout.write(self.style.SUCCESS(f"   ✅ Autenticação com senha '{senha}' funcionou"))
                            break
                    else:
                        self.stdout.write(self.style.ERROR("   ❌ Nenhuma senha testada funcionou"))
            else:
                self.stdout.write(self.style.ERROR("   ❌ Cliente não tem usuário associado"))
                
        except Cliente.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"❌ Cliente com telefone {telefone} não encontrado"))
            
            # Buscar clientes similares
            self.stdout.write("\nBuscando clientes com telefones similares:")
            clientes_similares = Cliente.objects.filter(telefone__contains="5837")
            for c in clientes_similares:
                self.stdout.write(f"   - {c.nome}: {c.telefone}")
                
            # Buscar por nome
            self.stdout.write("\nBuscando por nome 'Tiago':")
            clientes_tiago = Cliente.objects.filter(nome__icontains="Tiago")
            for c in clientes_tiago:
                self.stdout.write(f"   - {c.nome}: {c.telefone}")

        self.stdout.write("\n=== RESUMO DE TODOS OS CLIENTES ===")
        todos_clientes = Cliente.objects.all()
        for c in todos_clientes:
            status_usuario = "✅ Com usuário" if c.usuario else "❌ Sem usuário"
            self.stdout.write(f"{c.id}: {c.nome} - {c.telefone} - {status_usuario}")
