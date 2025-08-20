#!/usr/bin/env python3
"""
Script de diagnóstico para erro 500 no blog e problemas de imagem
Execute: python diagnostico_blog.py
"""

import os
import sys
import django
from pathlib import Path

def configurar_django():
    """Configura Django para o script"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
        django.setup()
        return True
    except Exception as e:
        print(f"❌ Erro ao configurar Django: {e}")
        return False

def verificar_artigos():
    """Verifica se há problemas com os artigos"""
    try:
        from artigos.models import Artigo
        
        print("📝 Verificando artigos...")
        
        # Contar artigos
        total = Artigo.objects.count()
        publicados = Artigo.objects.filter(publicado=True).count()
        
        print(f"✅ Total de artigos: {total}")
        print(f"✅ Artigos publicados: {publicados}")
        
        # Verificar artigos com problemas
        artigos_com_problema = []
        
        for artigo in Artigo.objects.all():
            problemas = []
            
            # Verificar se tem autor
            if not artigo.autor:
                problemas.append("Sem autor")
            
            # Verificar se tem imagem e se o arquivo existe
            if artigo.imagem_destacada:
                if not os.path.exists(artigo.imagem_destacada.path):
                    problemas.append("Imagem não encontrada")
            
            # Verificar slug
            if not artigo.slug:
                problemas.append("Sem slug")
            
            if problemas:
                artigos_com_problema.append({
                    'id': artigo.id,
                    'titulo': artigo.titulo,
                    'problemas': problemas
                })
        
        if artigos_com_problema:
            print("\n⚠️ Artigos com problemas:")
            for artigo in artigos_com_problema:
                print(f"  ID {artigo['id']}: {artigo['titulo']}")
                for problema in artigo['problemas']:
                    print(f"    - {problema}")
        else:
            print("✅ Todos os artigos estão OK")
        
        return len(artigos_com_problema) == 0
        
    except Exception as e:
        print(f"❌ Erro ao verificar artigos: {e}")
        return False

def verificar_templates():
    """Verifica se os templates existem"""
    
    print("\n📄 Verificando templates...")
    
    templates = [
        'artigos/lista_artigos.html',
        'artigos/detalhe_artigo.html',
        'artigos/buscar_artigos.html',
        'base.html'
    ]
    
    todos_ok = True
    
    for template in templates:
        caminho = Path('templates') / template
        if caminho.exists():
            print(f"✅ {template}")
        else:
            print(f"❌ {template} - NÃO ENCONTRADO")
            todos_ok = False
    
    return todos_ok

def verificar_arquivos_estaticos():
    """Verifica arquivos estáticos"""
    
    print("\n📁 Verificando arquivos estáticos...")
    
    # Verificar pasta static
    static_path = Path('static')
    if static_path.exists():
        print("✅ Pasta static/ existe")
        
        # Verificar subpastas
        subpastas = ['css', 'js', 'img']
        for pasta in subpastas:
            pasta_path = static_path / pasta
            if pasta_path.exists():
                arquivos = list(pasta_path.glob('*'))
                print(f"✅ static/{pasta}/ - {len(arquivos)} arquivo(s)")
            else:
                print(f"❌ static/{pasta}/ - NÃO ENCONTRADA")
    else:
        print("❌ Pasta static/ não encontrada")
    
    # Verificar pasta staticfiles
    staticfiles_path = Path('staticfiles')
    if staticfiles_path.exists():
        arquivos = list(staticfiles_path.rglob('*'))
        print(f"✅ staticfiles/ - {len(arquivos)} arquivo(s) coletados")
        
        # Verificar especificamente a imagem home2.jpg
        home_img = staticfiles_path / 'img' / 'home2.jpg'
        if home_img.exists():
            print("✅ staticfiles/img/home2.jpg - ENCONTRADA")
        else:
            print("❌ staticfiles/img/home2.jpg - NÃO ENCONTRADA")
    else:
        print("❌ Pasta staticfiles/ não encontrada")
        print("💡 Execute: python manage.py collectstatic")

def verificar_media():
    """Verifica pasta de media"""
    
    print("\n🖼️ Verificando pasta media...")
    
    media_path = Path('media')
    if media_path.exists():
        arquivos = list(media_path.rglob('*'))
        print(f"✅ media/ - {len(arquivos)} arquivo(s)")
        
        # Verificar pasta de artigos
        artigos_path = media_path / 'artigos'
        if artigos_path.exists():
            imagens = list(artigos_path.rglob('*.jpg')) + list(artigos_path.rglob('*.png'))
            print(f"✅ media/artigos/ - {len(imagens)} imagem(ns)")
        else:
            print("⚠️ media/artigos/ não encontrada")
    else:
        print("❌ Pasta media/ não encontrada")

def testar_views():
    """Testa as views do blog"""
    
    print("\n🧪 Testando views do blog...")
    
    try:
        from django.test import Client
        from django.urls import reverse
        
        client = Client()
        
        # Testar lista de artigos
        try:
            response = client.get('/blog/')
            if response.status_code == 200:
                print("✅ View lista_artigos - OK")
            else:
                print(f"❌ View lista_artigos - Status {response.status_code}")
        except Exception as e:
            print(f"❌ View lista_artigos - Erro: {e}")
        
        # Testar busca
        try:
            response = client.get('/blog/buscar/')
            if response.status_code == 200:
                print("✅ View buscar_artigos - OK")
            else:
                print(f"❌ View buscar_artigos - Status {response.status_code}")
        except Exception as e:
            print(f"❌ View buscar_artigos - Erro: {e}")
        
    except Exception as e:
        print(f"❌ Erro ao testar views: {e}")

def gerar_correcoes():
    """Gera script de correções"""
    
    print("\n🔧 COMANDOS DE CORREÇÃO:")
    print("=" * 50)
    
    print("\n1. Coletar arquivos estáticos:")
    print("python manage.py collectstatic --noinput")
    
    print("\n2. Verificar migrações:")
    print("python manage.py showmigrations")
    
    print("\n3. Executar migrações se necessário:")
    print("python manage.py migrate")
    
    print("\n4. Criar artigos de teste:")
    print("python popular_dados.py")
    
    print("\n5. Testar servidor:")
    print("python manage.py runserver")
    
    print("\n6. Para PythonAnywhere:")
    print("git pull origin master")
    print("python3.10 manage.py collectstatic --noinput --settings=setup.production_settings")
    print("python3.10 manage.py migrate --settings=setup.production_settings")

def main():
    print("🔍 DIAGNÓSTICO COMPLETO - BLOG E IMAGENS")
    print("=" * 50)
    
    if not configurar_django():
        return
    
    # Executar verificações
    artigos_ok = verificar_artigos()
    templates_ok = verificar_templates()
    verificar_arquivos_estaticos()
    verificar_media()
    
    if artigos_ok and templates_ok:
        testar_views()
    
    gerar_correcoes()
    
    print("\n" + "=" * 50)
    print("✅ DIAGNÓSTICO CONCLUÍDO")
    print("Execute os comandos de correção conforme necessário")

if __name__ == '__main__':
    main()
