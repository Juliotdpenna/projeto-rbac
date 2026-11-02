from getpass import getpass

from database.repositorio import consultar_usuario_login, conectar
from utils.seguranca import gerar_hash_senha


MATRICULA = "MAT-TESTE-9999"


def redefinir_senha():
    registro = consultar_usuario_login(MATRICULA)

    if registro is None:
        print("Usuário administrador não encontrado.")
        return

    senha = getpass("Digite a nova senha: ")
    confirmacao = getpass("Confirme a nova senha: ")

    if len(senha) < 12:
        print("A senha precisa ter pelo menos 12 caracteres.")
        return

    if senha != confirmacao:
        print("As senhas não coincidem.")
        return

    senha_hash = gerar_hash_senha(senha)

    conexao = conectar()

    try:
        cursor = conexao.cursor()
        cursor.execute(
            """
            UPDATE usuarios
            SET senha_hash = ?
            WHERE matricula = ?
            """,
            (senha_hash, MATRICULA),
        )

        if cursor.rowcount != 1:
            raise RuntimeError("Não foi possível atualizar a senha.")

        conexao.commit()
        print("Senha redefinida com sucesso.")

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()


if __name__ == "__main__":
    redefinir_senha()