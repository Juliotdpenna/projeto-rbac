# RBAC Manager — Plataforma de Gerenciamento de Acessos

Projeto de estudo e desenvolvimento de uma **Plataforma de Gerenciamento de Acessos baseada em RBAC (Role-Based Access Control)**, aplicada ao contexto de **IAM (Identity and Access Management)** e Segurança da Informação.

A aplicação permite gerenciar usuários, Roles, permissões e grupos, com autenticação, autorização e persistência de dados.

## Objetivo

Desenvolver, de forma incremental, uma plataforma de gerenciamento de identidades e acessos, aplicando conceitos de controle de acesso e Segurança da Informação.

O projeto tem como foco o aprendizado prático de Python, desenvolvimento de APIs, bancos de dados relacionais, desenvolvimento web e princípios de segurança.

## Funcionalidades implementadas

### Gerenciamento de acessos

- Cadastro, consulta, atualização, desativação e reativação de usuários.
- Gerenciamento de Roles e permissões.
- Associação e remoção de permissões às Roles.
- Gerenciamento de grupos.
- Associação e remoção de usuários e Roles aos grupos.
- Verificação de autorização com base nas permissões atribuídas.
- Persistência de dados utilizando SQLite.

### Autenticação e segurança

- Autenticação por matrícula e senha.
- Armazenamento de senhas utilizando hash Argon2id.
- Autenticação baseada em tokens JWT.
- Validação de tokens e controle de expiração.
- Proteção das rotas administrativas por autenticação e autorização.
- Limitação de tentativas de login (Rate Limiting).

**Observação sobre o Rate Limiting:** O controle de tentativas de login utiliza armazenamento em memória, sendo limitado a uma única instância da aplicação. Os registros são reiniciados quando a aplicação é encerrada ou reiniciada.

- Registro de eventos de autenticação e operações administrativas (Logs de Auditoria).

### Interface web

- Interface desenvolvida com React e Vite.
- Dashboard com indicadores de usuários, Roles, permissões e grupos.
- Telas para gerenciamento dos principais recursos.
- Integração com a API REST desenvolvida em FastAPI.

### Testes

- Testes automatizados com pytest.
- Testes de endpoints e regras de negócio.
- Verificações de autenticação, autorização e segurança.

## Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Linguagem principal do backend |
| FastAPI | Desenvolvimento da API REST |
| SQLite | Banco de dados relacional |
| Pydantic | Validação de dados |
| Argon2id | Hash de senhas |
| PyJWT | Criação e validação de tokens JWT |
| python-dotenv | Gerenciamento de variáveis de ambiente |
| pytest | Testes automatizados |
| HTTPX | Testes da API |
| JavaScript | Desenvolvimento do frontend |
| React | Construção da interface web |
| Vite | Ferramenta de desenvolvimento do frontend |
| HTML e CSS | Estrutura e estilização da interface |
| Git e GitHub | Versionamento e documentação |

## Conceitos de Segurança da Informação abordados

- Identity and Access Management (IAM).
- Role-Based Access Control (RBAC).
- Princípio do menor privilégio.
- Segregação de funções (SoD).
- Autenticação e autorização.
- Hash de senhas.
- JSON Web Tokens (JWT).
- Controle de sessões e expiração de tokens.
- Rate Limiting.
- Logs de auditoria.

## Como executar o projeto

### Pré-requisitos

- Python 3.13 ou superior.
- Node.js e npm.
- Git.

### 1. Clonar o repositório

```bash
git clone https://github.com/Juliotdpenna/projeto-rbac.git
```

Acesse a pasta do projeto:

```bash
cd projeto-rbac
```

### 2. Preparar o backend

Crie um ambiente virtual:

```bash
python -m venv .venv
```

No Windows PowerShell, ative o ambiente:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

### 3. Configurar as variáveis de ambiente

Copie o arquivo `.env.example` para `.env`.

No Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Configure as variáveis:

- `JWT_SECRET`: substitua o valor de exemplo por uma chave secreta forte e aleatória.
- `ADMIN_MATRICULA`: informe a matrícula que será utilizada pelo primeiro administrador.

**Importante:** não compartilhe nem publique o arquivo `.env`. Ele contém informações sensíveis do ambiente.

### 4. Inicializar o banco de dados

Com o ambiente virtual ativado e na raiz do projeto, execute:

Criação das tabelas SQLite:

```bash
python -m database.criar_tabelas
```

Cadastro das permissões iniciais:

```bash
python cadastrar_permissoes_iniciais.py
```

Criação do primeiro administrador:

```bash
python criar_administrador_inicial.py
```

Durante essa etapa, serão solicitados os dados do administrador e uma senha com pelo menos 12 caracteres.

A matrícula informada deverá ser a mesma configurada em `ADMIN_MATRICULA` no arquivo `.env`.

Configuração da Role administrativa:

```bash
python configurar_administrador.py
```

Esse procedimento cria ou configura a Role `ROLE_ADMINISTRADOR`, associa as permissões ativas e atribui a Role ao usuário administrador.

### 5. Iniciar o backend

Na raiz do projeto, execute:

```bash
uvicorn api:app --reload
```

A API estará disponível em:

`http://127.0.0.1:8000`

A documentação interativa estará disponível em:

`http://127.0.0.1:8000/docs`

### 6. Iniciar o frontend

Abra outro terminal e acesse a pasta `frontend`:

```bash
cd frontend
```

Instale as dependências:

```bash
npm install
```

Inicie a aplicação:

```bash
npm run dev
```

O Vite exibirá o endereço local para acessar a interface web.

### 7. Executar os testes automatizados

Na raiz do projeto, com o ambiente virtual ativado, execute:

```bash
python -m pytest
```

## Estrutura do projeto

```text
Projeto_RBAC/
├── database/
├── frontend/
│   ├── src/
│   └── ...
├── logs/
├── models/
├── services/
├── tests/
├── utils/
├── .env.example
├── .gitignore
├── api.py
├── cadastrar_permissoes_iniciais.py
├── configurar_administrador.py
├── criar_administrador_inicial.py
├── main.py
├── README.md
└── requirements.txt
```

## Status do projeto

**Em desenvolvimento — MVP funcional.**

O projeto já conta com gerenciamento de acessos, persistência em banco de dados, API REST, autenticação, autorização, interface web, testes automatizados e mecanismos iniciais de segurança.

## Próximas evoluções

- Aprimoramento do dashboard e dos relatórios.
- Evolução dos registros de auditoria.
- Fluxos de aprovação de acessos.
- Implementação de MFA (Autenticação Multifator).
- Evolução do controle de sessões.
- Implementação de ABAC (Attribute-Based Access Control).
- Integração com provedores de identidade (IdP), LDAP e Active Directory.
- Containerização e melhorias de implantação.

## Objetivo de aprendizado

Compreender não apenas como implementar um sistema de controle de acesso, mas também as decisões de arquitetura, as regras de autorização e os impactos dessas decisões na Segurança da Informação.

## Aviso

Este projeto possui finalidade educacional. Apesar de implementar mecanismos de segurança, ainda está em desenvolvimento e não deve ser utilizado para controlar acessos em ambientes de produção sem uma avaliação de segurança, testes adicionais e os controles necessários.
