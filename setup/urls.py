"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from artigos.sitemaps import ArtigoSitemap, StaticPagesSitemap

# Configuração dos sitemaps
sitemaps = {
    'artigos': ArtigoSitemap,
    'static': StaticPagesSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("Prisma_avaliacoes.urls")),
    path("blog/", include("artigos.urls")),
    
    # SEO URLs
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', lambda r: HttpResponse("User-agent: *\nAllow: /\nSitemap: {}/sitemap.xml".format(r.build_absolute_uri('/')[:-1]), content_type="text/plain")),
]

# Servir arquivos de media em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
