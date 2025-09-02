from django.urls import path
from . import views

app_name = 'area_cliente'

urlpatterns = [
    path('', views.login_cliente, name='login'),
    path('login/', views.login_cliente, name='login'),
    path('logout/', views.logout_cliente, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('minhas-compras/', views.minhas_compras, name='minhas_compras'),
    path('pagar-segundo-sinal/<int:venda_id>/', views.pagar_segundo_sinal, name='pagar_segundo_sinal'),
    path('baixar-documento/<int:venda_id>/', views.baixar_documento, name='baixar_documento'),
    path('trocar-senha/', views.trocar_senha, name='trocar_senha'),
    path('suporte/', views.suporte, name='suporte'),
]
