from django.core.management.base import BaseCommand
from controle.models import Cliente
from django.contrib.auth import authenticate

class Command(BaseCommand):
    help = 'Testar login do Tiago com telefone formatado'

    def handle(self, *args, **options):
        # Simular exatamente o que acontece no formulário
        telefone_formatado = "(77) 99951-5837"
        senha = "5837"
        
        self.stdout.write(f"=== TESTE LOGIN TIAGO ===")
        self.stdout.write(f"Telefone como digitado: '{telefone_formatado}'")
        self.stdout.write(f"Senha: '{senha}'")
        
        # Aplicar a mesma limpeza da view
        telefone_limpo = ''.join(filter(str.isdigit, telefone_formatado))
        self.stdout.write(f"Telefone após limpeza: '{telefone_limpo}'")
        
        try:
            # Buscar cliente pelo telefone limpo
            cliente = Cliente.objects.get(telefone=telefone_limpo)
            self.stdout.write(self.style.SUCCESS(f"✅ Cliente encontrado: {cliente.nome}"))
            
            if cliente.usuario:
                # Testar autenticação
                user = authenticate(username=cliente.usuario.username, password=senha)
                if user:
                    self.stdout.write(self.style.SUCCESS(f"✅ Autenticação OK! Login funcionaria."))
                else:
                    self.stdout.write(self.style.ERROR(f"❌ Falha na autenticação"))
            else:
                self.stdout.write(self.style.ERROR(f"❌ Cliente sem usuário"))
                
        except Cliente.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"❌ Cliente não encontrado com telefone: {telefone_limpo}"))
