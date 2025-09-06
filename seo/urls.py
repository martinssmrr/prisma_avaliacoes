"""
URLs para SEO
"""
from django.urls import path
from . import views

app_name = 'seo'

urlpatterns = [
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('ads.txt', views.ads_txt, name='ads_txt'),
    path('admin/ping-sitemap/', views.sitemap_ping_view, name='ping_sitemap'),
]
