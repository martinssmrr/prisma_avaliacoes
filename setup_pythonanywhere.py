"""
Script de configuração automática para PythonAnywhere
Execute este script após clonar o repositório
"""

import os
import subprocess
import sys

def executar_comando(comando, descricao):
    """Executa um comando e mostra o resultado"""
    print(f"\n🔧 {descricao}...")
    try:
        result = subprocess.run(comando, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {descricao} - Sucesso!")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {descricao} - Erro!")
            if result.stderr:
                print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {descricao} - Exceção: {e}")
        return False

def verificar_arquivo(caminho, descricao):
    """Verifica se um arquivo existe"""
    if os.path.exists(caminho):
        print(f"✅ {descricao} - Encontrado")
        return True
    else:
        print(f"❌ {descricao} - Não encontrado")
        return False

def main():
    print("🚀 Configuração Automática - Prisma Avaliações")
    print("=" * 50)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('manage.py'):
        print("❌ Erro: Execute este script no diretório raiz do projeto Django")
        sys.exit(1)
    
    # Verificar arquivos necessários
    arquivos_necessarios = [
        ('manage.py', 'Django manage.py'),
        ('requirements.txt', 'Arquivo de dependências'),
        ('setup/production_settings.py', 'Configurações de produção'),
        ('wsgi_pythonanywhere.py', 'WSGI para PythonAnywhere'),
    ]
    
    print("\n📋 Verificando arquivos necessários...")
    todos_arquivos_ok = True
    for arquivo, desc in arquivos_necessarios:
        if not verificar_arquivo(arquivo, desc):
            todos_arquivos_ok = False
    
    if not todos_arquivos_ok:
        print("\n❌ Alguns arquivos estão faltando. Verifique o repositório.")
        sys.exit(1)
    
    # Verificar se o ambiente virtual está ativo
    if 'VIRTUAL_ENV' not in os.environ:
        print("\n⚠️  Aviso: Ambiente virtual não detectado.")
        print("Certifique-se de ativar o ambiente virtual antes de continuar:")
        print("source venv/bin/activate")
        resposta = input("Continuar mesmo assim? (y/N): ")
        if resposta.lower() != 'y':
            sys.exit(1)
    
    # Instalar dependências
    if not executar_comando('pip install --upgrade pip', 'Atualizando pip'):
        print("⚠️  Falha ao atualizar pip, continuando...")
    
    if not executar_comando('pip install -r requirements.txt', 'Instalando dependências'):
        print("❌ Falha ao instalar dependências")
        sys.exit(1)
    
    # Executar migrações
    if not executar_comando('python manage.py migrate --settings=setup.production_settings', 'Executando migrações'):
        print("❌ Falha ao executar migrações")
        sys.exit(1)
    
    # Coletar arquivos estáticos
    if not executar_comando('python manage.py collectstatic --noinput --settings=setup.production_settings', 'Coletando arquivos estáticos'):
        print("❌ Falha ao coletar arquivos estáticos")
        sys.exit(1)
    
    # Verificar se popular_dados.py existe e executar
    if os.path.exists('popular_dados.py'):
        resposta = input("\n📊 Deseja popular dados de exemplo? (Y/n): ")
        if resposta.lower() != 'n':
            executar_comando('python popular_dados.py', 'Populando dados de exemplo')
    
    print("\n" + "=" * 50)
    print("✅ Configuração concluída com sucesso!")
    print("\n🔧 Próximos passos:")
    print("1. Configure sua Web App no PythonAnywhere:")
    print("   - Vá para a aba 'Web'")
    print("   - Clique em 'Add a new web app'")
    print("   - Escolha 'Manual configuration' com Python 3.10")
    print("\n2. Configure o WSGI file:")
    print("   - Use o conteúdo de 'wsgi_pythonanywhere.py'")
    print("   - Substitua 'seuusername' pelo seu username real")
    print("\n3. Configure arquivos estáticos:")
    print("   - /static/ -> /home/seuusername/prisma_avaliacoes/staticfiles/")
    print("   - /media/ -> /home/seuusername/prisma_avaliacoes/media/")
    print("\n4. Configure o Virtual Environment:")
    print("   - /home/seuusername/prisma_avaliacoes/venv")
    print("\n5. Faça o Reload da Web App")
    print("\n🌐 Consulte DEPLOY_GUIDE.md para instruções detalhadas")

if __name__ == '__main__':
    main()
