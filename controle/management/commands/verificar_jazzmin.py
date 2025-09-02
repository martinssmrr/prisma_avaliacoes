from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Verifica as configurações do Jazzmin'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n=== VERIFICAÇÃO JAZZMIN ==='))
        
        # Verificar configurações básicas
        jazzmin_settings = getattr(settings, 'JAZZMIN_SETTINGS', {})
        
        self.stdout.write(f"Site Title: {jazzmin_settings.get('site_title', 'Não definido')}")
        self.stdout.write(f"Site Header: {jazzmin_settings.get('site_header', 'Não definido')}")
        self.stdout.write(f"Site Brand: {jazzmin_settings.get('site_brand', 'Não definido')}")
        self.stdout.write(f"Site Logo: {jazzmin_settings.get('site_logo', 'Não definido')}")
        self.stdout.write(f"Login Logo: {jazzmin_settings.get('login_logo', 'Não definido')}")
        
        # Verificar se os arquivos existem
        import os
        from django.contrib.staticfiles.storage import staticfiles_storage
        
        site_logo = jazzmin_settings.get('site_logo')
        login_logo = jazzmin_settings.get('login_logo')
        
        if site_logo:
            try:
                logo_path = staticfiles_storage.path(site_logo)
                if os.path.exists(logo_path):
                    self.stdout.write(self.style.SUCCESS(f"✅ Site logo encontrada: {logo_path}"))
                else:
                    self.stdout.write(self.style.ERROR(f"❌ Site logo não encontrada: {logo_path}"))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"⚠️ Erro ao verificar site logo: {e}"))
        
        if login_logo:
            try:
                login_path = staticfiles_storage.path(login_logo)
                if os.path.exists(login_path):
                    self.stdout.write(self.style.SUCCESS(f"✅ Login logo encontrada: {login_path}"))
                else:
                    self.stdout.write(self.style.ERROR(f"❌ Login logo não encontrada: {login_path}"))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"⚠️ Erro ao verificar login logo: {e}"))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Verificação concluída!'))
