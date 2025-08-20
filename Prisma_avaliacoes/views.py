"""
Views para o app Prisma_avaliacoes
Gerencia as páginas da landing page
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    """
    View principal da landing page
    Exibe todas as seções: hero, serviços, depoimentos, contato
    """
    context = {
        'empresa': {
            'nome': 'Prisma Avaliações Imobiliárias',
            'slogan': 'Avaliações imobiliárias com precisão, agilidade e confiança',
            'descricao': 'Especialistas em avaliações de imóveis no Brasil com mais de 8 anos de experiência no mercado.',
            'whatsapp': '61998311920',
            'email': 'contato@prismaavaliacoes.com.br'
        },
        
        'servicos': [
            {
                'titulo': 'Laudos Técnicos Especializados',
                'descricao': 'Relatórios técnicos detalhados seguindo as normas da ABNT para todos os tipos de imóveis.',
                'icone': 'fas fa-file-alt'
            },
            {
                'titulo': 'Agilidade na Entrega',
                'descricao': 'Prazos otimizados sem comprometer a qualidade e precisão das avaliações.',
                'icone': 'fas fa-clock'
            },
            {
                'titulo': 'Confiabilidade Comprovada',
                'descricao': 'Profissionais certificados com vasta experiência no mercado imobiliário brasileiro.',
                'icone': 'fas fa-shield-alt'
            },
            {
                'titulo': 'Avaliação Completa',
                'descricao': 'Análise detalhada considerando localização, estado de conservação e tendências do mercado.',
                'icone': 'fas fa-home'
            }
        ],
        
        'depoimentos': [
            {
                'nome': 'Maria Jordana',
                'cargo': 'Proprietária',
                'texto': 'A Prisma me ajudou muito com avaliações precisas para meus clientes. Profissionalismo exemplar!',
                'estrelas': 5
            },
            {
                'nome': 'Augusto Martins',
                'cargo': 'Empresário',
                'texto': 'Excelente trabalho. O laudo foi entregue no prazo e com todas as informações que eu precisava.',
                'estrelas': 5
            },
            {
                'nome': 'Jorge Figueiredo',
                'cargo': 'Empresário',
                'texto': 'Recomendo a todos! Avaliação detalhada que me deu segurança para comprar o imóvel.',
                'estrelas': 5
            }
        ]
    }
    
    return render(request, 'Prisma_avaliacoes/home.html', context)

def contato(request):
    """
    View da página de contato (para futuras expansões)
    """
    context = {
        'titulo': 'Entre em Contato'
    }
    return render(request, 'Prisma_avaliacoes/contato.html', context)
