from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from .models import Artigo

class ArtigoSitemap(Sitemap):
    """Sitemap para artigos do blog"""
    changefreq = 'weekly'
    priority = 0.8
    
    def items(self):
        return Artigo.objects.filter(
            publicado=True,
            data_publicacao__lte=timezone.now()
        ).order_by('-data_publicacao')
    
    def lastmod(self, obj):
        return obj.data_atualizacao
    
    def location(self, obj):
        return obj.get_absolute_url()

class StaticPagesSitemap(Sitemap):
    """Sitemap para páginas estáticas"""
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        return ['artigos:lista', 'Prisma_avaliacoes:home']
    
    def location(self, item):
        return reverse(item)
