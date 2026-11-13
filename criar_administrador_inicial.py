
import sqlite3
from getpass import getpass

from dotenv import load_dotenv
import os

from database.repositorio import (
    cadastrar_usuario,
    consultar_usuarios,
)
from models.usuario import Usuario
from utils.seguranca import gerar_hash_senha


load_dotenv()

ADMIN_MATRICULA = os.getenv("ADMIN_MATRICULA")


def criar_administrador_inicial():

    if not ADMIN_MATRICULA:
        raise RuntimeError(
            "Configure ADMIN_MATRICULA no arquivo .env."
        )

    print("=== CRIAÇÃO DO ADMINISTRADOR INICIAL ===\n")

    nome = input("Nome completo: ").strip()
    departamento = input("Departamento: ").strip()
    cargo = input("Cargo: ").strip()

    if not nome or not departamento or not cargo:
        raise ValueError("Todos os campos são obrigatórios.")

    matricula = input("Matrícula: ").strip()

    if not matricula:
        raise ValueError("A matrícula não pode ficar vazia.")

    if matricula != ADMIN_MATRICULA:
        raise ValueError(
            "A matrícula informada não corresponde à "
            "ADMIN_MATRICULA configurada no .env."
        )

    usuarios_existentes = consultar_usuarios()

    if any(u.matricula == matricula for u in usuarios_existentes):
        raise ValueError(
            "Já existe um usuário cadastrado com essa matrícula."
        )

    senha = getpass("Digite a senha (mínimo 12 caracteres): ")
    confirmacao = getpass("Confirme a senha: ")

    if len(senha) < 12:
        raise ValueError(
            "A senha precisa ter pelo menos 12 caracteres."
        )

    if senha != confirmacao:
        raise ValueError("As senhas não coincidem.")

    senha_hash = gerar_hash_senha(senha)

    usuario = Usuario(
        None,
        nome,
        matricula,
        departamento,
        cargo,
        True,
        None,
        senha_hash,
    )

    try:
        cadastrar_usuario(usuario)

    except sqlite3.IntegrityError:
        raise ValueError(
            "Não foi possível cadastrar: a matrícula já existe."
        )

    print("\nAdministrador inicial cadastrado com sucesso!")
    print(f"ID: {usuario.id}")
    print(f"Matrícula: {usuario.matricula}")


if __name__ == "__main__":
    criar_administrador_inicial()
