"""
WSGI config para PythonAnywhere

Este arquivo é usado pelo PythonAnywhere para servir sua aplicação Django.
Copie este conteúdo para o arquivo WSGI no painel do PythonAnywhere.
"""

import os
import sys

# Adicione o caminho do seu projeto
path = '/home/prismaav/prisma_avaliacoes'  # Caminho correto no PythonAnywhere
if path not in sys.path:
    sys.path.insert(0, path)

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.production_settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
