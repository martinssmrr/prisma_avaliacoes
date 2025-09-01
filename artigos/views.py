"""
Views para o app de artigos/blog da Prisma Avaliações Imobiliárias
"""

import re
import math
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.utils.html import strip_tags
from .models import Artigo


def lista_artigos(request):
    """
    View para listagem de artigos publicados
    URL: /blog/
    """
    
    # Busca apenas artigos publicados
    artigos = Artigo.objects.filter(
        publicado=True,
        data_publicacao__lte=timezone.now()
    ).order_by('-data_publicacao')
    
    # Sistema de busca
    busca = request.GET.get('busca', '')
    if busca:
        artigos = artigos.filter(
            Q(titulo__icontains=busca) |
            Q(resumo__icontains=busca) |
            Q(conteudo__icontains=busca) |
            Q(tags__icontains=busca)
        )
    
    # Paginação
    paginator = Paginator(artigos, 6)  # 6 artigos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas para o template
    total_artigos = Artigo.objects.filter(publicado=True).count()
    
    context = {
        'page_obj': page_obj,
        'artigos': page_obj.object_list,
        'busca': busca,
        'total_artigos': total_artigos,
        'titulo_pagina': 'Blog - Prisma Avaliações Imobiliárias',
        'meta_description': 'Artigos sobre avaliações imobiliárias, mercado de imóveis e dicas profissionais da Prisma Avaliações.',
    }
    
    return render(request, 'artigos/lista_artigos.html', context)


def detalhe_artigo(request, slug):
    """
    View para exibição detalhada de um artigo
    URL: /blog/<slug>/
    Otimizada para SEO com meta tags dinâmicas e structured data
    """
    
    # Buscar o artigo
    artigo = get_object_or_404(
        Artigo,
        slug=slug,
        publicado=True,
        data_publicacao__lte=timezone.now()
    )
    
    # Processar conteúdo para SEO
    processed_content = process_article_content(artigo.conteudo)
    
    # Gerar sumário automático
    table_of_contents = generate_table_of_contents(artigo.conteudo)
    
    # Calcular tempo de leitura
    word_count = count_words(artigo.conteudo)
    reading_time = calculate_reading_time(word_count)
    
    # Meta tags SEO
    meta_description = artigo.meta_description or artigo.resumo[:160]
    meta_keywords = artigo.meta_keywords or generate_keywords_from_content(artigo)
    
    # URL canônica
    canonical_url = artigo.canonical_url or request.build_absolute_uri(artigo.get_absolute_url())
    
    # Título da página otimizado
    titulo_pagina = f"{artigo.titulo} | Blog Prisma Avaliações"
    
    # Buscar artigos relacionados (por tags)
    artigos_relacionados = get_related_articles(artigo)
    
    # Navegação entre artigos
    artigo_anterior = get_previous_article(artigo)
    proximo_artigo = get_next_article(artigo)
    
    # Tags processadas
    tags = artigo.get_tags_list()
    
    context = {
        'artigo': artigo,
        'processed_content': processed_content,
        'table_of_contents': table_of_contents,
        'word_count': word_count,
        'reading_time': reading_time,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
        'canonical_url': canonical_url,
        'titulo_pagina': titulo_pagina,
        'artigos_relacionados': artigos_relacionados,
        'artigo_anterior': artigo_anterior,
        'proximo_artigo': proximo_artigo,
        'tags': tags,
    }
    
    return render(request, 'artigos/detalhe_artigo_seo.html', context)


def process_article_content(content):
    """
    Processa o conteúdo do artigo para otimização SEO
    """
    # Adicionar IDs aos cabeçalhos para navegação
    content = re.sub(
        r'<h([2-4])>(.*?)</h[2-4]>',
        lambda m: f'<h{m.group(1)} id="heading-{hash(m.group(2)) % 10000}">{m.group(2)}</h{m.group(1)}>',
        content
    )
    
    # Adicionar loading lazy às imagens
    content = re.sub(
        r'<img([^>]*?)>',
        r'<img\1 loading="lazy">',
        content
    )
    
    # Adicionar alt text se não existir (versão corrigida)
    content = re.sub(
        r'<img([^>]*?)(?!.*alt=)([^>]*?)>',
        r'<img\1\2 alt="Imagem ilustrativa do artigo">',
        content
    )
    
    return content


def generate_table_of_contents(content):
    """
    Gera um sumário automático baseado nos cabeçalhos do conteúdo
    """
    # Extrair cabeçalhos H2, H3, H4
    headings = re.findall(r'<h([2-4]).*?>(.*?)</h[2-4]>', content, re.IGNORECASE)
    
    if not headings:
        return None
    
    toc_html = '<ul>'
    current_level = 2
    
    for level, text in headings:
        level = int(level)
        clean_text = strip_tags(text)
        anchor = f"heading-{hash(clean_text) % 10000}"
        
        if level > current_level:
            toc_html += '<ul>' * (level - current_level)
        elif level < current_level:
            toc_html += '</ul>' * (current_level - level)
        
        toc_html += f'<li><a href="#{anchor}">{clean_text}</a></li>'
        current_level = level
    
    # Fechar tags abertas
    toc_html += '</ul>' * (current_level - 1)
    
    return toc_html


def count_words(content):
    """
    Conta o número de palavras no conteúdo
    """
    # Remove HTML tags e conta palavras
    clean_text = strip_tags(content)
    words = clean_text.split()
    return len(words)


def calculate_reading_time(word_count):
    """
    Calcula o tempo estimado de leitura (assumindo 200 palavras por minuto)
    """
    words_per_minute = 200
    minutes = math.ceil(word_count / words_per_minute)
    return max(1, minutes)  # Mínimo de 1 minuto


def generate_keywords_from_content(artigo):
    """
    Gera palavras-chave automáticas a partir do conteúdo
    """
    if artigo.meta_keywords:
        return artigo.meta_keywords
    
    # Palavras-chave baseadas nas tags e título
    keywords = []
    
    if artigo.tags:
        keywords.extend(artigo.get_tags_list())
    
    # Adicionar palavras do título
    title_words = [word.lower() for word in artigo.titulo.split() if len(word) > 3]
    keywords.extend(title_words)
    
    # Palavras-chave padrão do negócio
    business_keywords = [
        'avaliação imobiliária', 'mercado imobiliário', 'prisma avaliações',
        'laudo técnico', 'avaliação de imóveis'
    ]
    keywords.extend(business_keywords)
    
    return ', '.join(keywords[:10])  # Máximo 10 palavras-chave


def get_related_articles(artigo, limit=3):
    """
    Busca artigos relacionados baseado nas tags
    """
    if not artigo.tags:
        # Se não há tags, buscar artigos recentes
        return Artigo.objects.filter(
            publicado=True,
            data_publicacao__lte=timezone.now()
        ).exclude(id=artigo.id).order_by('-data_publicacao')[:limit]
    
    # Buscar por tags similares
    tags = artigo.get_tags_list()
    related = Artigo.objects.filter(
        publicado=True,
        data_publicacao__lte=timezone.now()
    ).exclude(id=artigo.id)
    
    # Filtrar por tags
    for tag in tags:
        related = related.filter(tags__icontains=tag)
    
    related_articles = list(related[:limit])
    
    # Se não há artigos suficientes com tags similares, completar com artigos recentes
    if len(related_articles) < limit:
        recent = Artigo.objects.filter(
            publicado=True,
            data_publicacao__lte=timezone.now()
        ).exclude(
            id__in=[art.id for art in related_articles] + [artigo.id]
        ).order_by('-data_publicacao')[:limit - len(related_articles)]
        
        related_articles.extend(list(recent))
    
    return related_articles


def get_previous_article(artigo):
    """
    Busca o artigo anterior (mais antigo)
    """
    return Artigo.objects.filter(
        publicado=True,
        data_publicacao__lte=timezone.now(),
        data_publicacao__lt=artigo.data_publicacao
    ).order_by('-data_publicacao').first()


def get_next_article(artigo):
    """
    Busca o próximo artigo (mais recente)
    """
    return Artigo.objects.filter(
        publicado=True,
        data_publicacao__lte=timezone.now(),
        data_publicacao__gt=artigo.data_publicacao
    ).order_by('data_publicacao').first()


def artigos_por_tag(request, tag):
    """
    View para listagem de artigos por tag
    URL: /blog/tag/<tag>/
    """
    
    # Busca artigos que contenham a tag
    artigos = Artigo.objects.filter(
        publicado=True,
        data_publicacao__lte=timezone.now(),
        tags__icontains=tag
    ).order_by('-data_publicacao')
    
    # Paginação
    paginator = Paginator(artigos, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'artigos': page_obj.object_list,
        'tag': tag,
        'titulo_pagina': f'Artigos sobre {tag} - Blog Prisma Avaliações',
        'meta_description': f'Artigos sobre {tag} no blog da Prisma Avaliações Imobiliárias.',
    }
    
    return render(request, 'artigos/lista_artigos.html', context)


def buscar_artigos(request):
    """
    View para busca de artigos (AJAX ou GET)
    URL: /blog/buscar/
    """
    
    busca = request.GET.get('q', '').strip()
    artigos = []
    
    if busca and len(busca) >= 3:
        artigos = Artigo.objects.filter(
            publicado=True,
            data_publicacao__lte=timezone.now()
        ).filter(
            Q(titulo__icontains=busca) |
            Q(resumo__icontains=busca) |
            Q(tags__icontains=busca)
        ).order_by('-data_publicacao')[:10]
    
    context = {
        'artigos': artigos,
        'busca': busca,
        'titulo_pagina': f'Resultados para "{busca}" - Blog Prisma Avaliações',
    }
    
    return render(request, 'artigos/buscar_artigos.html', context)
