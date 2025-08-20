# Prisma Avaliações Imobiliárias - Site Django Completo

Site profissional para a empresa **Prisma Avaliações Imobiliárias**, desenvolvido em Django com sistema de blog integrado e painel administrativo completo.

## 🚀 Funcionalidades Implementadas

### 🏠 Landing Page Principal
- **Design Responsivo**: Layout moderno com Bootstrap 5.3.0
- **Hero Section**: Imagem de fundo profissional com call-to-action
- **Seções Informativas**:
  - Sobre a Empresa
  - Serviços Oferecidos
  - Por que Escolher a Prisma
  - Depoimentos de Clientes
- **Integração WhatsApp**: Botão direto para contato com mensagem pré-formatada
- **SEO Otimizado**: Meta tags e estrutura semântica

### 📝 Sistema de Blog (Artigos)
- **Modelo de Dados Completo**:
  - Artigos com título, slug, resumo, conteúdo HTML
  - Sistema de publicação (publicado/rascunho)
  - **Campo Autor Flexível**: Nome livre, sem necessidade de usuário do sistema
  - Meta description para SEO
  - Tags para organização
  - Imagens destacadas
  - Controle de datas (criação, atualização, publicação)
  
- **Views Funcionais**:
  - Lista de artigos publicados
  - Visualização individual de artigos
  - Sistema de busca por título e conteúdo
  - Paginação automática

- **Templates Responsivos**:
  - Design moderno e profissional
  - Navegação intuitiva
  - Breadcrumbs
  - Compartilhamento social
  - Layout otimizado para dispositivos móveis

### 🔧 Django Admin Personalizado
- **Interface Customizada**:
  - Header personalizado "Prisma Avaliações - Administração"
  - Configuração específica para gerenciamento de artigos
  - Ações em lote (publicar/despublicar)
  - Filtros avançados
  - Busca inteligente
  
- **Funcionalidades Admin**:
  - Preenchimento automático de slug
  - Status visual de publicação
  - Link direto para visualizar artigo no site
  - Organização por data de criação
  - Campos de somente leitura para auditoria

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 5.2.5
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5.3.0
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Bibliotecas Python**:
  - Pillow (processamento de imagens)
  - Django built-in apps
- **Recursos Externos**:
  - Font Awesome 6.4.0 (ícones)
  - Google Fonts (tipografia)
  - WhatsApp API (integração de contato)

## 📊 Dados de Exemplo Criados

### Artigos Publicados (4):
1. **"Como funciona a avaliação de imóveis residenciais"**
2. **"Tendências do mercado imobiliário em 2025"**
3. **"NBR 14653: Norma brasileira de avaliação de bens"**
4. **"5 dicas para valorizar seu imóvel antes da venda"**

### Categorias (4):
- Avaliação Imobiliária
- Mercado Imobiliário  
- Legislação
- Dicas e Orientações

## � Flexibilidade do Campo Autor

O sistema foi projetado para máxima flexibilidade no gerenciamento de autores:

### ✅ **Vantagens do Sistema Atual**
- **Campo de Texto Livre**: Qualquer nome pode ser usado como autor
- **Sem Dependência de Usuários**: Não é necessário criar contas no sistema
- **Títulos e Credenciais**: Pode incluir informações como "Dr.", "Eng.", CREA, etc.
- **Edição Simples**: Alteração direta no Django Admin
- **Flexibilidade Total**: Autores externos, convidados, ou equipes

### 💡 **Exemplos de Uso**
```
• "Dr. João Silva - Engenheiro Civil CREA 12345"
• "Equipe Prisma Avaliações"
• "Prof. Maria Santos - Especialista em Avaliações"
• "Eng. Carlos Oliveira - Consultor Imobiliário"
• "Redação Prisma"
```

### 🔧 **Funcionalidades Admin**
- Preenchimento automático com nome do usuário logado
- Edição livre do campo autor
- Histórico de autores utilizados
- Sem restrições de formato

## �🔐 Acesso Administrativo

**Credenciais do Admin:**
- **Usuário**: admin
- **Senha**: admin123
- **URL**: http://127.0.0.1:8001/admin

## 🌐 URLs Principais

### Site Principal
- **Home**: `http://127.0.0.1:8001/`
- **Sobre**: `http://127.0.0.1:8001/sobre/`
- **Serviços**: `http://127.0.0.1:8001/servicos/`
- **Contato**: `http://127.0.0.1:8001/contato/`

### Blog/Artigos
- **Lista de Artigos**: `http://127.0.0.1:8001/artigos/`
- **Busca**: `http://127.0.0.1:8001/artigos/buscar/?q=termo`
- **Artigo Individual**: `http://127.0.0.1:8001/artigos/slug-do-artigo/`

### Administração
- **Django Admin**: `http://127.0.0.1:8001/admin/`

## 🚀 Como Executar

1. **Ativar ambiente virtual**:
   ```bash
   .\venv\Scripts\Activate.ps1
   ```

2. **Instalar dependências**:
   ```bash
   pip install Django Pillow
   ```

3. **Executar migrações**:
   ```bash
   python manage.py migrate
   ```

4. **Popular com dados de exemplo**:
   ```bash
   python popular_dados.py
   ```

5. **Iniciar servidor**:
   ```bash
   python manage.py runserver 8001
   ```

## 🏗️ Estrutura do Projeto

```
Prisma Avaliações Imobiliarias/
├── manage.py
├── db.sqlite3
├── README.md
├── requirements.txt
├── .gitignore
├── venv/                           # Ambiente virtual Python
├── setup/                          # Configurações do Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── Prisma_avaliacoes/             # App principal
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
├── templates/                      # Templates HTML
│   ├── base.html
│   └── Prisma_avaliacoes/
│       ├── home.html
│       └── contato.html
├── static/                        # Arquivos estáticos
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── media/                         # Arquivos de mídia
    ├── home.jpg
    └── home2.jpg
```

## 🚀 Funcionalidades

### ✨ Landing Page Completa
- **Seção Hero**: Apresentação da empresa com call-to-action
- **Serviços**: Cards destacando benefícios da empresa
- **Depoimentos**: Testimoniais de clientes satisfeitos
- **Formulário de Contato**: Integração direta com WhatsApp
- **Rodapé Informativo**: Links, contatos e informações da empresa

### 📱 Design Responsivo
- Layout totalmente responsivo com Bootstrap 5
- Otimizado para mobile, tablet e desktop
- Cores elegantes (tons de azul, cinza e branco)
- Tipografia moderna (Inter Font)
- Animações suaves e interativas

### 🎯 Integração WhatsApp
- Botões de contato direto via WhatsApp
- Formulário que gera mensagem estruturada
- Número configurado: (77) 99951-5837

### ⚡ Performance e UX
- Carregamento rápido
- Animações de entrada
- Scroll suave entre seções
- Validação de formulários
- Máscaras para campos de telefone

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.12 + Django 5.2.5
- **Frontend**: HTML5, CSS3, JavaScript ES6
- **Framework CSS**: Bootstrap 5.3.0
- **Ícones**: Font Awesome 6.4.0
- **Tipografia**: Google Fonts (Inter)
- **Banco de Dados**: SQLite (desenvolvimento)

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 🔧 Instalação e Configuração

### 1. Clone o repositório
```bash
cd "Prisma Avaliações Imobiliarias"
```

### 2. Ative o ambiente virtual
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install Django>=4.2.0
```

### 4. Execute as migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crie um superusuário (opcional)
```bash
python manage.py createsuperuser
```

### 6. Inicie o servidor de desenvolvimento
```bash
python manage.py runserver
```

### 7. Acesse no navegador
```
http://127.0.0.1:8000/
```

## �‍💼 Django Admin

O projeto inclui um painel administrativo para gerenciar o conteúdo:

### Acesso ao Admin
- **URL**: `http://127.0.0.1:8000/admin/`
- **Usuário criado**: `prismaav`
- **Email**: `admin@prismaavaliacoes.com.br`

### Funcionalidades do Admin
- Gerenciar usuários do sistema
- Visualizar logs de acesso
- Configurações avançadas do Django
- Futuras expansões (blog, depoimentos, etc.)

## �📄 Páginas Disponíveis

| URL | Descrição |
|-----|-----------|
| `/` | Página inicial (landing page completa) |
| `/contato/` | Página dedicada ao contato (formulário expandido) |
| `/admin/` | Painel administrativo do Django |

## 🎨 Personalização

### Cores do Projeto
```css
:root {
    --primary-color: #1e40af;     /* Azul principal */
    --secondary-color: #0f172a;   /* Azul escuro */
    --accent-color: #3b82f6;      /* Azul claro */
    --text-color: #374151;        /* Cinza texto */
    --light-bg: #f8fafc;          /* Fundo claro */
}
```

### Contatos da Empresa
Para alterar os dados de contato, edite o arquivo `Prisma_avaliacoes/views.py`:

```python
'empresa': {
    'nome': 'Prisma Avaliações Imobiliárias',
    'slogan': 'Avaliações imobiliárias com precisão e confiança',
    'whatsapp': '77999515837',  # Altere aqui
    'email': 'contato@prismaavaliacoes.com.br'  # Altere aqui
}
```

### Serviços Oferecidos
Os serviços podem ser editados na mesma view, na seção `'servicos'`.

### Depoimentos
Os depoimentos de clientes também estão configurados na view principal.

### Imagens da Landing Page
As imagens estão localizadas na pasta `media/`:
- `home.jpg`: Imagem alternativa para o hero
- `home2.jpg`: Imagem principal do hero (ativa)

Para trocar a imagem do hero, edite o template `home.html` na linha da imagem:
```html
<img src="/media/nome-da-imagem.jpg" alt="Descrição da imagem">
```

## 📱 Funcionalidades Específicas

### Formulário de Contato
- Validação em tempo real
- Máscara automática para telefone
- Integração direta com WhatsApp
- Mensagem formatada automaticamente

### Navegação
- Menu fixo no topo
- Scroll suave entre seções
- Botão "voltar ao topo"
- Navegação responsiva

### Animações
- Cards com efeito hover
- Animações de entrada
- Transições suaves
- Loading states

## 🚀 Deploy em Produção

### Configurações Necessárias

1. **Configurar DEBUG**:
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['seu-dominio.com']
```

2. **Configurar arquivos estáticos**:
```python
# settings.py
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

3. **Coletar arquivos estáticos**:
```bash
python manage.py collectstatic
```

### Opções de Deploy
- **Heroku**: Plataforma simples para deploy
- **PythonAnywhere**: Hospedagem específica para Python
- **DigitalOcean**: VPS com mais controle
- **AWS/Azure**: Soluções enterprise

## 🔒 Segurança

- SECRET_KEY deve ser alterada em produção
- Configurar HTTPS obrigatório
- Validação de formulários no backend
- Proteção CSRF habilitada

## 📊 SEO e Performance

### Meta Tags Configuradas
- Description otimizada
- Keywords relevantes
- Open Graph (preparado para redes sociais)
- Viewport responsivo

### Performance
- CSS e JS minificados (CDN)
- Imagens otimizadas
- Lazy loading preparado
- Cache de assets

## 🐛 Troubleshooting

### Problema: Servidor não inicia
```bash
# Verifique se o ambiente virtual está ativo
# Verifique se as dependências estão instaladas
pip list
```

### Problema: Arquivos estáticos não carregam
```bash
# Execute collectstatic
python manage.py collectstatic
```

### Problema: Formulário não funciona
- Verifique se o JavaScript está carregando
- Verifique o console do navegador
- Teste a conectividade com WhatsApp

## 📞 Suporte

Para dúvidas sobre o código ou implementação:
- Consulte a documentação do Django: https://docs.djangoproject.com/
- Bootstrap 5: https://getbootstrap.com/docs/5.3/

## 📝 Licença

Este projeto foi desenvolvido especificamente para a Prisma Avaliações Imobiliárias.

---

**Desenvolvido com ❤️ para o mercado imobiliário brasileiro**
