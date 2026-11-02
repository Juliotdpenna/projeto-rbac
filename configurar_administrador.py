import os

from dotenv import load_dotenv

from database.conexao import conectar
from database.repositorio import (
    consultar_roles,
    consultar_permissoes,
    consultar_usuarios,
    cadastrar_role,
    associar_permissao_role,
    associar_role_usuario,
)
from models.role import Role


load_dotenv()

ADMIN_MATRICULA = os.getenv("ADMIN_MATRICULA")
NOME_ROLE = "ROLE_ADMINISTRADOR"


def configurar_administrador():
    if not ADMIN_MATRICULA:
        raise RuntimeError(
            "Configure ADMIN_MATRICULA no arquivo .env."
        )

    conexao = conectar()

    try:
        # 1. Localiza e verifica o usuário
        usuarios = consultar_usuarios(conexao=conexao)

        usuario = next(
            (
                u for u in usuarios
                if u.matricula == ADMIN_MATRICULA
            ),
            None,
        )

        if usuario is None or not usuario.status:
            raise RuntimeError(
                "Usuário inexistente ou desativado."
            )

        # 2. Localiza ou cria a Role administrativa
        roles = consultar_roles(conexao=conexao)

        role_admin = next(
            (r for r in roles if r.nome == NOME_ROLE),
            None,
        )

        if role_admin is None:
            role_admin = Role(
                None,
                NOME_ROLE,
                "Role administrativa do ambiente de desenvolvimento",
                True,
            )

            cadastrar_role(role_admin, conexao=conexao)

            print("Role administrativa criada.")

        elif not role_admin.status:
            raise RuntimeError(
                "A Role administrativa está desativada."
            )

        # 3. Associa as permissões ativas
        permissoes = consultar_permissoes(conexao=conexao)

        permissoes_existentes = {
            p.id for p in role_admin.permissoes
        }

        for permissao in permissoes:
            if not permissao.status:
                continue

            if permissao.id not in permissoes_existentes:
                associar_permissao_role(
                    role_admin.id,
                    permissao.id,
                    conexao=conexao,
                )

                print(
                    f"Permissão associada: {permissao.nome}"
                )

        # 4. Associa a Role ao usuário
        if not any(
            r.id == role_admin.id
            for r in usuario.roles_diretas
        ):
            associar_role_usuario(
                usuario.id,
                role_admin.id,
                conexao=conexao,
            )

            print("Role associada ao usuário.")

        conexao.commit()

        print("\nConfiguração administrativa concluída.")

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()


if __name__ == "__main__":
    configurar_administrador()