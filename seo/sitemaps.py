"""
Sitemaps para SEO
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.apps import apps
from .models import SEOConfig


class StaticPagesSitemap(Sitemap):
    """
    Sitemap para páginas estáticas
    """
    protocol = 'https'
    
    def items(self):
        """URLs estáticas do site"""
        return [
            {'url_name': 'home', 'priority': 1.0, 'changefreq': 'daily'},
            {'url_name': 'sobre', 'priority': 0.8, 'changefreq': 'monthly'},
            {'url_name': 'servicos', 'priority': 0.9, 'changefreq': 'monthly'},
            {'url_name': 'contato', 'priority': 0.8, 'changefreq': 'monthly'},
            {'url_name': 'artigos:lista', 'priority': 0.9, 'changefreq': 'daily'},
        ]
    
    def location(self, item):
        try:
            return reverse(item['url_name'])
        except:
            return '/'
    
    def priority(self, item):
        return item.get('priority', 0.5)
    
    def changefreq(self, item):
        return item.get('changefreq', 'monthly')


class ArtigosSitemap(Sitemap):
    """
    Sitemap para artigos do blog
    """
    changefreq = 'weekly'
    priority = 0.8
    protocol = 'https'
    
    def items(self):
        """Retorna todos os artigos publicados"""
        try:
            # Tenta importar o modelo Artigo
            Artigo = apps.get_model('artigos', 'Artigo')
            return Artigo.objects.filter(publicado=True).order_by('-data_publicacao')
        except:
            # Se o modelo não existir, retorna lista vazia
            return []
    
    def lastmod(self, obj):
        """Data da última modificação"""
        return getattr(obj, 'data_atualizacao', getattr(obj, 'updated_at', None))
    
    def location(self, obj):
        """URL do artigo"""
        if hasattr(obj, 'get_absolute_url'):
            return obj.get_absolute_url()
        return f'/artigos/{obj.slug}/'
    
    def changefreq(self, obj):
        """Frequência de mudança baseada na idade do artigo"""
        config = SEOConfig.get_config()
        return config.sitemap_changefreq
    
    def priority(self, obj):
        """Prioridade baseada na data de publicação"""
        config = SEOConfig.get_config()
        return float(config.sitemap_priority)


class SEOSitemap(Sitemap):
    """
    Sitemap dinâmico baseado nos objetos com SEO configurado
    """
    changefreq = 'weekly'
    priority = 0.7
    protocol = 'https'
    
    def items(self):
        """Retorna objetos que têm SEO configurado"""
        from .models import SEOMeta
        
        seo_objects = []
        for seo_meta in SEOMeta.objects.filter(noindex=False):
            if seo_meta.content_object and hasattr(seo_meta.content_object, 'get_absolute_url'):
                seo_objects.append(seo_meta.content_object)
        
        return seo_objects
    
    def lastmod(self, obj):
        """Data da última modificação do SEO"""
        from .models import SEOMeta
        from django.contrib.contenttypes.models import ContentType
        
        try:
            content_type = ContentType.objects.get_for_model(obj)
            seo_meta = SEOMeta.objects.get(
                content_type=content_type,
                object_id=obj.pk
            )
            return seo_meta.updated_at
        except SEOMeta.DoesNotExist:
            return None
    
    def location(self, obj):
        """URL do objeto"""
        return obj.get_absolute_url()


# Dicionário de sitemaps para usar em urls.py
sitemaps = {
    'static': StaticPagesSitemap,
    'artigos': ArtigosSitemap,
    'seo': SEOSitemap,
}
