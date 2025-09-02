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
                'titulo': 'Consultoria para Proprietários e Compradores',
                'descricao': 'Orientação especializada para proprietários e compradores em decisões imobiliárias estratégicas.',
                'icone': 'fas fa-handshake'
            },
            {
                'titulo': 'Regularização Imobiliária',
                'descricao': 'Serviços completos para regularização de imóveis, documentação e adequação às normas vigentes.',
                'icone': 'fas fa-clipboard-check'
            },
            {
                'titulo': 'Consultoria Tributária Imobiliária',
                'descricao': 'Assessoria especializada em questões tributárias relacionadas ao mercado imobiliário.',
                'icone': 'fas fa-calculator'
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
            },
            {
                'nome': 'Ana Paula Santos',
                'cargo': 'Investidora',
                'texto': 'Serviço de consultoria excepcional! Me orientaram perfeitamente na compra do meu primeiro imóvel.',
                'estrelas': 5
            },
            {
                'nome': 'Carlos Eduardo Lima',
                'cargo': 'Corretor de Imóveis',
                'texto': 'Parceria de anos! Sempre entregam laudos de qualidade e no prazo acordado. Muito confiáveis.',
                'estrelas': 5
            },
            {
                'nome': 'Fernanda Oliveira',
                'cargo': 'Arquiteta',
                'texto': 'A regularização do meu projeto foi feita com excelência. Equipe muito competente e atenciosa.',
                'estrelas': 5
            },
            {
                'nome': 'Roberto Silva',
                'cargo': 'Contador',
                'texto': 'A consultoria tributária imobiliária me ajudou a economizar muito dinheiro. Serviço impecável!',
                'estrelas': 5
            },
            {
                'nome': 'Juliana Costa',
                'cargo': 'Empresária',
                'texto': 'Atendimento personalizado e laudo técnico muito detalhado. Superou minhas expectativas!',
                'estrelas': 5
            },
            {
                'nome': 'Pedro Henrique',
                'cargo': 'Engenheiro',
                'texto': 'Profissionais altamente qualificados. O trabalho de avaliação foi perfeito e muito bem fundamentado.',
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
