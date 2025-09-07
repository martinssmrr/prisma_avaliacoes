"""
URL configuration for setuurlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("Prisma_avaliacoes.urls")),
    path("blog/", include("artigos.urls")),
    path("area-cliente/", include("area_cliente.urls")),  # Nova área do cliente
    
    # SEO URLs
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', lambda r: HttpResponse("User-agent: *\nAllow: /\nSitemap: http://127.0.0.1:8000/sitemap.xml", content_type="text/plain")),
].

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

# Importar sitemaps do SEO - Temporariamente usando sitemap simples
# from seo.sitemaps import sitemaps
from simple_sitemap import sitemaps_simple as sitemaps

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("Prisma_avaliacoes.urls")),
    path("blog/", include("artigos.urls")),
    path("area-cliente/", include("area_cliente.urls")),  # Área do cliente
    
    # SEO URLs
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('seo.urls')),  # Inclui robots.txt, ads.txt, etc.
]

# Servir arquivos de media em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
