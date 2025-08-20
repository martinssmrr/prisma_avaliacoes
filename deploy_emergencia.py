#!/usr/bin/env python3
"""
Script de emergência para corrigir ALLOWED_HOSTS no PythonAnywhere
Execute: python deploy_emergencia.py
"""

import os
import subprocess
import sys
from pathlib import Path

def executar_comando(comando, descricao):
    """Executa um comando e mostra o resultado"""
    print(f"\n🔧 {descricao}...")
    try:
        result = subprocess.run(comando, shell=True, capture_output=True, text=True, cwd='/home/prismaav/prisma_avaliacoes')
        if result.returncode == 0:
            print(f"✅ {descricao} - Sucesso!")
            if result.stdout.strip():
                print(result.stdout.strip())
        else:
            print(f"⚠️ {descricao} - Aviso:")
            if result.stderr.strip():
                print(result.stderr.strip())
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {descricao} - Erro: {e}")
        return False

def criar_env_producao():
    """Cria arquivo .env para produção"""
    
    env_path = Path('/home/prismaav/prisma_avaliacoes/.env')
    
    if env_path.exists():
        print("📋 Arquivo .env já existe")
        # Verificar se contém ALLOWED_HOSTS correto
        with open(env_path, 'r') as f:
            content = f.read()
            if 'prismaav.pythonanywhere.com' in content:
                print("✅ ALLOWED_HOSTS já configurado no .env")
                return True
    
    print("📝 Criando arquivo .env de produção...")
    
    env_content = """# Configurações de produção PythonAnywhere
SECRET_KEY=django-insecure-(=-&$c%lq2!cxtmdwinj4uw&yftv$0*jsgn*)ew)%accjk@gk$
DEBUG=False
ALLOWED_HOSTS=prismaav.pythonanywhere.com,localhost,127.0.0.1
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DJANGO_SUPERUSER_USERNAME=prismaav
DJANGO_SUPERUSER_PASSWORD=PrismaAv4002@--
DJANGO_SUPERUSER_EMAIL=admin@prismaavaliacoes.com
"""
    
    try:
        with open(env_path, 'w') as f:
            f.write(env_content)
        print("✅ Arquivo .env criado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar .env: {e}")
        return False

def verificar_configuracao():
    """Verifica se a configuração está correta"""
    
    print("\n🧪 Testando configuração Django...")
    
    try:
        # Mudar para diretório do projeto
        os.chdir('/home/prismaav/prisma_avaliacoes')
        
        # Configurar Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.production_settings')
        
        import django
        django.setup()
        
        from django.conf import settings
        
        print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"✅ DEBUG: {settings.DEBUG}")
        
        if 'prismaav.pythonanywhere.com' in settings.ALLOWED_HOSTS:
            print("✅ Configuração CORRETA!")
            return True
        else:
            print("❌ prismaav.pythonanywhere.com não está em ALLOWED_HOSTS")
            return False
            
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")
        return False

def main():
    print("🚨 SCRIPT DE EMERGÊNCIA - PYTHONANYWHERE")
    print("=" * 50)
    print("Corrigindo erro: Host não permitido")
    print("")
    
    # Verificar se estamos no PythonAnywhere
    if not os.path.exists('/home/prismaav'):
        print("❌ Este script deve ser executado no PythonAnywhere!")
        sys.exit(1)
    
    # Mudar para diretório do projeto
    try:
        os.chdir('/home/prismaav/prisma_avaliacoes')
        print(f"📁 Diretório: {os.getcwd()}")
    except FileNotFoundError:
        print("❌ Diretório do projeto não encontrado!")
        print("💡 Execute: git clone https://github.com/martinssmrr/prisma_avaliacoes.git")
        sys.exit(1)
    
    # Passo 1: Atualizar código
    executar_comando('git pull origin master', 'Atualizando código do repositório')
    
    # Passo 2: Criar .env se necessário
    criar_env_producao()
    
    # Passo 3: Instalar dependências
    executar_comando('pip3.10 install --user -r requirements.txt', 'Instalando dependências')
    
    # Passo 4: Executar migrações
    executar_comando('python3.10 manage.py migrate --settings=setup.production_settings', 'Executando migrações')
    
    # Passo 5: Coletar arquivos estáticos
    print("📸 Coletando arquivos estáticos (incluindo imagens)...")
    executar_comando('python3.10 manage.py collectstatic --noinput --settings=setup.production_settings', 'Coletando arquivos estáticos')
    
    # Verificar se imagens foram coletadas
    print("🖼️ Verificando imagens coletadas...")
    static_img_path = Path('/home/prismaav/prisma_avaliacoes/staticfiles/img')
    if static_img_path.exists():
        print("✅ Pasta de imagens criada em staticfiles")
        img_files = list(static_img_path.glob('*.jpg'))
        if img_files:
            print(f"✅ {len(img_files)} imagem(ns) encontrada(s)")
        else:
            print("⚠️ Nenhuma imagem encontrada")
    else:
        print("⚠️ Pasta staticfiles/img não encontrada")
    
    # Passo 6: Verificar configuração
    if verificar_configuracao():
        print("\n" + "=" * 50)
        print("✅ CORREÇÃO APLICADA COM SUCESSO!")
        print("=" * 50)
        print("\n🔄 PRÓXIMO PASSO OBRIGATÓRIO:")
        print("1. Vá para a aba 'Web' no PythonAnywhere")
        print("2. Clique em 'Reload prismaav.pythonanywhere.com'")
        print("3. Aguarde 30 segundos")
        print("4. Teste: https://prismaav.pythonanywhere.com")
        print("\n✅ O erro de ALLOWED_HOSTS deve estar resolvido!")
    else:
        print("\n❌ Ainda há problemas na configuração")
        print("💡 Verifique o Error log na aba Web do PythonAnywhere")

if __name__ == '__main__':
    main()
