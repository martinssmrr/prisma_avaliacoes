#!/usr/bin/env python
"""
Script para demonstrar a flexibilidade do campo autor
"""

import os
import sys
import django
from datetime import datetime

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from artigos.models import Artigo

def demonstrar_flexibilidade_autor():
    """Demonstra como o campo autor agora é flexível"""
    
    print("🔧 Demonstrando flexibilidade do campo autor...")
    
    # Criar artigo com autor personalizado
    artigo_teste = Artigo.objects.create(
        titulo="Teste de Flexibilidade do Autor",
        slug="teste-flexibilidade-autor",
        autor="Dr. João Silva - Engenheiro Civil CREA 12345",
        resumo="Este artigo demonstra que agora qualquer nome pode ser usado como autor.",
        conteudo="<p>Agora o campo autor é totalmente flexível!</p>",
        meta_description="Teste de flexibilidade do campo autor",
        tags="teste, autor, flexibilidade",
        publicado=True,
        data_publicacao=datetime.now()
    )
    
    print(f"✓ Artigo criado com autor personalizado: {artigo_teste.autor}")
    
    # Atualizar um artigo existente com novo autor
    artigo_existente = Artigo.objects.filter(slug="como-funciona-avaliacao-imoveis-residenciais").first()
    if artigo_existente:
        artigo_existente.autor = "Eng. Maria Santos - Especialista em Avaliações"
        artigo_existente.save()
        print(f"✓ Artigo atualizado com novo autor: {artigo_existente.autor}")
    
    # Listar todos os autores únicos
    autores = Artigo.objects.values_list('autor', flat=True).distinct()
    print("\n📋 Autores atualmente no sistema:")
    for autor in autores:
        print(f"• {autor}")
    
    print("\n🎉 Demonstração concluída!")
    print("\n💡 Agora você pode:")
    print("• Usar qualquer nome como autor")
    print("• Incluir títulos e credenciais")
    print("• Não precisar criar usuários no sistema")
    print("• Editar livremente no Django Admin")

if __name__ == '__main__':
    demonstrar_flexibilidade_autor()
