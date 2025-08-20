"""
Views para o app de artigos/blog da Prisma Avaliações Imobiliárias
"""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
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
    View para exibição individual do artigo
    URL: /blog/<slug>/
    """
    
    # Busca o artigo pelo slug
    artigo = get_object_or_404(
        Artigo,
        slug=slug,
        publicado=True,
        data_publicacao__lte=timezone.now()
    )
    
    # Artigos relacionados (mesmas tags ou autor)
    artigos_relacionados = Artigo.objects.filter(
        publicado=True,
        data_publicacao__lte=timezone.now()
    ).exclude(id=artigo.id)
    
    # Filtra por tags similares se existirem
    if artigo.tags:
        tags_artigo = artigo.get_tags_list()
        for tag in tags_artigo:
            artigos_relacionados = artigos_relacionados.filter(
                tags__icontains=tag
            )
        
        # Se não encontrou por tags, busca por autor
        if not artigos_relacionados.exists():
            artigos_relacionados = Artigo.objects.filter(
                publicado=True,
                data_publicacao__lte=timezone.now(),
                autor=artigo.autor
            ).exclude(id=artigo.id)
    
    # Limita a 3 artigos relacionados
    artigos_relacionados = artigos_relacionados[:3]
    
    # Artigo anterior e próximo
    artigo_anterior = Artigo.objects.filter(
        publicado=True,
        data_publicacao__lt=artigo.data_publicacao
    ).first()
    
    proximo_artigo = Artigo.objects.filter(
        publicado=True,
        data_publicacao__gt=artigo.data_publicacao
    ).last()
    
    context = {
        'artigo': artigo,
        'artigos_relacionados': artigos_relacionados,
        'artigo_anterior': artigo_anterior,
        'proximo_artigo': proximo_artigo,
        'titulo_pagina': f'{artigo.titulo} - Blog Prisma Avaliações',
        'meta_description': artigo.meta_description or artigo.resumo[:160],
        'tags': artigo.get_tags_list(),
    }
    
    return render(request, 'artigos/detalhe_artigo.html', context)


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
