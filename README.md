# 📘 DOCUMENTAÇÃO E IDEALIZAÇÃO DO PROJETO LEXIFLOW

> **Versão:** 1.0.0  
> **Data:** Maio/2026  
> **Autor:** Dev Team  
> **Status:** Em desenvolvimento — Fase 1 (Autenticação & Cadastro)

---

## 📋 ÍNDICE

1. [Visão Geral](#1-visão-geral)
2. [Funcionalidades Atuais](#2-funcionalidades-atuais)
3. [Arquitetura do Sistema](#3-arquitetura-do-sistema)
4. [Telas do Sistema](#4-telas-do-sistema)
5. [Planos de Assinatura](#5-planos-de-assinatura)
6. [Banco de Dados](#6-banco-de-dados)
7. [Tecnologias Utilizadas](#7-tecnologias-utilizadas)
8. [Instalação e Execução](#8-instalação-e-execução)
9. [Geração do Executável](#9-geração-do-executável)
10. [Próximos Passos (Roadmap)](#10-próximos-passos-roadmap)
11. [Estrutura de Pastas](#11-estrutura-de-pastas)

---

## 1. VISÃO GERAL

### 1.1 O que é o LexiFlow?

**LexiFlow** é uma aplicação desktop desenvolvida em Python por mim com interface gráfica moderna (PyQt6) voltada para **automação e gestão do trabalho jurídico**. O objetivo é oferecer aos advogados e escritórios de advocacia uma ferramenta unificada que reduza tarefas repetitivas, organize documentos e otimize o fluxo de trabalho diário.

### 1.2 Público-Alvo

- Advogados autônomos
- Escritórios de advocacia (pequenos, médios e grandes)
- Departamentos jurídicos de empresas
- Estagiários e assistentes jurídicos

### 1.3 Problema que Resolve

| Problema | Solução do LexiFlow |
|----------|---------------------|
| Perda de prazos processuais | Calculadora de prazos com alertas |
| Geração manual de contratos | Templates automáticos com preenchimento |
| Documentos espalhados | Gestão centralizada com OCR e busca |
| Falta de controle de assinaturas | Sistema de planos com controle de acesso |
| Dificuldade de acompanhar processos | Web scraping de tribunais |

---

## 2. FUNCIONALIDADES ATUAIS

### ✅ Fase 1 — Implementadas (v1.0.0)

#### 2.1 Sistema de Autenticação
- **Tela de Login** — Acesso via nome de usuário cadastrado
- **Tela de Cadastro** — Registro completo com validações
- **Controle de Planos** — Diferentes níveis de acesso por assinatura
- **Persistência Local** — Banco SQLite para armazenar usuários

#### 2.2 Cadastro de Usuário
O sistema coleta as seguintes informações:

| Campo | Obrigatório | Descrição |
|-------|-------------|-----------|
| Nome Completo | ✅ | Identificação do usuário |
| Número OAB | ❌ | Registro profissional |
| Idade | ✅ | Restrição: 18-100 anos |
| Estado (pessoal) | ✅ | UF de residência |
| Cidade (pessoal) | ✅ | Cidade de residência |
| Nome do Escritório | ❌ | Razão social ou nome fantasia |
| Estado do Escritório | ❌ | UF do escritório |
| Cidade do Escritório | ❌ | Cidade do escritório |
| Plano de Assinatura | ✅ | Teste, Essencial, Profissional ou Elite |
| Email Corporativo | Condicional | Obrigatório para planos pagos |

#### 2.3 Validações Automáticas
- ✅ Verificação de idade (18-100 anos)
- ✅ Validação de formato de email
- ✅ Verificação de duplicidade de nome
- ✅ Campos obrigatórios não podem ficar vazios
- ✅ Planos pagos exigem email corporativo

#### 2.4 Interface Gráfica
- 🎨 Tema Dark moderno (inspirado em apps profissionais)
- 📐 Layout responsivo com painéis laterais
- 🖱️ Cards interativos para seleção de planos
- ⚡ Animações sutis de hover e seleção
- 🪟 Janela sem bordas (frameless) com design premium

---

## 3. ARQUITETURA DO SISTEMA

### 3.1 Diagrama de Fluxo

```
┌─────────────────┐
│   Usuário       │
│  (clica .exe)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│  Tela de Login  │────▶│ Tela de Cadastro│
│   (main.py)     │◄────│  (register)     │
└────────┬────────┘     └─────────────────┘
         │
    Login Válido
         │
         ▼
┌─────────────────┐
│    Dashboard    │◄──── Próxima fase
│   (em breve)    │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  SQLite Local   │
│   (lexiflow.db) │
└─────────────────┘
```

### 3.2 Padrão de Projeto

O LexiFlow utiliza o padrão **MVC simplificado**:

| Camada | Responsabilidade | Arquivos |
|--------|------------------|----------|
| **Model** | Dados e persistência | `database.py`, `config.py` |
| **View** | Interface gráfica | `screens/*.py`, `styles/theme.py` |
| **Controller** | Lógica e validações | `utils/validators.py`, eventos nos widgets |

---

## 4. TELAS DO SISTEMA

### 4.1 Tela de Login (`login_screen.py`)

**Objetivo:** Permitir que usuários cadastrados acessem o sistema.

**Layout:**
```
┌─────────────────────────────────────────────┐
│  ┌─────────────┐  ┌──────────────────────┐  │
│  │             │  │  ✕                   │  │
│  │    ⚖️       │  │                      │  │
│  │  LexiFlow   │  │  Bem-vindo de volta  │  │
│  │             │  │  Entre com seu nome  │  │
│  │  [Gradiente]│  │                      │  │
│  │   Azul      │  │  NOME COMPLETO       │  │
│  │   Escuro    │  │  ┌────────────────┐  │  │
│  │             │  │  │ Digite seu nome│  │  │
│  │             │  │  └────────────────┘  │  │
│  │             │  │                      │  │
│  │             │  │  [    ENTRAR    ]    │  │
│  │             │  │                      │  │
│  │             │  │  ────── ou ──────    │  │
│  │             │  │                      │  │
│  │             │  │  [Criar nova conta]  │  │
│  │             │  │                      │  │
│  │             │  │         v1.0.0       │  │
│  └─────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────┘
```

**Comportamentos:**
- Valida se o nome existe no banco de dados
- Verifica se a conta ainda está ativa (não expirou)
- Botão "Criar nova conta" navega para tela de registro
- Botão ✕ fecha a aplicação

---

### 4.2 Tela de Cadastro (`register_screen.py`)

**Objetivo:** Coletar dados do novo usuário e criar conta com plano escolhido.

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  ┌─────────────┐  ┌─────────────────────────────────────┐  │
│  │             │  │ ← Voltar              ✕             │  │
│  │    ⚖️       │  │                                     │  │
│  │  LexiFlow   │  │  Criar sua conta                    │  │
│  │             │  │  Preencha os dados abaixo           │  │
│  │  Etapa 1    │  │                                     │  │
│  │  de 2       │  │  📋 DADOS PESSOAIS                  │  │
│  │             │  │  NOME COMPLETO *                    │  │
│  │  [Gradiente]│  │  ┌────────────────────────────┐     │  │
│  │             │  │  │ Ex: Dr. João Silva         │     │  │
│  │             │  │  └────────────────────────────┘     │  │
│  │             │  │  NÚMERO OAB                         │  │
│  │             │  │  IDADE *                            │  │
│  │             │  │  ESTADO *    │  CIDADE *            │  │
│  │             │  │                                     │  │
│  │             │  │  🏢 DADOS DO ESCRITÓRIO             │  │
│  │             │  │  NOME DO ESCRITÓRIO                 │  │
│  │             │  │  ESTADO    │  CIDADE                │  │
│  │             │  │                                     │  │
│  │             │  │  💎 ESCOLHA SEU PLANO               │  │
│  │             │  │  ┌────┐ ┌────┐ ┌────┐ ┌────┐      │  │
│  │             │  │  │Test│ │Ess │ │Pro │ │Eli │      │  │
│  │             │  │  │e   │ │enc │ │fiss│ │te  │      │  │
│  │             │  │  └────┘ └────┘ └────┘ └────┘      │  │
│  │             │  │                                     │  │
│  │             │  │  EMAIL CORPORATIVO * (condicional)  │  │
│  │             │  │                                     │  │
│  │             │  │  [      CRIAR CONTA      ]          │  │
│  │             │  │                                     │  │
│  │             │  │  Termos de Uso e Privacidade        │  │
│  └─────────────┘  └─────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Comportamentos:**
- Scroll automático para acomodar todos os campos
- Cards de plano com hover e seleção visual
- Campo de email aparece apenas para planos pagos
- Validações em tempo real antes de submeter
- Feedback visual de sucesso ou erro

---

## 5. PLANOS DE ASSINATURA

### 5.1 Comparativo de Planos

| Recurso | Teste | Essencial | Profissional | Elite |
|---------|-------|-----------|--------------|-------|
| **Preço** | Grátis | R$ 49,90/mês | R$ 99,90/mês | R$ 199,90/mês |
| **Duração** | 7 dias | 30 dias | 30 dias | 30 dias |
| **Cor** | Cinza | Azul | Roxo | Dourado |
| **Email obrigatório** | ❌ | ❌ | ✅ | ✅ |
| **Calculadora de prazos** | ✅ | ✅ | ✅ | ✅ |
| **Gerador de contratos** | ✅ (limitado) | ✅ | ✅ | ✅ |
| **OCR em documentos** | ❌ | ❌ | ✅ | ✅ |
| **Web scraping** | ❌ | ❌ | ✅ | ✅ |
| **Dashboard avançado** | ❌ | ❌ | ❌ | ✅ |
| **Suporte prioritário** | ❌ | ❌ | ❌ | ✅ |
| **Usuários simultâneos** | 1 | 1 | 3 | Ilimitado |

### 5.2 Fluxo de Aquisição

```
Usuário seleciona plano
        │
        ▼
┌─────────────────┐
│ Plano é pago?   │
└────────┬────────┘
    Sim /    \\     Não
     │        \\    │
     ▼         \\   ▼
┌─────────┐    \\┌─────────┐
│ Solicita│     │ Cria    │
│ email   │     │ conta   │
│ corporat│     │ direto  │
│ ivo     │     │         │
└────┬────┘     └────┬────┘
     │               │
     ▼               ▼
┌─────────┐     ┌─────────┐
│ Valida  │     │ Libera  │
│ formato │     │ acesso  │
│ email   │     │ por N   │
└────┬────┘     │ dias    │
     │          └─────────┘
     ▼
┌─────────┐
│ Cria    │
│ conta   │
└─────────┘
```

---

## 6. BANCO DE DADOS

### 6.1 Estrutura da Tabela `usuarios`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | INTEGER PK | Identificador único |
| `nome` | TEXT | Nome completo do usuário |
| `oab` | TEXT | Número da OAB |
| `idade` | INTEGER | Idade do usuário |
| `estado` | TEXT | UF de residência |
| `cidade` | TEXT | Cidade de residência |
| `escritorio_nome` | TEXT | Nome do escritório |
| `escritorio_estado` | TEXT | UF do escritório |
| `escritorio_cidade` | TEXT | Cidade do escritório |
| `plano` | TEXT | Tipo de assinatura |
| `email` | TEXT | Email corporativo |
| `data_cadastro` | TEXT | Data/hora do registro (ISO 8601) |
| `data_expiracao` | TEXT | Data de expiração do plano |
| `ativo` | INTEGER | 1 = ativo, 0 = inativo |

### 6.2 Diagrama ER (Simplificado)

```
┌─────────────────────────────────────────┐
│              usuarios                   │
├─────────────────────────────────────────┤
│ PK  id              INTEGER             │
│     nome            TEXT    (UNIQUE)    │
│     oab             TEXT                │
│     idade           INTEGER             │
│     estado          TEXT                │
│     cidade          TEXT                │
│     escritorio_nome TEXT                │
│     escritorio_estado TEXT              │
│     escritorio_cidade TEXT              │
│     plano           TEXT                │
│     email           TEXT                │
│     data_cadastro   TEXT                │
│     data_expiracao  TEXT                │
│     ativo           INTEGER (DEFAULT 1) │
└─────────────────────────────────────────┘
```

---

## 7. TECNOLOGIAS UTILIZADAS

### 7.1 Stack Principal

| Tecnologia | Versão | Função |
|------------|--------|--------|
| **Python** | 3.10+ | Linguagem principal |
| **PyQt6** | 6.6.1 | Interface gráfica (GUI) |
| **SQLite3** | Built-in | Banco de dados local |
| **PyInstaller** | 6.x | Geração de executável |

### 7.2 Bibliotecas Python

```python
# requirements.txt
PyQt6==6.6.1
```

### 7.3 Ferramentas de Desenvolvimento

| Ferramenta | Uso |
|------------|-----|
| VS Code / PyCharm | IDE |
| Git | Controle de versão |
| GitHub | Repositório remoto |
| PyInstaller | Build do executável |

---

## 8. INSTALAÇÃO E EXECUÇÃO

### 8.1 Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes)
- Git (opcional, para clonar)

### 8.2 Passo a Passo

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/LexiFlow.git
cd LexiFlow

# 2. Crie um ambiente virtual (recomendado)
python -m venv venv

# Windows:
venv\\Scripts\\activate

# macOS/Linux:
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o aplicativo
python main.py
```

### 8.3 Primeiro Acesso

1. Execute o aplicativo
2. Na tela de login, clique em **"Criar nova conta"**
3. Preencha todos os campos obrigatórios
4. Selecione o plano **Teste** (7 dias grátis)
5. Clique em **"Criar Conta"**
6. Volte para a tela de login e acesse com seu nome

---

## 9. GERAÇÃO DO EXECUTÁVEL

### 9.1 Instalar PyInstaller

```bash
pip install pyinstaller
```

### 9.2 Comando de Build

```bash
pyinstaller \\
  --noconfirm \\
  --onefile \\
  --windowed \\
  --name "LexiFlow" \\
  --clean \\
  main.py
```

### 9.3 Parâmetros Explicados

| Parâmetro | Descrição |
|-----------|-----------|
| `--noconfirm` | Sobrescreve builds anteriores sem perguntar |
| `--onefile` | Gera um único arquivo `.exe` |
| `--windowed` | Modo GUI (sem console em background) |
| `--name` | Nome do executável gerado |
| `--clean` | Limpa cache antes de buildar |

### 9.4 Saída

```
LexiFlow/
├── build/          # Arquivos temporários (pode deletar)
├── dist/
│   └── LexiFlow.exe   # ← EXECUTÁVEL FINAL
├── LexiFlow.spec   # Configuração do PyInstaller
└── ...
```

### 9.5 Distribuição

O arquivo `dist/LexiFlow.exe` pode ser:
- Copiado para a Área de Trabalho
- Compartilhado via email/pen drive
- Instalado em múltiplas máquinas

> **Nota:** O banco de dados (`lexiflow.db`) será criado automaticamente na primeira execução na mesma pasta do executável.

---

## 10. PRÓXIMOS PASSOS (ROADMAP)

### 🔵 Fase 2 — Dashboard & Navegação (v1.1.0)
**Prioridade: ALTA | Tempo estimado: 2 semanas**

| Tarefa | Descrição |
|--------|-----------|
| Tela Principal (Dashboard) | Painel pós-login com resumo do plano, dias restantes, atalhos |
| Menu Lateral | Navegação entre módulos (Calculadora, Contratos, Documentos, Configurações) |
| Barra Superior | Perfil do usuário, notificações, botão de logout |
| Tela de Perfil | Editar dados cadastrais, visualizar plano atual |
| Tela de Renovação | Upgrade/downgrade de plano com cálculo de prorata |

```
┌─────────────────────────────────────────────────────────────┐
│  LexiFlow                              👤 João │ 🔔 │ ⚙️  │
├────────┬────────────────────────────────────────────────────┤
│  ⚖️    │  ┌─────────────────────────────────────────────┐   │
│ Início │  │  Bem-vindo, Dr. João!                       │   │
│        │  │  Plano: Profissional │ Expira em: 23 dias   │   │
│  📊    │  └─────────────────────────────────────────────┘   │
│  📄    │                                                     │
│  📁    │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │
│  ⚙️    │  │ Calculadora │  │ Contratos   │  │ Processos │  │
│        │  │   de Prazos │  │             │  │           │  │
│        │  └─────────────┘  └─────────────┘  └───────────┘  │
│        │                                                     │
│        │  ┌─────────────────────────────────────────────┐   │
│        │  │  Últimas Atividades                         │   │
│        │  │  • Contrato de locação gerado — há 2h      │   │
│        │  │  • Prazo processual calculado — há 5h      │   │
│        │  └─────────────────────────────────────────────┘   │
└────────┴────────────────────────────────────────────────────┘
```

---

### 🟢 Fase 3 — Módulo Calculadora de Prazos (v1.2.0)
**Prioridade: ALTA | Tempo estimado: 2-3 semanas**

| Tarefa | Descrição |
|--------|-----------|
| Cálculo de Prazos Processuais | CPC/CPP com regras de suspensão, prorrogação |
| Prescrição e Decadência | Cálculo automático por área do Direito |
| Alertas e Lembretes | Notificações desktop para prazos próximos |
| Histórico de Cálculos | Salvar e consultar cálculos anteriores |
| Exportação PDF | Gerar relatório do cálculo para anexar em petições |

**Regras Jurídicas a Implementar:**
- Art. 175, §1º CPC (suspensão por feriado)
- Art. 219 CPC (prazo em dobro para o MP)
- Art. 109 CP (prescrição penal)
- Art. 205 CC (prescrição civil)

---

### 🟡 Fase 4 — Módulo Gerador de Documentos (v1.3.0)
**Prioridade: ALTA | Tempo estimado: 3 semanas**

| Tarefa | Descrição |
|--------|-----------|
| Templates de Contratos | Locação, prestação de serviços, honorários, etc. |
| Preenchimento Automático | Campos dinâmicos com dados do cliente |
| Editor de Templates | Criar/editar templates personalizados |
| Exportação Multi-formato | DOCX, PDF, TXT |
| Assinatura Digital | Integração com certificado digital A1/A3 |

**Templates Iniciais:**
1. Contrato de Locação Residencial
2. Contrato de Honorários Advocatícios
3. Procuração Ad Judicia
4. Petição Inicial (modelo genérico)
5. Recurso de Apelação

---

### 🟠 Fase 5 — Módulo Gestão de Documentos (v1.4.0)
**Prioridade: MÉDIA | Tempo estimado: 3-4 semanas**

| Tarefa | Descrição |
|--------|-----------|
| OCR em PDFs | Converter documentos escaneados em texto pesquisável |
| Classificação Automática | IA identifica tipo de documento (contrato, decisão, petição) |
| Busca Full-Text | Pesquisar por palavras-chave em todos os documentos |
| Organização por Pasta | Estrutura hierárquica por cliente/processos |
| Versionamento | Manter histórico de alterações |

**Bibliotecas:** `pytesseract`, `pdfplumber`, `PyMuPDF`

---

### 🔴 Fase 6 — Módulo Web Scraping (v1.5.0)
**Prioridade: MÉDIA | Tempo estimado: 4 semanas**

| Tarefa | Descrição |
|--------|-----------|
| Consulta Processual | Buscar andamentos em tribunais (TJ, TRF, STJ, STF) |
| Monitoramento | Alertar quando houver movimentação em processos |
| Jurisprudência | Buscar e salvar decisões relevantes |
| Diário Oficial | Rastrear publicações por palavras-chave |
| Relatórios Automáticos | Gerar relatório de andamentos para cliente |

**Tribunais Alvo:**
- PJe (Processo Judicial Eletrônico)
- e-SAJ (Sistema de Automação da Justiça)
- PROJUDI
- e-Proc (V2)

---

### 🟣 Fase 7 — IA e Análise Avançada (v2.0.0)
**Prioridade: BAIXA | Tempo estimado: 6+ semanas**

| Tarefa | Descrição |
|--------|-----------|
| Sumarização de Decisões | IA resume ementas e acórdãos extensos |
| Análise de Risco em Contratos | Destaca cláusulas problemáticas |
| Chatbot Jurídico (RAG) | Responde com base na base de conhecimento do escritório |
| Predição de Resultados | Análise estatística de chances de êxito |
| Geração de Petições com IA | Sugere argumentos com base em jurisprudência |

**Tecnologias:** `langchain`, `transformers`, APIs OpenAI/Claude

---

### 📅 Timeline Resumida

```
Maio/2026    Junho/2026    Julho/2026    Agosto/2026    Set/2026+
    │             │             │             │             │
    ▼             ▼             ▼             ▼             ▼
┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐
│ v1.0.0 │   │ v1.1.0 │   │ v1.2.0 │   │ v1.3.0 │   │ v2.0.0 │
│ Auth   │   │ Dash   │   │ Prazos │   │ Docs   │   │  IA    │
│ Cadastro│   │ Perfil │   │ Alertas│   │ OCR    │   │ RAG    │
└────────┘   └────────┘   └────────┘   └────────┘   └────────┘
   AGORA       +2 sem      +4 sem      +7 sem      +13 sem
```

---

## 11. ESTRUTURA DE PASTAS

```
LexiFlow/
│
├── 📄 main.py                          # Ponto de entrada da aplicação
├── 📄 config.py                        # Configurações e constantes
├── 📄 database.py                      # Camada de persistência (SQLite)
├── 📄 requirements.txt                 # Dependências do projeto
├── 📄 README.md                        # Documentação rápida (GitHub)
│
├── 📁 assets/                          # Recursos visuais
│   ├── logo.png                        # Logo do aplicativo
│   ├── icon.ico                        # Ícone do executável
│   └── fonts/                          # Fontes customizadas
│
├── 📁 screens/                         # Telas da aplicação
│   ├── __init__.py
│   ├── login_screen.py                 # Tela de login
│   ├── register_screen.py              # Tela de cadastro
│   ├── dashboard_screen.py             # [FUTURO] Dashboard principal
│   ├── calculator_screen.py            # [FUTURO] Calculadora de prazos
│   ├── documents_screen.py             # [FUTURO] Gerador de documentos
│   └── settings_screen.py              # [FUTURO] Configurações
│
├── 📁 utils/                           # Utilitários
│   ├── __init__.py
│   ├── validators.py                   # Validações de formulário
│   ├── formatters.py                   # Formatação de dados
│   └── helpers.py                      # Funções auxiliares
│
├── 📁 styles/                          # Temas visuais
│   ├── __init__.py
│   ├── theme.py                        # Tema Dark principal
│   └── theme_light.py                  # [FUTURO] Tema claro
│
├── 📁 templates/                       # Templates de documentos
│   ├── contrato_locacao.docx
│   ├── procuracao.docx
│   └── peticao_inicial.docx
│
├── 📁 models/                          # [FUTURO] Modelos de dados
│   ├── __init__.py
│   ├── usuario.py
│   ├── processo.py
│   └── documento.py
│
├── 📁 services/                        # [FUTURO] Integrações
│   ├── __init__.py
│   ├── ocr_service.py
│   ├── scraper_service.py
│   └── ai_service.py
│
└── 📁 tests/                           # Testes automatizados
    ├── __init__.py
    ├── test_validators.py
    └── test_database.py
```

---

## 📎 ANEXOS

### A. Convenções de Código

- **Nomenclatura:** snake_case para variáveis/funções, PascalCase para classes
- **Idioma:** Português para UI, Inglês para código interno
- **Docstrings:** Google Style
- **Commits:** Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`)

### B. Contato e Suporte

- **Repositório:** github.com/seu-usuario/LexiFlow
- **Issues:** Reporte bugs e sugestões via GitHub Issues
- **Email:** suporte@lexiflow.com.br (futuro)

---

> **Documento gerado em:** 16 de Maio de 2026  
> **Última atualização:** v1.0.0  
> **Próxima revisão:** Após lançamento da Fase 2

---
*LexiFlow — Tecnologia a serviço da Advocacia ⚖️*
"""
