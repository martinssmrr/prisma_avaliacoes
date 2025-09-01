#!/usr/bin/env python
"""
Script para verificar a implementação SEO dos artigos
Executa validações básicas de SEO on-page
"""

import os
import sys
import django
from bs4 import BeautifulSoup

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from artigos.models import Artigo
from django.test import Client
from django.urls import reverse

def verificar_seo_artigo(artigo):
    """
    Verifica elementos SEO de um artigo específico
    """
    print(f"\n🔍 Verificando SEO: {artigo.titulo}")
    print("=" * 60)
    
    # Usar Django test client
    client = Client()
    response = client.get(artigo.get_absolute_url())
    
    if response.status_code != 200:
        print(f"❌ Erro: Status {response.status_code}")
        return
    
    # Parse HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    seo_score = 0
    max_score = 15
    
    # 1. Verificar título H1
    h1 = soup.find('h1')
    if h1 and h1.get_text().strip():
        print("✅ H1 encontrado:", h1.get_text()[:50] + "...")
        seo_score += 1
    else:
        print("❌ H1 não encontrado ou vazio")
    
    # 2. Verificar meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        desc = meta_desc.get('content')
        print(f"✅ Meta description ({len(desc)} chars):", desc[:80] + "...")
        if 120 <= len(desc) <= 160:
            seo_score += 1
        else:
            print(f"⚠️  Meta description deveria ter 120-160 chars (atual: {len(desc)})")
    else:
        print("❌ Meta description não encontrada")
    
    # 3. Verificar meta keywords
    meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
    if meta_keywords and meta_keywords.get('content'):
        print("✅ Meta keywords:", meta_keywords.get('content')[:50] + "...")
        seo_score += 1
    else:
        print("❌ Meta keywords não encontradas")
    
    # 4. Verificar canonical URL
    canonical = soup.find('link', attrs={'rel': 'canonical'})
    if canonical and canonical.get('href'):
        print("✅ URL canônica:", canonical.get('href'))
        seo_score += 1
    else:
        print("❌ URL canônica não encontrada")
    
    # 5. Verificar Open Graph
    og_title = soup.find('meta', attrs={'property': 'og:title'})
    og_desc = soup.find('meta', attrs={'property': 'og:description'})
    og_image = soup.find('meta', attrs={'property': 'og:image'})
    
    og_count = 0
    if og_title:
        print("✅ OG Title:", og_title.get('content', '')[:50] + "...")
        og_count += 1
    if og_desc:
        print("✅ OG Description:", og_desc.get('content', '')[:50] + "...")
        og_count += 1
    if og_image:
        print("✅ OG Image:", og_image.get('content', '')[:50] + "...")
        og_count += 1
    
    if og_count >= 2:
        seo_score += 1
    
    # 6. Verificar Twitter Cards
    twitter_card = soup.find('meta', attrs={'name': 'twitter:card'})
    if twitter_card:
        print("✅ Twitter Card:", twitter_card.get('content'))
        seo_score += 1
    else:
        print("❌ Twitter Card não encontrada")
    
    # 7. Verificar JSON-LD Schema
    json_ld = soup.find('script', attrs={'type': 'application/ld+json'})
    if json_ld:
        print("✅ Schema.org JSON-LD encontrado")
        seo_score += 1
    else:
        print("❌ Schema.org JSON-LD não encontrado")
    
    # 8. Verificar estrutura de cabeçalhos
    headings = {
        'h1': len(soup.find_all('h1')),
        'h2': len(soup.find_all('h2')),
        'h3': len(soup.find_all('h3')),
        'h4': len(soup.find_all('h4')),
    }
    
    if headings['h1'] == 1:
        print("✅ Exatamente 1 H1 encontrado")
        seo_score += 1
    else:
        print(f"❌ Número incorreto de H1: {headings['h1']} (deveria ser 1)")
    
    if headings['h2'] >= 1:
        print(f"✅ {headings['h2']} cabeçalhos H2 encontrados")
        seo_score += 1
    else:
        print("⚠️  Nenhum H2 encontrado - considere adicionar subtítulos")
    
    # 9. Verificar imagens com alt
    images = soup.find_all('img')
    images_with_alt = [img for img in images if img.get('alt')]
    
    if images:
        alt_percentage = (len(images_with_alt) / len(images)) * 100
        print(f"📷 Imagens: {len(images)} total, {len(images_with_alt)} com alt ({alt_percentage:.1f}%)")
        if alt_percentage >= 90:
            seo_score += 1
    else:
        print("⚠️  Nenhuma imagem encontrada")
        seo_score += 1  # Não penalizar se não há imagens
    
    # 10. Verificar links internos
    internal_links = soup.find_all('a', href=True)
    blog_links = [link for link in internal_links if '/blog/' in link.get('href', '')]
    
    if len(blog_links) >= 2:
        print(f"✅ {len(blog_links)} links internos para blog encontrados")
        seo_score += 1
    else:
        print(f"⚠️  Poucos links internos: {len(blog_links)} (recomendado: 2+)")
    
    # 11. Verificar breadcrumbs
    breadcrumbs = soup.find('nav', attrs={'aria-label': 'Breadcrumb'})
    if breadcrumbs:
        print("✅ Breadcrumbs encontrados")
        seo_score += 1
    else:
        print("❌ Breadcrumbs não encontrados")
    
    # 12. Verificar tempo de leitura
    reading_time = soup.find(text=lambda text: text and 'min de leitura' in text)
    if reading_time:
        print("✅ Tempo de leitura exibido")
        seo_score += 1
    else:
        print("❌ Tempo de leitura não encontrado")
    
    # 13. Verificar botões de compartilhamento
    share_buttons = soup.find_all('a', href=lambda x: x and ('facebook.com' in x or 'twitter.com' in x or 'linkedin.com' in x))
    if len(share_buttons) >= 3:
        print(f"✅ {len(share_buttons)} botões de compartilhamento encontrados")
        seo_score += 1
    else:
        print(f"⚠️  Poucos botões de compartilhamento: {len(share_buttons)}")
    
    # 14. Verificar artigos relacionados
    related_section = soup.find(text=lambda text: text and 'Relacionados' in text)
    if related_section:
        print("✅ Seção de artigos relacionados encontrada")
        seo_score += 1
    else:
        print("❌ Artigos relacionados não encontrados")
    
    # 15. Verificar responsividade (meta viewport)
    viewport = soup.find('meta', attrs={'name': 'viewport'})
    if viewport:
        print("✅ Meta viewport configurado")
        seo_score += 1
    else:
        print("❌ Meta viewport não encontrado")
    
    # Resultado final
    percentage = (seo_score / max_score) * 100
    print(f"\n📊 SCORE SEO: {seo_score}/{max_score} ({percentage:.1f}%)")
    
    if percentage >= 90:
        print("🎉 EXCELENTE! SEO altamente otimizado")
    elif percentage >= 70:
        print("👍 BOM! SEO bem configurado com algumas melhorias possíveis")
    elif percentage >= 50:
        print("⚠️  REGULAR! Várias melhorias SEO necessárias")
    else:
        print("❌ CRÍTICO! SEO precisa de atenção urgente")
    
    return seo_score, max_score

def verificar_sitemap():
    """
    Verifica se o sitemap está funcionando
    """
    print("\n🗺️  Verificando Sitemap...")
    client = Client()
    
    try:
        response = client.get('/sitemap.xml')
        if response.status_code == 200:
            print("✅ Sitemap.xml acessível")
            # Parse XML
            soup = BeautifulSoup(response.content, 'xml')
            urls = soup.find_all('url')
            print(f"✅ {len(urls)} URLs no sitemap")
            return True
        else:
            print(f"❌ Erro no sitemap: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao acessar sitemap: {e}")
        return False

def verificar_robots():
    """
    Verifica robots.txt
    """
    print("\n🤖 Verificando Robots.txt...")
    client = Client()
    
    try:
        response = client.get('/robots.txt')
        if response.status_code == 200:
            print("✅ Robots.txt acessível")
            content = response.content.decode('utf-8')
            if 'Sitemap:' in content:
                print("✅ Sitemap referenciado no robots.txt")
                return True
            else:
                print("⚠️  Sitemap não referenciado no robots.txt")
                return False
        else:
            print(f"❌ Erro no robots.txt: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao acessar robots.txt: {e}")
        return False

def main():
    """
    Função principal para verificar SEO de todos os artigos
    """
    print("🚀 VERIFICAÇÃO SEO - PRISMA AVALIAÇÕES")
    print("=" * 60)
    
    # Verificar sitemap e robots
    sitemap_ok = verificar_sitemap()
    robots_ok = verificar_robots()
    
    # Buscar artigos publicados
    artigos = Artigo.objects.filter(publicado=True)[:5]  # Primeiros 5 artigos
    
    if not artigos:
        print("\n❌ Nenhum artigo publicado encontrado!")
        return
    
    total_score = 0
    total_max = 0
    
    # Verificar cada artigo
    for artigo in artigos:
        score, max_score = verificar_seo_artigo(artigo)
        total_score += score
        total_max += max_score
    
    # Resultado geral
    print("\n" + "=" * 60)
    print("📈 RELATÓRIO GERAL SEO")
    print("=" * 60)
    
    if artigos:
        avg_percentage = (total_score / total_max) * 100
        print(f"📊 Score médio: {total_score}/{total_max} ({avg_percentage:.1f}%)")
        print(f"📝 Artigos verificados: {len(artigos)}")
    
    print(f"🗺️  Sitemap: {'✅ OK' if sitemap_ok else '❌ ERRO'}")
    print(f"🤖 Robots.txt: {'✅ OK' if robots_ok else '❌ ERRO'}")
    
    print("\n✨ Verificação concluída!")
    print("\nPara melhorar o SEO:")
    print("1. Certifique-se de que meta descriptions tenham 120-160 caracteres")
    print("2. Use estrutura hierárquica de cabeçalhos (H1 > H2 > H3)")
    print("3. Adicione alt text em todas as imagens")
    print("4. Inclua links internos relevantes")
    print("5. Configure palavras-chave estratégicas")

if __name__ == '__main__':
    main()
