from database.criar_tabelas import criar_tabelas
from database.conexao import conectar
from database.repositorio import (
    cadastrar_role,
    consultar_roles,
    cadastrar_permissao,
    associar_permissao_role,
    cadastrar_usuario,
    consultar_usuarios,
    cadastrar_grupo,
    consultar_grupos,
    consultar_grupos_do_usuario,
)
from models.grupo import Grupo
from models.role import Role
from models.permissao import Permissao
from models.usuario import Usuario
import sqlite3
import pytest

def test_cadastrar_e_consultar_role(tmp_path):
    caminho_banco = tmp_path / "rbac_teste.db"

    criar_tabelas(caminho_banco)

    conexao = conectar(caminho_banco)

    try:
        role_original = Role(
            1,
            "ROLE_TESTE",
            "Role criada para teste automatizado",
            True,
        )

        cadastrar_role(role_original, conexao=conexao)
        conexao.commit()

        roles = consultar_roles(conexao=conexao)

        assert len(roles) == 1
        assert roles[0].id == 1
        assert roles[0].nome == "ROLE_TESTE"
        assert roles[0].descricao == "Role criada para teste automatizado"
        assert roles[0].status is True

    finally:
        conexao.close()

def test_persistir_relacionamento_role_permissao(tmp_path):
    caminho_banco = tmp_path / "rbac_relacionamento.db"

    criar_tabelas(caminho_banco)
    conexao = conectar(caminho_banco)

    try:
        role = Role(
            1,
            "ROLE_ANALISTA",
            "Role de analista",
            True,
        )

        permissao = Permissao(
            1,
            "VISUALIZAR_RELATORIOS",
            "Permite visualizar relatórios",
            True,
        )

        cadastrar_role(role, conexao=conexao)
        cadastrar_permissao(permissao, conexao=conexao)

        associar_permissao_role(
            role.id,
            permissao.id,
            conexao=conexao,
        )

        conexao.commit()

        roles = consultar_roles(conexao=conexao)

        assert len(roles) == 1
        assert len(roles[0].permissoes) == 1
        assert roles[0].permissoes[0].id == permissao.id
        assert roles[0].permissoes[0].nome == "VISUALIZAR_RELATORIOS"

    finally:
        conexao.close()

def test_persistir_usuario_com_role_direta(tmp_path):
    caminho_banco = tmp_path / "rbac_usuario.db"

    criar_tabelas(caminho_banco)
    conexao = conectar(caminho_banco)

    try:
        role = Role(
            1,
            "ROLE_ANALISTA",
            "Role de analista",
            True,
        )

        usuario = Usuario(
            1,
            "Usuario Teste",
            "MAT-TESTE-01",
            "TI",
            "Analista",
            True,
            role,
        )

        cadastrar_role(role, conexao=conexao)
        cadastrar_usuario(usuario, conexao=conexao)
        conexao.commit()

        usuarios = consultar_usuarios(conexao=conexao)

        assert len(usuarios) == 1
        assert usuarios[0].id == 1
        assert usuarios[0].nome == "Usuario Teste"
        assert len(usuarios[0].roles_diretas) == 1
        assert usuarios[0].roles_diretas[0].id == role.id
        assert usuarios[0].roles_diretas[0].nome == "ROLE_ANALISTA"

    finally:
        conexao.close()

def test_persistir_grupo_com_usuario_e_role(tmp_path):
    caminho_banco = tmp_path / "rbac_grupo.db"

    criar_tabelas(caminho_banco)
    conexao = conectar(caminho_banco)

    try:
        role = Role(
            1,
            "ROLE_ANALISTA",
            "Role de analista",
            True,
        )

        usuario = Usuario(
            1,
            "Usuario Teste",
            "MAT-TESTE-01",
            "TI",
            "Analista",
            True,
            None,
        )

        grupo = Grupo(
            1,
            "GRUPO_TI",
            "Grupo da equipe de TI",
            True,
        )

        cadastrar_role(role, conexao=conexao)
        cadastrar_usuario(usuario, conexao=conexao)

        grupo.adicionar_usuario(usuario)
        grupo.adicionar_role(role)

        cadastrar_grupo(grupo, conexao=conexao)
        conexao.commit()

        grupos = consultar_grupos(conexao=conexao)

        assert len(grupos) == 1
        assert grupos[0].id == 1
        assert grupos[0].nome == "GRUPO_TI"

        assert len(grupos[0].usuarios) == 1
        assert grupos[0].usuarios[0].id == usuario.id

        assert len(grupos[0].roles) == 1
        assert grupos[0].roles[0].id == role.id

    finally:
        conexao.close()

def test_consultar_grupos_do_usuario(tmp_path):
    caminho_banco = tmp_path / "rbac_grupos_usuario.db"

    criar_tabelas(caminho_banco)
    conexao = conectar(caminho_banco)

    try:
        usuario = Usuario(
            1,
            "Usuario Teste",
            "MAT-TESTE-01",
            "TI",
            "Analista",
            True,
            None,
        )

        grupo = Grupo(
            1,
            "GRUPO_TI",
            "Grupo da equipe de TI",
            True,
        )

        cadastrar_usuario(usuario, conexao=conexao)

        grupo.adicionar_usuario(usuario)
        cadastrar_grupo(grupo, conexao=conexao)
        conexao.commit()

        grupos = consultar_grupos_do_usuario(
            usuario.id,
            conexao=conexao,
        )

        assert len(grupos) == 1
        assert grupos[0].id == grupo.id
        assert grupos[0].nome == "GRUPO_TI"

    finally:
        conexao.close()

def test_banco_rejeita_role_inexistente(tmp_path):
    caminho_banco = tmp_path / "rbac_integridade.db"

    criar_tabelas(caminho_banco)
    conexao = conectar(caminho_banco)

    try:
        with pytest.raises(sqlite3.IntegrityError):
            conexao.execute(
                """
                INSERT INTO role_permissoes (role_id, permissao_id)
                VALUES (?, ?)
                """,
                (999, 1),
            )
    finally:
        conexao.close()

def test_rollback_desfaz_operacao_no_banco(tmp_path):
    caminho_banco = tmp_path / "rbac_rollback.db"

    criar_tabelas(caminho_banco)
    conexao = conectar(caminho_banco)

    try:
        conexao.execute(
            """
            INSERT INTO roles (id, nome, descricao, status)
            VALUES (?, ?, ?, ?)
            """,
            (1, "ROLE_TESTE", "Role de teste", 1),
        )

        conexao.rollback()

        registros = conexao.execute(
            "SELECT * FROM roles WHERE id = ?",
            (1,),
        ).fetchall()

        assert registros == []

    finally:
        conexao.close()

def test_cadastro_usuario_falha_sem_role_existente(tmp_path):
    caminho_banco = tmp_path / "rbac_rollback_usuario.db"
    criar_tabelas(caminho_banco)

    conexao = conectar(caminho_banco)

    usuario = Usuario(
        1,
        "Usuario Teste",
        "MAT-ROLLBACK",
        "TI",
        "Analista",
        True,
        None,
    )

    usuario.roles_diretas.append(
        Role(999, "ROLE_INEXISTENTE", "Role inexistente", True)
    )

    try:
        with pytest.raises(sqlite3.IntegrityError):
            cadastrar_usuario(usuario, conexao=conexao)

        conexao.rollback()

        registros = conexao.execute(
            "SELECT * FROM usuarios WHERE id = ?",
            (usuario.id,),
        ).fetchall()

        assert registros == []

    finally:
        conexao.close()

def test_cadastro_grupo_faz_rollback_se_usuario_nao_existir(tmp_path):
    caminho_banco = tmp_path / "rbac_rollback_grupo.db"
    criar_tabelas(caminho_banco)

    conexao = conectar(caminho_banco)

    try:
        grupo = Grupo(
            1,
            "GRUPO_TESTE",
            "Grupo para teste de rollback",
            True,
        )

        usuario_inexistente = Usuario(
            999,
            "Usuario Inexistente",
            "MAT-INEXISTENTE",
            "TI",
            "Analista",
            True,
            None,
        )

        grupo.adicionar_usuario(usuario_inexistente)

        with pytest.raises(sqlite3.IntegrityError):
            cadastrar_grupo(grupo, conexao=conexao)

        conexao.rollback()

        registro = conexao.execute(
            "SELECT * FROM grupos WHERE id = ?",
            (grupo.id,),
        ).fetchone()

        assert registro is None

    finally:
        conexao.close()

def test_cadastro_usuario_rejeita_matricula_duplicada(tmp_path):
    caminho_banco = tmp_path / "rbac_matricula.db"
    criar_tabelas(caminho_banco)

    conexao = conectar(caminho_banco)

    usuario1 = Usuario(
        1, "João", "MAT-001", "TI", "Analista", True, None
    )
    usuario2 = Usuario(
        2, "Maria", "MAT-001", "RH", "Analista", True, None
    )

    try:
        cadastrar_usuario(usuario1, conexao=conexao)
        conexao.commit()

        with pytest.raises(sqlite3.IntegrityError):
            cadastrar_usuario(usuario2, conexao=conexao)

        conexao.rollback()

        registros = conexao.execute(
            "SELECT id FROM usuarios WHERE matricula = ?",
            ("MAT-001",),
        ).fetchall()

        assert len(registros) == 1
        assert registros[0][0] == 1

    finally:
        conexao.close()

def test_cadastro_role_rejeita_nome_duplicado(tmp_path):
    caminho_banco = tmp_path / "rbac_role_duplicada.db"
    criar_tabelas(caminho_banco)

    conexao = conectar(caminho_banco)

    try:
        cadastrar_role(
            Role(1, "ROLE_ANALISTA", "Analista", True),
            conexao=conexao,
        )
        conexao.commit()

        with pytest.raises(sqlite3.IntegrityError):
            cadastrar_role(
                Role(2, "ROLE_ANALISTA", "Outra descrição", True),
                conexao=conexao,
            )

        conexao.rollback()

        registros = conexao.execute(
            "SELECT id FROM roles WHERE nome = ?",
            ("ROLE_ANALISTA",),
        ).fetchall()

        assert len(registros) == 1
        assert registros[0][0] == 1

    finally:
        conexao.close()