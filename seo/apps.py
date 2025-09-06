"""
Configuração do app SEO
"""
from django.apps import AppConfig


class SeoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'seo'
    verbose_name = 'SEO & Marketing'
    
    def ready(self):
        """Importar signals quando o app estiver pronto"""
        try:
            import seo.signals  # noqa F401
        except ImportError:
            pass
