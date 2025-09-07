"""
Comando para corrigir problemas no sitemap
"""
from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import models
from seo.models import SEOConfig


class Command(BaseCommand):
    help = 'Corrige problemas comuns no sitemap'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔧 Corrigindo problemas do sitemap'))
        
        # 1. Verificar e corrigir artigos sem slug
        try:
            Artigo = apps.get_model('artigos', 'Artigo')
            
            # Artigos publicados sem slug
            artigos_sem_slug = Artigo.objects.filter(
                publicado=True
            ).filter(
                models.Q(slug__isnull=True) | models.Q(slug='')
            )
            
            if artigos_sem_slug.exists():
                self.stdout.write(f'⚠️ Encontrados {artigos_sem_slug.count()} artigos sem slug')
                
                for artigo in artigos_sem_slug:
                    # Gerar slug automaticamente
                    from django.utils.text import slugify
                    base_slug = slugify(artigo.titulo)
                    slug = base_slug
                    counter = 1
                    
                    # Garantir que o slug seja único
                    while Artigo.objects.filter(slug=slug).exists():
                        slug = f'{base_slug}-{counter}'
                        counter += 1
                    
                    artigo.slug = slug
                    artigo.save()
                    
                    self.stdout.write(f'   ✅ Slug criado para "{artigo.titulo}": {slug}')
            else:
                self.stdout.write('✅ Todos os artigos publicados têm slug válido')
                
        except Exception as e:
            self.stdout.write(f'❌ Erro ao verificar artigos: {str(e)}')
        
        # 2. Verificar configuração SEO
        try:
            config = SEOConfig.get_config()
            if not config:
                self.stdout.write('⚠️ Criando configuração SEO padrão...')
                SEOConfig.objects.create(
                    site_name='Prisma Avaliações Imobiliárias',
                    site_domain='prismaavaliacoes.com.br',
                    site_description='Avaliações imobiliárias profissionais em Minas Gerais',
                    default_keywords='avaliação imobiliária, perícia imobiliária, laudo de avaliação'
                )
                self.stdout.write('✅ Configuração SEO criada')
            else:
                # Verificar se o domínio está correto
                if 'localhost' in config.site_domain or '127.0.0.1' in config.site_domain:
                    self.stdout.write('⚠️ Corrigindo domínio em configuração SEO...')
                    config.site_domain = 'prismaavaliacoes.com.br'
                    config.save()
                    self.stdout.write('✅ Domínio corrigido')
                else:
                    self.stdout.write('✅ Configuração SEO está correta')
                    
        except Exception as e:
            self.stdout.write(f'❌ Erro ao verificar configuração SEO: {str(e)}')
        
        # 3. Limpar cache de sitemap
        try:
            from django.core.cache import cache
            cache.delete_many([
                'sitemaps_static',
                'sitemaps_artigos', 
                'sitemaps_seo'
            ])
            self.stdout.write('✅ Cache de sitemap limpo')
        except Exception as e:
            self.stdout.write(f'⚠️ Não foi possível limpar cache: {str(e)}')
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Correções do sitemap concluídas!'))
