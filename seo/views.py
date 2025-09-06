"""
Views para SEO
"""
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .models import SEOConfig


@cache_page(60 * 60 * 24)  # Cache por 24 horas
@require_http_methods(["GET"])
def robots_txt(request):
    """
    View para gerar robots.txt dinamicamente
    """
    config = SEOConfig.get_config()
    
    # Conteúdo do robots.txt
    content = f"""User-agent: *
Allow: /

# Sitemaps
Sitemap: {config.get_full_domain()}/sitemap.xml

# Disallow admin and private areas
Disallow: /admin/
Disallow: /accounts/
Disallow: /api/
Disallow: /*.json$
Disallow: /*.xml$

# Allow static files and media
Allow: /static/
Allow: /media/

# Crawl delay (optional)
Crawl-delay: 1

# Popular bots specific rules
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: facebookexternalhit
Allow: /

User-agent: Twitterbot
Allow: /
"""
    
    return HttpResponse(content, content_type='text/plain')


@cache_page(60 * 60)  # Cache por 1 hora
@require_http_methods(["GET"])
def ads_txt(request):
    """
    View para gerar ads.txt (para Google AdSense)
    """
    # Adicione aqui suas configurações do Google AdSense
    content = """# Google AdSense
# google.com, pub-XXXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0

# Adicione outras redes de publicidade aqui
"""
    
    return HttpResponse(content, content_type='text/plain')


def sitemap_ping_view(request):
    """
    View para ping manual dos search engines
    """
    if not request.user.is_staff:
        return HttpResponse('Unauthorized', status=401)
    
    from django.core.management import call_command
    
    try:
        call_command('ping_search_engines')
        return HttpResponse('Sitemap ping enviado com sucesso!')
    except Exception as e:
        return HttpResponse(f'Erro ao enviar ping: {str(e)}', status=500)
