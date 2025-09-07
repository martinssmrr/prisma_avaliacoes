"""
Sitemap simplificado para resolver problemas de URL
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class SimpleSitemap(Sitemap):
    """
    Sitemap muito simples apenas com URLs básicas
    """
    protocol = 'https'
    changefreq = 'weekly'
    priority = 0.8
    
    def items(self):
        """URLs básicas testadas"""
        return [
            '/',  # Home
            '/blog/',  # Blog
        ]
    
    def location(self, item):
        """Retorna a própria URL"""
        return item
    
    def lastmod(self, item):
        """Data de modificação"""
        from datetime import datetime
        return datetime.now()


# Sitemap temporário simplificado
sitemaps_simple = {
    'main': SimpleSitemap,
}
