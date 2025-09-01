#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from artigos.models import Artigo
from django.utils import timezone

def criar_artigo_seo_exemplo():
    print("Criando artigo de exemplo para SEO...")
    
    conteudo_artigo = """
    <h2>Introdução à Avaliação Imobiliária</h2>
    <p>A avaliação imobiliária é um processo técnico fundamental no mercado de imóveis, 
    realizada por profissionais especializados para determinar o valor de mercado de um bem.</p>
    
    <h3>O que é uma Avaliação Imobiliária?</h3>
    <p>Uma avaliação imobiliária consiste na análise técnica de um imóvel para determinar 
    seu valor justo de mercado, considerando diversos fatores como localização, 
    características construtivas, estado de conservação e condições do mercado local.</p>
    
    <h3>Métodos de Avaliação</h3>
    <p>Existem três métodos principais utilizados na avaliação de imóveis:</p>
    
    <h4>Método Comparativo Direto</h4>
    <p>Baseia-se na comparação com imóveis similares negociados recentemente na região.</p>
    
    <h4>Método da Renda</h4>
    <p>Considera o potencial de geração de renda do imóvel através de locação.</p>
    
    <h4>Método do Custo</h4>
    <p>Calcula o valor baseado no custo de reprodução da edificação.</p>
    
    <h2>Importância da Avaliação Profissional</h2>
    <p>A contratação de um avaliador qualificado é essencial para garantir 
    a precisão e confiabilidade do laudo de avaliação.</p>
    
    <h3>Quando Solicitar uma Avaliação</h3>
    <p>A avaliação imobiliária é recomendada em diversas situações:</p>
    <ul>
        <li>Compra e venda de imóveis</li>
        <li>Financiamentos bancários</li>
        <li>Partilha de bens</li>
        <li>Seguro habitacional</li>
        <li>Investimentos imobiliários</li>
    </ul>
    
    <h2>Conclusão</h2>
    <p>A avaliação imobiliária é um investimento que garante segurança e assertividade 
    nas transações imobiliárias, proporcionando bases sólidas para tomada de decisões.</p>
    """
    
    # Criar o artigo
    artigo, created = Artigo.objects.get_or_create(
        slug='guia-completo-avaliacao-imobiliaria-seo',
        defaults={
            'titulo': 'Guia Completo de Avaliação Imobiliária: Métodos, Importância e Quando Solicitar',
            'autor': 'Prisma Avaliações',
            'resumo': 'Descubra tudo sobre avaliação imobiliária: métodos utilizados, importância profissional e quando solicitar este serviço essencial para o mercado de imóveis.',
            'conteudo': conteudo_artigo,
            'meta_description': 'Guia completo sobre avaliação imobiliária: métodos, importância e quando solicitar. Saiba como escolher o melhor avaliador para seu imóvel.',
            'meta_keywords': 'avaliação imobiliária, laudo técnico, valor de mercado, avaliador imóvel, métodos avaliação, mercado imobiliário, Prisma Avaliações',
            'tags': 'avaliação, imóveis, mercado, laudo técnico, valor de mercado',
            'publicado': True,
            'data_publicacao': timezone.now(),
        }
    )
    
    if created:
        print(f"Artigo criado: {artigo.titulo}")
        print(f"Slug: {artigo.slug}")
        print(f"Meta description: {artigo.meta_description}")
        print(f"Meta keywords: {artigo.meta_keywords}")
        print(f"Tags: {artigo.tags}")
    else:
        print(f"Artigo já existe: {artigo.titulo}")
    
    print("\nArtigo de exemplo criado com sucesso!")
    print(f"URL: /blog/{artigo.slug}/")

if __name__ == '__main__':
    criar_artigo_seo_exemplo()
