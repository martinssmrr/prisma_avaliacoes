"""
Comando para testar e validar o sitemap
"""
from django.core.management.base import BaseCommand
from django.test import RequestFactory
from django.contrib.sites.models import Site
from seo.sitemaps import sitemaps


class Command(BaseCommand):
    help = 'Testa e valida URLs do sitemap'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--sitemap',
            type=str,
            default='all',
            help='Qual sitemap testar (static, artigos, seo, all)'
        )
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Testando Sitemaps'))
        
        factory = RequestFactory()
        request = factory.get('/')
        
        sitemap_name = options['sitemap']
        
        if sitemap_name == 'all':
            sitemaps_to_test = sitemaps.keys()
        else:
            sitemaps_to_test = [sitemap_name] if sitemap_name in sitemaps else []
        
        total_urls = 0
        total_errors = 0
        
        for name in sitemaps_to_test:
            self.stdout.write(f'\n📋 Testando sitemap: {name}')
            
            try:
                sitemap_class = sitemaps[name]
                sitemap = sitemap_class()
                
                items = sitemap.items()
                self.stdout.write(f'   Items encontrados: {len(items)}')
                
                valid_urls = []
                invalid_urls = []
                
                for item in items:
                    try:
                        location = sitemap.location(item)
                        if location and location != '/':
                            valid_urls.append(location)
                            self.stdout.write(f'   ✅ {location}')
                        else:
                            invalid_urls.append(f'Item: {item}, Location: {location}')
                            self.stdout.write(f'   ❌ URL inválida para item: {item}')
                            total_errors += 1
                    except Exception as e:
                        invalid_urls.append(f'Item: {item}, Erro: {str(e)}')
                        self.stdout.write(f'   ❌ Erro ao processar {item}: {str(e)}')
                        total_errors += 1
                
                total_urls += len(valid_urls)
                
                self.stdout.write(f'   URLs válidas: {len(valid_urls)}')
                self.stdout.write(f'   URLs inválidas: {len(invalid_urls)}')
                
                if invalid_urls:
                    self.stdout.write('   Problemas encontrados:')
                    for invalid in invalid_urls:
                        self.stdout.write(f'     - {invalid}')
                        
            except Exception as e:
                self.stdout.write(f'   ❌ Erro no sitemap {name}: {str(e)}')
                total_errors += 1
        
        self.stdout.write(f'\n📊 Resumo:')
        self.stdout.write(f'   Total de URLs válidas: {total_urls}')
        self.stdout.write(f'   Total de erros: {total_errors}')
        
        if total_errors == 0:
            self.stdout.write(self.style.SUCCESS('✅ Todos os sitemaps estão funcionando corretamente!'))
        else:
            self.stdout.write(self.style.ERROR(f'❌ {total_errors} problemas encontrados nos sitemaps'))
