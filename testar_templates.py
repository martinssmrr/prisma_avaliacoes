#!/usr/bin/env python
"""
Script para testar templates após correção do campo autor
"""

import os
import sys
import django
from django.test import RequestFactory
from django.template import Context, Template
from django.template.loader import render_to_string

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from artigos.models import Artigo
from django.http import HttpRequest

def testar_templates():
    """Testa se os templates estão renderizando corretamente"""
    
    print("🔧 Testando templates após correção do campo autor...")
    
    # Pegar um artigo para teste
    artigo = Artigo.objects.filter(publicado=True).first()
    
    if not artigo:
        print("❌ Nenhum artigo encontrado para teste")
        return
    
    print(f"📝 Testando com artigo: '{artigo.titulo}'")
    print(f"👤 Autor: {artigo.autor}")
    
    # Criar request mock
    factory = RequestFactory()
    request = factory.get('/')
    
    # Teste 1: Renderização básica do campo autor
    try:
        template_content = """
        <p>Autor: {{ artigo.autor }}</p>
        <p>Primeira letra: {{ artigo.autor.0 }}</p>
        """
        template = Template(template_content)
        context = Context({'artigo': artigo})
        resultado = template.render(context)
        
        print("✅ Template básico renderizado com sucesso")
        print(f"   Resultado: {resultado.strip()}")
        
    except Exception as e:
        print(f"❌ Erro no template básico: {e}")
    
    # Teste 2: Meta tags do detalhe
    try:
        meta_template = """<meta property="article:author" content="{{ artigo.autor }}">"""
        template = Template(meta_template)
        context = Context({'artigo': artigo})
        resultado = template.render(context)
        
        print("✅ Meta tags renderizadas com sucesso")
        print(f"   Resultado: {resultado}")
        
    except Exception as e:
        print(f"❌ Erro nas meta tags: {e}")
    
    # Teste 3: Avatar circle (primeira letra)
    try:
        avatar_template = """<div class="avatar">{{ artigo.autor.0 }}</div>"""
        template = Template(avatar_template)
        context = Context({'artigo': artigo})
        resultado = template.render(context)
        
        print("✅ Avatar renderizado com sucesso")
        print(f"   Resultado: {resultado}")
        
    except Exception as e:
        print(f"❌ Erro no avatar: {e}")
    
    print("\n🎉 Todos os testes de template concluídos!")
    print("\n💡 Campo autor agora funciona como texto simples:")
    print(f"   • Valor completo: '{artigo.autor}'")
    print(f"   • Primeira letra: '{artigo.autor[0] if artigo.autor else ''}'")

if __name__ == '__main__':
    testar_templates()
