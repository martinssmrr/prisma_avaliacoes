"""
URLs para o app Prisma_avaliacoes
Configuração das rotas da landing page
"""

from django.urls import path
from . import views

app_name = 'Prisma_avaliacoes'

urlpatterns = [
    # Página inicial (landing page)
    path('', views.home, name='home'),
    
    # Página de contato (caso queira uma página separada no futuro)
    path('contato/', views.contato, name='contato'),
]
