"""
Context processors para SEO
"""
from .models import SEOConfig


def seo_context(request):
    """
    Context processor para injetar dados SEO em todos os templates
    
    Adiciona:
    - SITE_NAME
    - SITE_DOMAIN  
    - seo_config (configuração completa)
    """
    config = SEOConfig.get_config()
    
    return {
        'SITE_NAME': config.site_name,
        'SITE_DOMAIN': config.site_domain,
        'SITE_URL': config.get_full_domain(),
        'seo_config': config,
    }
