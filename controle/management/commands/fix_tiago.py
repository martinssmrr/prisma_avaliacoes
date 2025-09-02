from django.core.management.base import BaseCommand
from controle.models import Cliente
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class Command(BaseCommand):
    help = 'Resolver problema de login do Tiago Martins'

    def handle(self, *args, **options):
        telefone = "77999515837"
        
        try:
            cliente = Cliente.objects.get(telefone=telefone)
            self.stdout.write(f"Cliente encontrado: {cliente.nome}")
            
            if cliente.usuario:
                usuario = cliente.usuario
                self.stdout.write(f"Usuário: {usuario.username}")
                
                # Testar senha atual
                senha_atual = telefone[-4:]  # 5837
                user = authenticate(username=usuario.username, password=senha_atual)
                
                if user:
                    self.stdout.write(self.style.SUCCESS(f"✅ Senha atual ({senha_atual}) funciona"))
                else:
                    self.stdout.write(self.style.WARNING(f"❌ Senha atual ({senha_atual}) não funciona"))
                    
                    # Resetar senha para o padrão
                    self.stdout.write("Resetando senha para o padrão...")
                    usuario.set_password(senha_atual)
                    usuario.save()
                    
                    # Testar novamente
                    user = authenticate(username=usuario.username, password=senha_atual)
                    if user:
                        self.stdout.write(self.style.SUCCESS(f"✅ Senha resetada com sucesso!"))
                    else:
                        self.stdout.write(self.style.ERROR(f"❌ Erro ao resetar senha"))
                        
                # Verificar se usuário está ativo
                if not usuario.is_active:
                    self.stdout.write("Ativando usuário...")
                    usuario.is_active = True
                    usuario.save()
                    
                self.stdout.write(f"Status final:")
                self.stdout.write(f"- Usuário ativo: {usuario.is_active}")
                self.stdout.write(f"- Último login: {usuario.last_login}")
                
            else:
                self.stdout.write(self.style.ERROR("Cliente não tem usuário associado"))
                
        except Cliente.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Cliente com telefone {telefone} não encontrado"))
