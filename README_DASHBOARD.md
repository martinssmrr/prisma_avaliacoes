# Dashboard de Vendas - Prisma Avaliações

## 🎯 Sistema Implementado

### Dashboard Administrativo Completo
Um sistema de controle de vendas profissional com interface moderna e funcionalidades avançadas para gerenciar o processo comercial da Prisma Avaliações.

## 🔧 Funcionalidades Implementadas

### 1. **Gestão de Clientes**
- Cadastro completo com nome, telefone, email, cidade e estado
- Listagem com filtros e busca
- Visualização do histórico de vendas por cliente
- Campos obrigatórios e opcionais bem organizados

### 2. **Controle de Vendas (7 Etapas)**
- **Orçamento**: Elaboração e envio da proposta
- **Venda**: Fechamento do negócio
- **Documentação**: Coleta de documentos necessários
- **1º Sinal**: Recebimento do primeiro pagamento
- **Confecção**: Elaboração do laudo/avaliação
- **2º Sinal**: Recebimento do pagamento final
- **Envio**: Entrega do produto final

### 3. **Dashboard Visual**
- **Estatísticas em tempo real**: Total de clientes, vendas, status
- **Cartões coloridos**: Visual moderno com ícones FontAwesome
- **Barras de progresso**: Acompanhamento visual de cada venda
- **Status badges**: Identificação rápida do status (Iniciada/Em Andamento/Concluída)
- **Tabela de vendas recentes**: Últimas 10 vendas com detalhes

### 4. **Interface Moderna (Django Jazzmin)**
- Design responsivo e profissional
- Menu lateral organizado por categorias
- Tema claro/escuro disponível
- Ícones personalizados para cada seção
- Logo da empresa integrada

### 5. **Funcionalidades Avançadas**
- **Botão "Avançar Etapa"**: Progresso automático no workflow
- **Filtros personalizados**: Por status da venda
- **Busca inteligente**: Por cliente, telefone, ID da venda
- **Campos calculados**: Status geral, percentual de progresso, próxima etapa
- **Relacionamentos**: Cliente ↔ Vendas com histórico completo

### 6. **Automação de Processo**
- Cálculo automático do progresso (0% a 100%)
- Determinação da próxima etapa automaticamente
- Status geral baseado nas etapas concluídas
- Mensagens de feedback ao avançar etapas

## 🚀 Como Acessar

### Credenciais de Acesso:
- **URL**: http://127.0.0.1:8000/admin/
- **Usuário**: `prisma`
- **Senha**: `prisma123`

### URLs Importantes:
- **Dashboard Principal**: `/admin/`
- **Dashboard de Vendas**: `/admin/controle/venda/dashboard/`
- **Clientes**: `/admin/controle/cliente/`
- **Vendas**: `/admin/controle/venda/`

## 📊 Dados de Exemplo

O sistema já vem com 5 clientes e 5 vendas de exemplo:

### Clientes:
1. João Silva (SP) - Venda Concluída
2. Maria Santos (RJ) - Em Andamento (43%)
3. Pedro Costa (MG) - Em Andamento (14%)
4. Ana Oliveira (PR) - Em Andamento (71%)
5. Carlos Ferreira (RS) - Iniciada (0%)

### Status das Vendas:
- **1 Concluída** (100%)
- **3 Em Andamento** (14% a 71%)
- **1 Iniciada** (0%)

## 🎨 Características Visuais

### Cores do Sistema:
- **Iniciada**: Amarelo (#F59E0B)
- **Em Andamento**: Azul (#3B82F6)
- **Concluída**: Verde (#10B981)

### Elementos Visuais:
- Barras de progresso animadas
- Ícones FontAwesome para cada seção
- Cards estatísticos com hover effects
- Tabelas responsivas com destaque ao passar o mouse
- Botões de ação com feedback visual

## 🔄 Fluxo de Trabalho

1. **Cadastrar Cliente** → Novo cliente no sistema
2. **Criar Venda** → Associar venda ao cliente
3. **Acompanhar Progresso** → Usar botão "Avançar" em cada etapa
4. **Monitorar Dashboard** → Visão geral de todas as vendas
5. **Finalizar Processo** → Venda marcada como concluída

## 🛠️ Tecnologias Utilizadas

- **Django 5.2.5**: Framework principal
- **Django Jazzmin**: Interface administrativa moderna
- **Bootstrap 5**: Design responsivo
- **FontAwesome**: Ícones profissionais
- **Python 3.12**: Linguagem de programação
- **SQLite**: Banco de dados (desenvolvimento)

## 📈 Benefícios do Sistema

### Para a Gestão:
- Visão completa do pipeline de vendas
- Identificação de gargalos no processo
- Controle financeiro por etapas
- Histórico completo de cada cliente

### Para a Operação:
- Interface intuitiva e rápida
- Automação de cálculos
- Redução de erros manuais
- Padronização do processo

### Para o Cliente:
- Maior transparência no processo
- Acompanhamento de progresso
- Comunicação mais eficiente
- Entrega dentro do prazo

## 🔧 Comandos Úteis

### Iniciar o Servidor:
```bash
cd "C:\Users\teste\OneDrive\Desktop\Prisma Avaliações Imobiliarias"
./venv/Scripts/python manage.py runserver
```

### Criar Novo Superusuário:
```bash
./venv/Scripts/python manage.py createsuperuser
```

### Aplicar Migrações:
```bash
./venv/Scripts/python manage.py migrate
```

### Coletar Arquivos Estáticos:
```bash
./venv/Scripts/python manage.py collectstatic
```

---

**Sistema desenvolvido para otimizar o controle de vendas da Prisma Avaliações Imobiliárias** 🏢✨
