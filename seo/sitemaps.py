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
    
    def get_config(self):
        """Obter configuração SEO"""
        try:
            return SEOConfig.get_config()
        except:
            return None
    
    def items(self):
        """URLs estáticas do site - apenas URLs que existem"""
        valid_items = []
        
        # Lista de URLs para testar
        test_items = [
            {'url_name': 'home', 'priority': 1.0, 'changefreq': 'daily'},
            {'url_name': 'artigos:lista', 'priority': 0.9, 'changefreq': 'daily'},
        ]
        
        for item in test_items:
            try:
                # Testar se a URL pode ser resolvida
                url = reverse(item['url_name'])
                if url:
                    valid_items.append(item)
            except:
                # Pular URLs que não podem ser resolvidas
                continue
                
        return valid_items
    
    def location(self, item):
        try:
            url = reverse(item['url_name'])
            return url
        except:
            # Se não conseguir resolver a URL, retornar None para pular
            return None
    
    def priority(self, item):
        return item.get('priority', 0.5)
    
    def changefreq(self, item):
        config = self.get_config()
        if config:
            return config.sitemap_changefreq
        return item.get('changefreq', 'monthly')


class ArtigosSitemap(Sitemap):
    """
    Sitemap para artigos do blog
    """
    changefreq = 'weekly'
    priority = 0.8
    protocol = 'https'
    
    def items(self):
        """Retorna todos os artigos publicados com slugs válidos"""
        try:
            # Tenta importar o modelo Artigo
            Artigo = apps.get_model('artigos', 'Artigo')
            # Filtrar apenas artigos com slug válido e não vazio
            artigos = Artigo.objects.filter(
                publicado=True,
                slug__isnull=False
            ).exclude(
                slug__exact=''
            ).order_by('-data_publicacao')
            
            # Validar que cada artigo tem get_absolute_url funcionando
            valid_artigos = []
            for artigo in artigos:
                try:
                    url = artigo.get_absolute_url()
                    if url and url != '/' and '/blog/' in url:
                        valid_artigos.append(artigo)
                except:
                    continue
            
            return valid_artigos
        except:
            # Se o modelo não existir, retorna lista vazia
            return []
    
    def lastmod(self, obj):
        """Data da última modificação"""
        return getattr(obj, 'data_atualizacao', getattr(obj, 'updated_at', None))
    
    def location(self, obj):
        """URL do artigo"""
        try:
            if hasattr(obj, 'get_absolute_url'):
                return obj.get_absolute_url()
            # Fallback para URL padrão
            return f'/blog/{obj.slug}/'
        except:
            return None
    
    def changefreq(self, obj):
        """Frequência de mudança baseada na configuração"""
        try:
            config = SEOConfig.get_config()
            return config.sitemap_changefreq
        except:
            return 'weekly'
    
    def priority(self, obj):
        """Prioridade baseada na configuração"""
        try:
            config = SEOConfig.get_config()
            return float(config.sitemap_priority)
        except:
            return 0.8


class SEOSitemap(Sitemap):
    """
    Sitemap dinâmico baseado nos objetos com SEO configurado
    """
    changefreq = 'weekly'
    priority = 0.7
    protocol = 'https'
    
    def items(self):
        """Retorna objetos que têm SEO configurado e URLs válidas"""
        from .models import SEOMeta
        
        seo_objects = []
        for seo_meta in SEOMeta.objects.filter(noindex=False):
            try:
                obj = seo_meta.content_object
                if obj and hasattr(obj, 'get_absolute_url'):
                    # Verificar se a URL é válida antes de adicionar
                    url = obj.get_absolute_url()
                    if url and url != '/':
                        seo_objects.append(obj)
            except:
                # Pular objetos com problemas
                continue
        
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
            return getattr(obj, 'updated_at', getattr(obj, 'data_atualizacao', None))
    
    def location(self, obj):
        """URL do objeto"""
        try:
            return obj.get_absolute_url()
        except:
            return None
    
    def changefreq(self, obj):
        """Frequência baseada na configuração"""
        try:
            config = SEOConfig.get_config()
            return config.sitemap_changefreq
        except:
            return 'weekly'
    
    def priority(self, obj):
        """Prioridade baseada na configuração"""
        try:
            config = SEOConfig.get_config()
            return float(config.sitemap_priority)
        except:
            return 0.7


# Dicionário de sitemaps para usar em urls.py
# Comentar temporariamente sitemaps problemáticos para depuração
sitemaps = {
    'static': StaticPagesSitemap,
    'artigos': ArtigosSitemap,
    # 'seo': SEOSitemap,  # Temporariamente desabilitado
}
