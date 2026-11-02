from database.conexao import conectar
from models.role import Role
from models.permissao import Permissao
from models.usuario import Usuario
from models.grupo import Grupo

def cadastrar_role(role, conexao=None):
    fechar_conexao = conexao is None

    if fechar_conexao:
        conexao = conectar()

    try:
        cursor = conexao.execute(
            """
            INSERT INTO roles (nome, descricao, status)
            VALUES (?, ?, ?)
            """,
            (role.nome, role.descricao, int(role.status))
        )

        role.id = cursor.lastrowid

        if fechar_conexao:
            conexao.commit()

        print("Role cadastrada no banco com sucesso.")

    except Exception:
        if fechar_conexao:
            conexao.rollback()
        raise

    finally:
        if fechar_conexao:
            conexao.close()

def consultar_roles(conexao=None):
    fechar_conexao = conexao is None

    if fechar_conexao:
        conexao = conectar()

    try:
        registros = conexao.execute(
            """
            SELECT id, nome, descricao, status
            FROM roles
            ORDER BY id
            """
        ).fetchall()

        roles = []

        for registro in registros:
            role = Role(
                registro[0],
                registro[1],
                registro[2],
                bool(registro[3])
            )

            role.permissoes = consultar_permissoes_da_role(
                role.id,
                conexao=conexao
            )

            roles.append(role)

        return roles

    finally:
        if fechar_conexao:
            conexao.close()

def cadastrar_permissao(permissao, conexao=None):
    fechar_conexao = conexao is None

    if fechar_conexao:
        conexao = conectar()

    try:
        cursor = conexao.execute(
            """
            INSERT INTO permissoes (nome, descricao, status)
            VALUES (?, ?, ?)
            """,
            (
                permissao.nome,
                permissao.descricao,
                int(permissao.status)
            )
        )

        permissao.id = cursor.lastrowid

        if fechar_conexao:
            conexao.commit()

        print("Permissão cadastrada no banco com sucesso.")

    except Exception:
        if fechar_conexao:
            conexao.rollback()
        raise

    finally:
        if fechar_conexao:
            conexao.close()

def consultar_permissoes(conexao=None):
    fechar_conexao = conexao is None

    if fechar_conexao:
        conexao = conectar()

    try:
        registros = conexao.execute(
            """
            SELECT id, nome, descricao, status
            FROM permissoes
            ORDER BY id
            """
        ).fetchall()

        permissoes = []

        for registro in registros:
            permissao = Permissao(
                registro[0],
                registro[1],
                registro[2],
                bool(registro[3])
            )
            permissoes.append(permissao)

        return permissoes

    finally:
        if fechar_conexao:
            conexao.close()


def associar_permissao_role(role_id, permissao_id, conexao=None):
    fechar_conexao = conexao is None

    if fechar_conexao:
        conexao = conectar()

    try:
        conexao.execute(
            """
            INSERT INTO role_permissoes (role_id, permissao_id)
            VALUES (?, ?)
            """,
            (role_id, permissao_id)
        )

        if fechar_conexao:
            conexao.commit()

        print("Permissão associada à Role com sucesso.")

    except Exception:
        if fechar_conexao:
            conexao.rollback()
        raise

    finally:
        if fechar_conexao:
            conexao.close()

def consultar_permissoes_da_role(role_id, conexao=None):
    fechar_conexao = conexao is None

    if fechar_conexao:
        conexao = conectar()

    try:
        registros = conexao.execute(
            """
            SELECT p.id, p.nome, p.descricao, p.status
            FROM permissoes p
            JOIN role_permissoes rp
                ON rp.permissao_id = p.id
            WHERE rp.role_id = ?
            ORDER BY p.id
            """,
            (role_id,)
        ).fetchall()

        return [
            Permissao(
                registro[0],
                registro[1],
                registro[2],
                bool(registro[3])
            )
            for registro in registros
        ]

    finally:
        if fechar_conexao:
            conexao.close()

def cadastrar_usuario(usuario, conexao=None):
    fechar_conexao = conexao is None

    if fechar_conexao:
        conexao = conectar()

    try:
        cursor = conexao.execute(
            """
            INSERT INTO usuarios
                (nome, matricula, departamento, cargo, status, senha_hash)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                usuario.nome,
                usuario.matricula,
                usuario.departamento,
                usuario.cargo,
                int(usuario.status),
                usuario.senha_hash
            )
        )

        usuario.id = cursor.lastrowid

        for role in usuario.roles_diretas:
            conexao.execute(
                """
                INSERT INTO usuario_roles (usuario_id, role_id)
                VALUES (?, ?)
                """,
                (usuario.id, role.id)
            )

        if fechar_conexao:
            conexao.commit()

        print("Usuário cadastrado no banco com sucesso.")

    except Exception:
        if fechar_conexao:
            conexao.rollback()
        raise

    finally:
        if fechar_conexao:
            conexao.close()

def associar_role_usuario(usuario_id, role_id, conexao=None):
    fechar_conexao = conexao is None

    if fechar_conexao:
        conexao = conectar()

    try:
        conexao.execute(
            """
            INSERT INTO usuario_roles (usuario_id, role_id)
            VALUES (?, ?)
            """,
            (usuario_id, role_id)
        )

        if fechar_conexao:
            conexao.commit()

    except Exception:
        if fechar_conexao:
            conexao.rollback()
        raise

    finally:
        if fechar_conexao:
            conexao.close()

def consultar_usuarios(conexao=None):
    fechar_conexao = conexao is None

    if fechar_conexao:
        conexao = conectar()

    try:
        registros = conexao.execute(
            """
            SELECT id, nome, matricula, departamento, cargo, status, senha_hash
            FROM usuarios
            ORDER BY id
            """
        ).fetchall()

        roles = consultar_roles(conexao=conexao)
        roles_por_id = {role.id: role for role in roles}

        usuarios = []

        for registro in registros:
            usuario = Usuario(
                registro[0],
                registro[1],
                registro[2],
                registro[3],
                registro[4],
                bool(registro[5]),
                None,
                registro[6]  # senha_hash
            )

            # Carrega as Roles atribuídas diretamente
            associacoes = conexao.execute(
                """
                SELECT role_id
                FROM usuario_roles
                WHERE usuario_id = ?
                ORDER BY role_id
                """,
                (usuario.id,)
            ).fetchall()

            for associacao in associacoes:
                role = roles_por_id.get(associacao[0])

                if role is not None:
                    usuario.roles_diretas.append(role)

            # Carrega os grupos aos quais o usuário pertence
            grupos_associados = conexao.execute(
                """
                SELECT g.id, g.nome, g.descricao, g.status
                FROM grupos g
                JOIN grupo_usuarios gu ON gu.grupo_id = g.id
                WHERE gu.usuario_id = ?
                ORDER BY g.id
                """,
                (usuario.id,)
            ).fetchall()

            for registro_grupo in grupos_associados:
                grupo = Grupo(
                    registro_grupo[0],
                    registro_grupo[1],
                    registro_grupo[2],
                    bool(registro_grupo[3])
                )

                # Carrega as Roles associadas ao grupo
                roles_do_grupo = conexao.execute(
                    """
                    SELECT role_id
                    FROM grupo_roles
                    WHERE grupo_id = ?
                    ORDER BY role_id
                    """,
                    (grupo.id,)
                ).fetchall()

                for associacao in roles_do_grupo:
                    role = roles_por_id.get(associacao[0])

                    if role is not None:
                        grupo.roles.append(role)

                grupo.usuarios.append(usuario)
                usuario.grupos.append(grupo)

            usuarios.append(usuario)

        return usuarios

    finally:
        if fechar_conexao:
            conexao.close()

def cadastrar_grupo(grupo, conexao=None):
    fechar_conexao = conexao is None

    if fechar_conexao:
        conexao = conectar()

    try:
        cursor = conexao.execute(
            """
            INSERT INTO grupos (nome, descricao, status)
            VALUES (?, ?, ?)
            """,
            (grupo.nome, grupo.descricao, int(grupo.status))
        )

        grupo.id = cursor.lastrowid

        for usuario in grupo.usuarios:
            conexao.execute(
                """
                INSERT INTO grupo_usuarios (grupo_id, usuario_id)
                VALUES (?, ?)
                """,
                (grupo.id, usuario.id)
            )

        for role in grupo.roles:
            conexao.execute(
                """
                INSERT INTO grupo_roles (grupo_id, role_id)
                VALUES (?, ?)
                """,
                (grupo.id, role.id)
            )

        if fechar_conexao:
            conexao.commit()

        print("Grupo cadastrado no banco com sucesso.")

    except Exception:
        if fechar_conexao:
            conexao.rollback()
        raise

    finally:
        if fechar_conexao:
            conexao.close()

def consultar_grupos(conexao=None):
    fechar_conexao = conexao is None

    if fechar_conexao:
        conexao = conectar()

    try:
        registros = conexao.execute(
            """
            SELECT id, nome, descricao, status
            FROM grupos
            ORDER BY id
            """
        ).fetchall()

        usuarios_por_id = {
            usuario.id: usuario
            for usuario in consultar_usuarios(conexao=conexao)
        }

        roles_por_id = {
            role.id: role
            for role in consultar_roles(conexao=conexao)
        }

        grupos = []

        for registro in registros:
            grupo = Grupo(
                registro[0],
                registro[1],
                registro[2],
                bool(registro[3])
            )

            usuarios_associados = conexao.execute(
                """
                SELECT usuario_id
                FROM grupo_usuarios
                WHERE grupo_id = ?
                ORDER BY usuario_id
                """,
                (grupo.id,)
            ).fetchall()

            for associacao in usuarios_associados:
                usuario = usuarios_por_id.get(associacao[0])

                if usuario is not None:
                    grupo.usuarios.append(usuario)

                    usuario.grupos = [
                        g for g in usuario.grupos
                        if g.id != grupo.id
                    ]

                    usuario.grupos.append(grupo)

            roles_associadas = conexao.execute(
                """
                SELECT role_id
                FROM grupo_roles
                WHERE grupo_id = ?
                ORDER BY role_id
                """,
                (grupo.id,)
            ).fetchall()

            for associacao in roles_associadas:
                role = roles_por_id.get(associacao[0])

                if role is not None:
                    grupo.roles.append(role)

            grupos.append(grupo)

        return grupos

    finally:
        if fechar_conexao:
            conexao.close()


def consultar_grupos_do_usuario(usuario_id, conexao=None):
    grupos = consultar_grupos(conexao=conexao)

    return [
        grupo
        for grupo in grupos
        if any(usuario.id == usuario_id for usuario in grupo.usuarios)
    ]


def atualizar_usuario(usuario, conexao=None):
    fechar_conexao = conexao is None

    if fechar_conexao:
        conexao = conectar()

    try:
        resultado = conexao.execute(
            """
            UPDATE usuarios
            SET nome = ?,
                matricula = ?,
                departamento = ?,
                cargo = ?,
                status = ?
            WHERE id = ?
            """,
            (
                usuario.nome,
                usuario.matricula,
                usuario.departamento,
                usuario.cargo,
                int(usuario.status),
                usuario.id,
            )
        )

        if resultado.rowcount == 0:
            raise ValueError("Usuário não encontrado.")

        if fechar_conexao:
            conexao.commit()

    except Exception:
        if fechar_conexao:
            conexao.rollback()
        raise

    finally:
        if fechar_conexao:
            conexao.close()

def desativar_usuario(usuario_id, conexao=None):
    fechar_conexao = conexao is None

    if fechar_conexao:
        conexao = conectar()

    try:
        resultado = conexao.execute(
            """
            UPDATE usuarios
            SET status = 0
            WHERE id = ? AND status = 1
            """,
            (usuario_id,)
        )

        if resultado.rowcount == 0:
            raise ValueError(
                "Usuário não encontrado ou já desativado."
            )

        if fechar_conexao:
            conexao.commit()

    except Exception:
        if fechar_conexao:
            conexao.rollback()
        raise

    finally:
        if fechar_conexao:
            conexao.close()

def reativar_usuario(usuario_id, conexao=None):
    fechar_conexao = conexao is None

    if fechar_conexao:
        conexao = conectar()

    try:
        resultado = conexao.execute(
            """
            UPDATE usuarios
            SET status = 1
            WHERE id = ? AND status = 0
            """,
            (usuario_id,)
        )

        if resultado.rowcount == 0:
            raise ValueError(
                "Usuário não encontrado ou já ativo."
            )

        if fechar_conexao:
            conexao.commit()

    except Exception:
        if fechar_conexao:
            conexao.rollback()
        raise

    finally:
        if fechar_conexao:
            conexao.close()

def desativar_permissao(permissao_id, conexao=None):
    fechar_conexao = conexao is None

    if fechar_conexao:
        conexao = conectar()

    try:
        resultado = conexao.execute(
            """
            UPDATE permissoes
            SET status = 0
            WHERE id = ? AND status = 1
            """,
            (permissao_id,)
        )

        if resultado.rowcount == 0:
            raise ValueError(
                "Permissão não encontrada ou já desativada."
            )

        if fechar_conexao:
            conexao.commit()

    except Exception:
        if fechar_conexao:
            conexao.rollback()
        raise

    finally:
        if fechar_conexao:
            conexao.close()

def associar_usuario_grupo(grupo_id, usuario_id, conexao=None):
    fechar_conexao = conexao is None

    if fechar_conexao:
        conexao = conectar()

    try:
        conexao.execute(
            """
            INSERT INTO grupo_usuarios (grupo_id, usuario_id)
            VALUES (?, ?)
            """,
            (grupo_id, usuario_id)
        )

        if fechar_conexao:
            conexao.commit()

    except Exception:
        if fechar_conexao:
            conexao.rollback()
        raise

    finally:
        if fechar_conexao:
            conexao.close()


def associar_role_grupo(grupo_id, role_id, conexao=None):
    fechar_conexao = conexao is None

    if fechar_conexao:
        conexao = conectar()

    try:
        conexao.execute(
            """
            INSERT INTO grupo_roles (grupo_id, role_id)
            VALUES (?, ?)
            """,
            (grupo_id, role_id)
        )

        if fechar_conexao:
            conexao.commit()

    except Exception:
        if fechar_conexao:
            conexao.rollback()
        raise

    finally:
        if fechar_conexao:
            conexao.close()

def consultar_usuario_login(matricula, conexao=None):
    fechar_conexao = conexao is None

    if fechar_conexao:
        conexao = conectar()

    try:
        registro = conexao.execute(
            """
            SELECT id, matricula, status, senha_hash
            FROM usuarios
            WHERE matricula = ?
            """,
            (matricula,)
        ).fetchone()

        return registro

    finally:
        if fechar_conexao:
            conexao.close()