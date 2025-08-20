"""
URLs para o app de artigos/blog
"""

from django.urls import path
from . import views

app_name = 'artigos'

urlpatterns = [
    # Lista de artigos - /blog/
    path('', views.lista_artigos, name='lista'),
    
    # Busca de artigos - /blog/buscar/
    path('buscar/', views.buscar_artigos, name='buscar'),
    
    # Artigos por tag - /blog/tag/<tag>/
    path('tag/<str:tag>/', views.artigos_por_tag, name='por_tag'),
    
    # Detalhe do artigo - /blog/<slug>/
    path('<slug:slug>/', views.detalhe_artigo, name='detalhe'),
]
