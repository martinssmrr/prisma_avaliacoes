#!/usr/bin/env python
"""
Script para popular o banco de dados com dados de exemplo
"""

import os
import sys
import django
from datetime import datetime

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.contrib.auth.models import User
from artigos.models import Categoria, Artigo

def criar_dados_exemplo():
    """Cria dados de exemplo para testar o sistema"""
    
    print("🔧 Criando dados de exemplo...")
    
    # Criar superusuário se não existir
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@prisma.com',
            password='admin123'
        )
        print("✓ Superusuário criado: admin/admin123")
    else:
        admin = User.objects.get(username='admin')
        print("✓ Superusuário já existe")
    
    # Criar categorias
    categorias_data = [
        {
            'nome': 'Avaliação Imobiliária',
            'slug': 'avaliacao-imobiliaria',
            'descricao': 'Artigos sobre métodos e técnicas de avaliação de imóveis'
        },
        {
            'nome': 'Mercado Imobiliário',
            'slug': 'mercado-imobiliario',
            'descricao': 'Análises e tendências do mercado imobiliário'
        },
        {
            'nome': 'Legislação',
            'slug': 'legislacao',
            'descricao': 'Normas e regulamentações do setor imobiliário'
        },
        {
            'nome': 'Dicas e Orientações',
            'slug': 'dicas-orientacoes',
            'descricao': 'Dicas práticas para proprietários e investidores'
        }
    ]
    
    categorias_criadas = []
    for cat_data in categorias_data:
        categoria, criada = Categoria.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        categorias_criadas.append(categoria)
        if criada:
            print(f"✓ Categoria criada: {categoria.nome}")
        else:
            print(f"• Categoria já existe: {categoria.nome}")
    
    # Criar artigos
    artigos_data = [
        {
            'titulo': 'Como funciona a avaliação de imóveis residenciais',
            'slug': 'como-funciona-avaliacao-imoveis-residenciais',
            'resumo': 'Entenda os métodos e critérios utilizados na avaliação de imóveis residenciais para diferentes finalidades.',
            'conteudo': '''
            <h2>Introdução</h2>
            <p>A avaliação de imóveis residenciais é um processo técnico que determina o valor de mercado de uma propriedade em uma data específica. Este procedimento é fundamental para diversas situações como compra, venda, financiamento, seguros e questões jurídicas.</p>
            
            <h2>Métodos de Avaliação</h2>
            <h3>1. Método Comparativo de Dados de Mercado</h3>
            <p>É o método mais utilizado para imóveis residenciais. Baseia-se na comparação com imóveis similares que foram vendidos recentemente na região.</p>
            
            <h3>2. Método da Renda</h3>
            <p>Utilizado principalmente para imóveis de investimento, considera a capacidade de geração de renda do imóvel.</p>
            
            <h3>3. Método do Custo</h3>
            <p>Considera o custo de construção atual do imóvel, descontando a depreciação.</p>
            
            <h2>Fatores Considerados</h2>
            <ul>
                <li>Localização e bairro</li>
                <li>Área construída e terreno</li>
                <li>Estado de conservação</li>
                <li>Idade da construção</li>
                <li>Infraestrutura do entorno</li>
                <li>Padrão de acabamento</li>
            </ul>
            
            <h2>Conclusão</h2>
            <p>Uma avaliação imobiliária precisa é essencial para tomadas de decisão informadas no mercado imobiliário. Sempre procure profissionais qualificados e credenciados.</p>
            ''',
            'meta_description': 'Aprenda como funciona a avaliação de imóveis residenciais, métodos utilizados e fatores considerados pelos avaliadores.',
            'tags': 'avaliação, imóveis, residencial, valor de mercado',
            'publicado': True
        },
        {
            'titulo': 'Tendências do mercado imobiliário em 2025',
            'slug': 'tendencias-mercado-imobiliario-2025',
            'resumo': 'Análise das principais tendências que estão moldando o mercado imobiliário brasileiro em 2025.',
            'conteudo': '''
            <h2>O Mercado em Transformação</h2>
            <p>O ano de 2025 trouxe mudanças significativas para o mercado imobiliário brasileiro. A digitalização, sustentabilidade e novas formas de trabalho estão redefinindo as preferências dos consumidores.</p>
            
            <h2>Principais Tendências</h2>
            <h3>1. Home Office Permanente</h3>
            <p>A consolidação do trabalho remoto aumentou a demanda por imóveis com home office bem estruturado.</p>
            
            <h3>2. Sustentabilidade</h3>
            <p>Imóveis com certificações ambientais e eficiência energética têm maior valorização.</p>
            
            <h3>3. Tecnologia Integrada</h3>
            <p>Casas inteligentes com automação residencial se tornaram mais acessíveis e desejadas.</p>
            
            <h3>4. Migração para Cidades Menores</h3>
            <p>A flexibilidade do trabalho remoto impulsionou a busca por qualidade de vida em cidades menores.</p>
            
            <h2>Impactos nos Preços</h2>
            <p>Essas tendências têm impacto direto na valorização dos imóveis, criando novas oportunidades de investimento.</p>
            ''',
            'meta_description': 'Descubra as principais tendências do mercado imobiliário em 2025 e como elas afetam preços e oportunidades.',
            'tags': 'mercado imobiliário, tendências, 2025, investimento',
            'publicado': True
        },
        {
            'titulo': 'NBR 14653: Norma brasileira de avaliação de bens',
            'slug': 'nbr-14653-norma-brasileira-avaliacao-bens',
            'resumo': 'Conheça a norma técnica que regulamenta as atividades de avaliação de bens no Brasil.',
            'conteudo': '''
            <h2>O que é a NBR 14653</h2>
            <p>A NBR 14653 é a norma técnica brasileira que estabelece os procedimentos gerais para avaliação de bens, direitos e empreendimentos. É composta por 7 partes, sendo a parte 2 específica para imóveis urbanos.</p>
            
            <h2>Estrutura da Norma</h2>
            <ul>
                <li>Parte 1: Procedimentos gerais</li>
                <li>Parte 2: Imóveis urbanos</li>
                <li>Parte 3: Imóveis rurais</li>
                <li>Parte 4: Empreendimentos</li>
                <li>Parte 5: Máquinas, equipamentos, instalações e bens industriais em geral</li>
                <li>Parte 6: Recursos naturais e ambientais</li>
                <li>Parte 7: Patrimônios históricos</li>
            </ul>
            
            <h2>Importância para Avaliadores</h2>
            <p>O cumprimento da NBR 14653 é obrigatório para avaliadores e garante a qualidade técnica e a padronização dos laudos de avaliação.</p>
            
            <h2>Graus de Precisão</h2>
            <p>A norma estabelece três graus de precisão (I, II e III) baseados na finalidade da avaliação e nos dados disponíveis.</p>
            ''',
            'meta_description': 'Entenda a NBR 14653, norma brasileira que regulamenta a avaliação de bens e sua importância para o setor.',
            'tags': 'NBR 14653, norma técnica, avaliação, legislação',
            'publicado': True
        },
        {
            'titulo': '5 dicas para valorizar seu imóvel antes da venda',
            'slug': '5-dicas-valorizar-imovel-antes-venda',
            'resumo': 'Dicas práticas e econômicas para aumentar o valor do seu imóvel na hora da venda.',
            'conteudo': '''
            <h2>Preparando seu Imóvel para a Venda</h2>
            <p>Pequenos investimentos podem resultar em significativo aumento no valor de venda do seu imóvel. Confira nossas dicas profissionais.</p>
            
            <h2>1. Pintura Geral</h2>
            <p>Uma pintura nova em cores neutras pode valorizar o imóvel em até 5%. Invista em cores claras e modernas.</p>
            
            <h2>2. Reforma do Banheiro</h2>
            <p>Banheiros atualizados são grandes atrativos. Troque metais, louças antigas e invista em um bom rejunte.</p>
            
            <h2>3. Melhore a Iluminação</h2>
            <p>Troque lâmpadas por LED e adicione pontos de luz. Ambientes bem iluminados parecem maiores e mais acolhedores.</p>
            
            <h2>4. Organize e Desapegue</h2>
            <p>Retire móveis em excesso e objetos pessoais. Isso ajuda os compradores a visualizarem o espaço.</p>
            
            <h2>5. Cuide do Paisagismo</h2>
            <p>A primeira impressão é fundamental. Mantenha jardins bem cuidados e a fachada limpa.</p>
            
            <h2>Retorno do Investimento</h2>
            <p>Essas melhorias podem aumentar o valor de venda entre 8% a 15%, com investimento relativamente baixo.</p>
            ''',
            'meta_description': 'Confira 5 dicas práticas para valorizar seu imóvel antes da venda e aumentar o preço de mercado.',
            'tags': 'valorização, venda de imóvel, dicas, reforma',
            'publicado': True
        },
        {
            'titulo': 'Como escolher um avaliador imobiliário qualificado',
            'slug': 'como-escolher-avaliador-imobiliario-qualificado',
            'resumo': 'Critérios importantes para escolher um profissional competente para avaliar seu imóvel.',
            'conteudo': '''
            <h2>A Importância da Escolha Certa</h2>
            <p>A escolha de um avaliador qualificado é fundamental para obter um laudo preciso e confiável. Um erro na avaliação pode custar caro em negociações.</p>
            
            <h2>Critérios de Seleção</h2>
            <h3>1. Formação e Credenciamento</h3>
            <p>Verifique se o profissional possui registro no CREA ou IBAPE e formação em Engenharia, Arquitetura ou áreas afins.</p>
            
            <h3>2. Experiência na Região</h3>
            <p>Dê preferência a profissionais que conhecem bem a região do imóvel a ser avaliado.</p>
            
            <h3>3. Especialização</h3>
            <p>Para imóveis específicos (industriais, rurais, históricos), procure especialistas na área.</p>
            
            <h3>4. Referências</h3>
            <p>Solicite referências de trabalhos anteriores e verifique a reputação do profissional.</p>
            
            <h2>Documentos Necessários</h2>
            <ul>
                <li>Certidões do imóvel</li>
                <li>Plantas e projetos</li>
                <li>Comprovantes de IPTU</li>
                <li>Fotos atuais</li>
            </ul>
            
            <h2>Conclusão</h2>
            <p>Investir na escolha de um bom avaliador é investir na segurança da sua transação imobiliária.</p>
            ''',
            'meta_description': 'Saiba como escolher um avaliador imobiliário qualificado e os critérios importantes para essa decisão.',
            'tags': 'avaliador, qualificação, escolha, profissional',
            'publicado': False  # Este ficará como rascunho para teste
        }
    ]
    
    for artigo_data in artigos_data:
        artigo, criado = Artigo.objects.get_or_create(
            slug=artigo_data['slug'],
            defaults={
                **artigo_data,
                'autor': 'Equipe Prisma Avaliações',  # Nome fixo para todos os artigos
                'data_publicacao': datetime.now() if artigo_data['publicado'] else None
            }
        )
        if criado:
            status = "publicado" if artigo_data['publicado'] else "rascunho"
            print(f"✓ Artigo criado ({status}): {artigo.titulo}")
        else:
            print(f"• Artigo já existe: {artigo.titulo}")
    
    print("\n🎉 Dados de exemplo criados com sucesso!")
    print("\n📋 Resumo:")
    print(f"• Categorias: {Categoria.objects.count()}")
    print(f"• Artigos publicados: {Artigo.objects.filter(publicado=True).count()}")
    print(f"• Artigos em rascunho: {Artigo.objects.filter(publicado=False).count()}")
    print(f"• Total de artigos: {Artigo.objects.count()}")
    
    print("\n🔐 Login do admin:")
    print("Usuário: admin")
    print("Senha: admin123")
    print("URL: http://127.0.0.1:8001/admin")

if __name__ == '__main__':
    criar_dados_exemplo()
