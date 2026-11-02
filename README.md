# Projeto RBAC em Python

Projeto de estudo e desenvolvimento de uma **Plataforma de Gerenciamento de Acessos baseada em RBAC (Role-Based Access Control)**, aplicada ao contexto de **IAM (Identity and Access Management)** e Segurança da Informação.

## Objetivo

Desenvolver, de forma incremental, uma plataforma para gerenciar usuários, funções (Roles), permissões e grupos, aplicando princípios de controle de acesso e Segurança da Informação.

O projeto tem como foco o aprendizado prático de Python, modelagem de sistemas, desenvolvimento de APIs, bancos de dados e conceitos de IAM.

## Funcionalidades implementadas

- Cadastro e consulta de usuários.
- Atualização, desativação e reativação de usuários.
- Gerenciamento de Roles e permissões.
- Associação de permissões a Roles.
- Gerenciamento de grupos e associações entre usuários e Roles.
- Verificação de autorização conforme as permissões atribuídas.
- Persistência de dados com SQLite.
- Autenticação por matrícula e senha.
- Armazenamento de senhas com hash Argon2id.
- Autenticação baseada em tokens JWT.
- API REST desenvolvida com FastAPI.
- Testes automatizados com pytest.

## Tecnologias utilizadas

- **Python** — linguagem principal.
- **SQLite** — banco de dados relacional.
- **FastAPI** — desenvolvimento da API REST.
- **Pydantic** — validação de dados.
- **Argon2id** — armazenamento seguro de senhas.
- **PyJWT** — criação e validação de tokens JWT.
- **python-dotenv** — gerenciamento de variáveis de ambiente.
- **pytest** — testes automatizados.
- **HTTPX** — suporte aos testes da API.
- **Git e GitHub** — versionamento e documentação.

## Conceitos de Segurança da Informação abordados

- Identity and Access Management (IAM).
- Role-Based Access Control (RBAC).
- Princípio do menor privilégio.
- Segregação de funções (SoD).
- Autenticação e autorização.
- Hash de senhas.
- Autenticação baseada em tokens.

## Status do projeto

**Em desenvolvimento (MVP).**

O projeto já possui uma estrutura funcional de gerenciamento de acessos, persistência em banco de dados, autenticação, autorização e API REST.

## Objetivo de aprendizado

Compreender não apenas como implementar um sistema de controle de acesso, mas também as decisões de arquitetura, as regras de autorização e os impactos dessas decisões na Segurança da Informação.

## Aviso

Este projeto possui finalidade educacional. Não deve ser utilizado para controlar acessos em ambientes de produção sem uma avaliação de segurança, testes adequados e os controles necessários.