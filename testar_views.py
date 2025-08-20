#!/usr/bin/env python
"""
Script para testar as views do blog após correção do campo autor
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from artigos.models import Artigo
from django.utils import timezone

def testar_views():
    """Testa as consultas das views"""
    
    print("🔧 Testando views do blog...")
    
    # Teste 1: Lista de artigos (equivalente à view lista_artigos)
    try:
        artigos = Artigo.objects.filter(
            publicado=True,
            data_publicacao__lte=timezone.now()
        ).order_by('-data_publicacao')
        
        print(f"✅ Lista de artigos: {artigos.count()} artigos encontrados")
        
        for artigo in artigos[:3]:
            print(f"   • {artigo.titulo} - Autor: {artigo.autor}")
            
    except Exception as e:
        print(f"❌ Erro na lista de artigos: {e}")
    
    # Teste 2: Busca por tag (equivalente à view artigos_por_tag)
    try:
        artigos_tag = Artigo.objects.filter(
            publicado=True,
            data_publicacao__lte=timezone.now(),
            tags__icontains='avaliação'
        ).order_by('-data_publicacao')
        
        print(f"✅ Busca por tag 'avaliação': {artigos_tag.count()} artigos encontrados")
        
    except Exception as e:
        print(f"❌ Erro na busca por tag: {e}")
    
    # Teste 3: Busca textual (equivalente à view buscar_artigos)
    try:
        from django.db.models import Q
        
        busca = 'imóvel'
        artigos_busca = Artigo.objects.filter(
            publicado=True,
            data_publicacao__lte=timezone.now()
        ).filter(
            Q(titulo__icontains=busca) |
            Q(resumo__icontains=busca) |
            Q(tags__icontains=busca)
        ).order_by('-data_publicacao')[:10]
        
        print(f"✅ Busca textual '{busca}': {len(artigos_busca)} artigos encontrados")
        
    except Exception as e:
        print(f"❌ Erro na busca textual: {e}")
    
    # Teste 4: Detalhes de um artigo
    try:
        artigo = Artigo.objects.filter(publicado=True).first()
        if artigo:
            print(f"✅ Detalhes do artigo: '{artigo.titulo}' - Autor: {artigo.autor}")
        else:
            print("⚠️ Nenhum artigo publicado encontrado")
            
    except Exception as e:
        print(f"❌ Erro nos detalhes do artigo: {e}")
    
    print("\n🎉 Todos os testes concluídos!")

if __name__ == '__main__':
    testar_views()
