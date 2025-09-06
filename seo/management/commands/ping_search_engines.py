"""
Management command para fazer ping do sitemap nos mecanismos de busca
"""
from django.core.management.base import BaseCommand
from django.conf import settings
import urllib.request
import urllib.parse
from seo.models import SEOConfig


class Command(BaseCommand):
    help = 'Faz ping do sitemap para Google e Bing'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--sitemap-url',
            type=str,
            help='URL específica do sitemap (opcional)',
        )
        parser.add_argument(
            '--google-only',
            action='store_true',
            help='Fazer ping apenas no Google',
        )
        parser.add_argument(
            '--bing-only',
            action='store_true',
            help='Fazer ping apenas no Bing',
        )
    
    def handle(self, *args, **options):
        config = SEOConfig.get_config()
        
        # URL do sitemap
        if options['sitemap_url']:
            sitemap_url = options['sitemap_url']
        else:
            sitemap_url = f"{config.get_full_domain()}/sitemap.xml"
        
        self.stdout.write(f'Fazendo ping do sitemap: {sitemap_url}')
        
        results = []
        
        # Google
        if not options['bing_only']:
            google_result = self.ping_google(sitemap_url)
            results.append(('Google', google_result))
        
        # Bing
        if not options['google_only']:
            bing_result = self.ping_bing(sitemap_url)
            results.append(('Bing', bing_result))
        
        # Resultados
        self.stdout.write('\n' + '='*50)
        self.stdout.write('RESULTADOS DO PING:')
        self.stdout.write('='*50)
        
        for engine, result in results:
            if result['success']:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ {engine}: {result["message"]}')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'✗ {engine}: {result["message"]}')
                )
        
        self.stdout.write('\n' + '='*50)
    
    def ping_google(self, sitemap_url):
        """Faz ping no Google"""
        try:
            encoded_url = urllib.parse.quote(sitemap_url, safe='')
            ping_url = f'https://www.google.com/ping?sitemap={encoded_url}'
            
            with urllib.request.urlopen(ping_url, timeout=30) as response:
                if response.getcode() == 200:
                    return {
                        'success': True,
                        'message': 'Ping enviado com sucesso!'
                    }
                else:
                    return {
                        'success': False,
                        'message': f'Resposta inesperada: {response.getcode()}'
                    }
        
        except urllib.error.HTTPError as e:
            return {
                'success': False,
                'message': f'Erro HTTP: {e.code} - {e.reason}'
            }
        except urllib.error.URLError as e:
            return {
                'success': False,
                'message': f'Erro de URL: {e.reason}'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro inesperado: {str(e)}'
            }
    
    def ping_bing(self, sitemap_url):
        """Faz ping no Bing"""
        try:
            encoded_url = urllib.parse.quote(sitemap_url, safe='')
            ping_url = f'https://www.bing.com/ping?sitemap={encoded_url}'
            
            with urllib.request.urlopen(ping_url, timeout=30) as response:
                if response.getcode() == 200:
                    return {
                        'success': True,
                        'message': 'Ping enviado com sucesso!'
                    }
                else:
                    return {
                        'success': False,
                        'message': f'Resposta inesperada: {response.getcode()}'
                    }
        
        except urllib.error.HTTPError as e:
            return {
                'success': False,
                'message': f'Erro HTTP: {e.code} - {e.reason}'
            }
        except urllib.error.URLError as e:
            return {
                'success': False,
                'message': f'Erro de URL: {e.reason}'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro inesperado: {str(e)}'
            }


# Uso do comando:
# python manage.py ping_search_engines
# python manage.py ping_search_engines --google-only
# python manage.py ping_search_engines --bing-only
# python manage.py ping_search_engines --sitemap-url="https://meusite.com/sitemap.xml"
