#!/usr/bin/env python3
"""
Passenger WSGI file for HostGator cPanel deployment
Prisma Avaliações Imobiliárias - Production WSGI Configuration
"""

import sys
import os
from pathlib import Path

# Definir o diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent

# Adicionar o diretório do projeto ao Python path
sys.path.insert(0, str(BASE_DIR))

# Configurar a variável de ambiente para o Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings.production')

# Importar e configurar a aplicação WSGI do Django
try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except ImportError:
    # Fallback caso haja problemas de importação
    import traceback
    traceback.print_exc()
    
    # Criar uma aplicação WSGI simples para debug
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [b'Django import failed. Check your configuration.']

# Debug information (remover em produção final)
print(f"BASE_DIR: {BASE_DIR}")
print(f"Python Path: {sys.path[:3]}...")
print(f"Django Settings Module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
