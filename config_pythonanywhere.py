#!/usr/bin/env python
"""
Script de configuração para PythonAnywhere
Execute este script no console do PythonAnywhere para verificar e corrigir configurações
"""

import os
import sys

def verificar_configuracao_pythonanywhere():
    """Verifica e ajusta configurações para PythonAnywhere"""
    
    print("🚀 Configuração PythonAnywhere - Prisma Avaliações")
    print("=" * 55)
    
    # Verificar se estamos no PythonAnywhere
    if 'pythonanywhere' in os.environ.get('USER', '').lower():
        print("✅ Executando no PythonAnywhere")
    else:
        print("⚠️  Não detectado PythonAnywhere - configuração local")
    
    # Verificar estrutura de diretórios
    current_dir = os.getcwd()
    print(f"📁 Diretório atual: {current_dir}")
    
    # Verificar arquivos essenciais
    arquivos_essenciais = [
        'manage.py',
        'setup/settings.py',
        'setup/production_settings.py',
        'wsgi_pythonanywhere.py',
        'requirements.txt',
        '.env'
    ]
    
    print("\n📋 Verificando arquivos essenciais:")
    for arquivo in arquivos_essenciais:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo} - NÃO ENCONTRADO")
    
    # Verificar variáveis de ambiente
    verificar_env()
    
    # Verificar dependências
    verificar_dependencias()
    
    print("\n" + "=" * 55)
    print("🔧 INSTRUÇÕES PARA PYTHONANYWHERE")
    print("=" * 55)
    
    print("\n1. 📝 Configure o arquivo WSGI:")
    print("   - Vá para a aba 'Web' no PythonAnywhere")
    print("   - Clique no link do arquivo WSGI")
    print("   - Substitua o conteúdo pelo arquivo 'wsgi_pythonanywhere.py'")
    
    print("\n2. 🔧 Configure diretórios estáticos:")
    print("   URL: /static/")
    print("   Directory: /home/prismaav/prisma_avaliacoes/staticfiles/")
    print("")
    print("   URL: /media/")
    print("   Directory: /home/prismaav/prisma_avaliacoes/media/")
    
    print("\n3. 🐍 Configure Virtual Environment:")
    print("   Virtualenv: /home/prismaav/.virtualenvs/prismaav.pythonanywhere.com/")
    
    print("\n4. 🔄 Reload da Web App:")
    print("   - Clique no botão verde 'Reload' na aba Web")
    
    print("\n5. 🌐 Teste o site:")
    print("   https://prismaav.pythonanywhere.com")

def verificar_env():
    """Verifica configurações do arquivo .env"""
    
    print("\n🔧 Verificando arquivo .env:")
    
    if not os.path.exists('.env'):
        print("❌ Arquivo .env não encontrado!")
        return
    
    with open('.env', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar variáveis importantes
    variaveis = {
        'SECRET_KEY': 'Chave secreta',
        'DEBUG': 'Modo debug',
        'ALLOWED_HOSTS': 'Hosts permitidos',
        'DB_ENGINE': 'Engine do banco'
    }
    
    for var, desc in variaveis.items():
        if f'{var}=' in content:
            # Extrair valor
            lines = content.split('\n')
            for line in lines:
                if line.startswith(f'{var}='):
                    value = line.split('=', 1)[1].strip()
                    if var == 'ALLOWED_HOSTS':
                        if 'prismaav.pythonanywhere.com' in value:
                            print(f"✅ {desc}: pythonanywhere.com configurado")
                        else:
                            print(f"⚠️  {desc}: verificar se contém prismaav.pythonanywhere.com")
                    elif var == 'SECRET_KEY':
                        print(f"✅ {desc}: {'*' * min(len(value), 20)}")
                    else:
                        print(f"✅ {desc}: {value}")
                    break
        else:
            print(f"❌ {desc}: não encontrado")

def verificar_dependencias():
    """Verifica se as dependências estão instaladas"""
    
    print("\n📦 Verificando dependências:")
    
    dependencias = [
        'django',
        'python-decouple',
        'Pillow'
    ]
    
    for dep in dependencias:
        try:
            __import__(dep.lower().replace('-', '_'))
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - NÃO INSTALADO")
            print(f"   Execute: pip install {dep}")

def gerar_comandos_deploy():
    """Gera comandos para deploy"""
    
    print("\n🚀 COMANDOS PARA DEPLOY NO PYTHONANYWHERE:")
    print("=" * 55)
    
    comandos = [
        "# 1. Instalar dependências",
        "pip install -r requirements.txt",
        "",
        "# 2. Executar migrações",
        "python manage.py migrate --settings=setup.production_settings",
        "",
        "# 3. Coletar arquivos estáticos", 
        "python manage.py collectstatic --noinput --settings=setup.production_settings",
        "",
        "# 4. Criar superusuário (se necessário)",
        "python manage.py criar_superuser_env --settings=setup.production_settings",
        "",
        "# 5. Popular dados de exemplo (opcional)",
        "python popular_dados.py",
        "",
        "# 6. Verificar configuração",
        "python manage.py check --settings=setup.production_settings --deploy"
    ]
    
    for comando in comandos:
        print(comando)
    
    print("\n" + "=" * 55)
    print("⚠️  IMPORTANTE: Após executar os comandos, faça RELOAD da Web App!")

def main():
    verificar_configuracao_pythonanywhere()
    gerar_comandos_deploy()

if __name__ == '__main__':
    main()
