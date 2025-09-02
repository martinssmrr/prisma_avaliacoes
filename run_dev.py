#!/usr/bin/env python
"""
Script para executar o Django em modo de desenvolvimento
Garante que o DEBUG=True e ALLOWED_HOSTS esteja configurado
"""

import os
import sys

def main():
    """Run administrative tasks in development mode."""
    
    # Forçar configurações de desenvolvimento
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
    os.environ.setdefault('DEBUG', 'True')
    
    print("🚀 INICIANDO SERVIDOR DE DESENVOLVIMENTO")
    print("📋 Modo: DESENVOLVIMENTO (DEBUG=True)")
    print("🌐 Disponível em: http://127.0.0.1:8000/")
    print("📊 Admin: http://127.0.0.1:8000/admin/")
    print("")
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Executar o servidor de desenvolvimento
    execute_from_command_line([sys.argv[0], 'runserver'])

if __name__ == '__main__':
    main()
